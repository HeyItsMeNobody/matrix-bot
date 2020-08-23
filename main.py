import asyncio
import requests
import aiofiles
import re
import config

from nio import AsyncClient, AsyncClientConfig, MatrixRoom, RoomMessageText, MatrixInvitedRoom, InviteEvent
from nio import Api as MatrixApi
from datetime import datetime
from io import BytesIO
from pathlib import Path
from glob import glob
from importlib import import_module
from util.general import get_command, send_generic_msg

client_config = AsyncClientConfig(max_timeouts=10)
client = AsyncClient(config.homeserver, config.user, config=client_config, ssl=False)

# When the bot receives a message
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    # See if message is older than set time and return based on that.
    when = datetime.fromtimestamp(event.server_timestamp / 1000)
    now = datetime.now()
    if (now-when).total_seconds() > 5:
        return

    # Log message
    print(
        f"Message received in room {room.display_name}\n"
        f"{event.server_timestamp} | {room.user_name(event.sender)} | {event.body}"
    )

    # Check if it's itself
    if event.sender == config.user:
        return

    # Filter out text
    raw_text = event.body
    if not raw_text.startswith("?"):
        return
    
    # Remove the first character and split at a space
    raw_text = raw_text[1:]
    raw_text_split = raw_text.split(" ")
    # Get first in split, the command.
    command = raw_text_split[0].lower()
    # Get the arguments
    args = raw_text_split
    args.pop(0)

    # Get the command class
    command = get_command(command)
    if command:
        # Initialize command class
        command = command()
        # Check if the command can only be used by bot admins, And react based on that.
        if command.bot_admin_only and event.sender not in config.owners:
            return await send_generic_msg(client, room, "You aren't permitted to use this command.")
        # Execute the command
        return await command.execute(client=client, room=room, args=args)

    # Send command not found message
    #await client.room_send(
    #    room_id=room.room_id,
    #    message_type="m.room.message",
    #    content = {
    #        "msgtype": "m.text",
    #        "body": "COMMAND NOT FOUND",
    #        "format": "org.matrix.custom.html",
    #        "formatted_body": "<h1>COMMAND NOT FOUND</h1>"
    #    }
    #)

# When invited to a room
async def on_room_invite(room: MatrixInvitedRoom, event: InviteEvent) -> None:
    # Log message
    print(
        f"Joining room with name '{room.display_name}' | ID {room.room_id}\n"
        f"Name of user who invited me: {event.sender}"
    )

    # Join the room
    await client.join(room.room_id)

async def main() -> None:
    client.add_event_callback(message_callback, RoomMessageText)
    client.add_event_callback(on_room_invite, InviteEvent)

    print(await client.login(config.password))

    await client.sync_forever(timeout=30000) # milliseconds

asyncio.get_event_loop().run_until_complete(main())
