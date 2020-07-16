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

    # Filter out text
    raw_text = event.body
    if not raw_text.startswith("!"):
        return
    
    # Remove the first character and split at a space
    raw_text = raw_text[1:]
    raw_text_split = raw_text.split(" ")
    # Get first in split, the command.
    command = raw_text_split[0].lower()
    # Get the arguments
    args = raw_text_split
    args.pop(0)

    for command_path in glob(f'./commands/**/{command}.py', recursive=True):
        # Get command_name and command_dir
        command_name = command_path.rsplit('/', 1)[1].replace(".py", "")
        command_module_path = command_path.replace('./', '').replace('/', '.').replace('.py', '')
        # Import command
        command = getattr(import_module(command_module_path), f'{command_name}')
        # Initialize and execute command
        command = command()
        print(command.help)
        await command.execute(client=client, room=room, args=args)

        return

    await client.room_send(
        room_id=room.room_id,
        message_type="m.room.message",
        content = {
            "msgtype": "m.text",
            "body": "COMMAND NOT FOUND",
            "format": "org.matrix.custom.html",
            "formatted_body": "<h1>COMMAND NOT FOUND</h1>"
        }
    )

    # if raw_text.startswith("!dog"):
    #     # Get the image url
    #     image_url_request = requests.get("https://random.dog/woof")
    #     image_url = "https://random.dog/" + image_url_request.text
    #     # Get the image
    #     content_type = requests.head(image_url).headers['Content-Type']
    #     #image = requests.get(image_url, stream=True).raw
    #     image = BytesIO(requests.get(image_url).content).getbuffer()
    #     print(image_url)
    #     print(content_type)
    #     # Upload the image
    #     upload_response, maybe_keys = await client.upload(
    #         image,
    #         content_type=MatrixApi.mimetype_to_msgtype(content_type)
    #     )
    #     # async with aiofiles.open(image) as f:
    #     #     upload_response, maybe_keys = await client.upload(
    #     #         f,
    #     #         content_type=MatrixApi.mimetype_to_msgtype(content_type)
    #     #     )

        # await client.room_send(
        #     room_id=room.room_id,
        #     message_type="m.room.message",
        #     content = {
        #         "msgtype": MatrixApi.mimetype_to_msgtype(content_type),
        #         "body": "dog.png",
        #         "file": {
        #             "url": upload_response.content_uri
        #         }
        #     }
        # )

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