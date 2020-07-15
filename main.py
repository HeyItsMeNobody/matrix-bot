import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText, MatrixInvitedRoom, InviteEvent
from datetime import datetime

client = AsyncClient("https://synapse.dyonb.nl", "@matrix-bot:dyonb.nl")

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

    # Check if the text starts with !bot 
    raw_text = event.body
    if raw_text.startswith("!bot "):
        text = raw_text.split("!bot ")[1]
        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "body": text
            }
        )

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

    print(await client.login(""))
    
    # If you made a new room and haven't joined as that user, you can use
    # await client.join("!yjesBjOOiliyCXevUN:dyonb.nl")
    # await client.room_send(
    #     # Watch out! If you join an old room you'll see lots of old messages
    #     room_id="!yjesBjOOiliyCXevUN:dyonb.nl",
    #     message_type="m.room.message",
    #     content = {
    #         "msgtype": "m.text",
    #         "body": "Hello world!"
    #     }
    # )
    await client.sync_forever(timeout=30000) # milliseconds

asyncio.get_event_loop().run_until_complete(main())
