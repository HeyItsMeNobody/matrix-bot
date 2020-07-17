class BaseCommand:
    def __init__(self) -> None:
        self.description = "Base command."
        self.arguments = {"--example -e": {"accepts": None, "description": None}}
        self.bot_admin_only = False

    async def execute(self, client, room, args):
        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "body": "Base command!",
            }
        )