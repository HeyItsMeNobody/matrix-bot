import re
from util.BaseCommand import BaseCommand

class speak(BaseCommand):
    def __init__(self) -> None:
        self.description = "Can echo whatever you want."

    async def execute(self, client, room, args):
        text = " ".join(args)

        # Check for header option
        if (index := "--header") in args or (index := "-h") in args:
            index = args.index(index)
            option = args[index + 1]
            # Remove the header option from args
            args.pop(index); args.pop(index)

            # Check if it's a valid header tag
            hregex = re.compile('^h[1-6]$')
            if hregex.match(option):
                text = f"<{option}>{' '.join(args)}</{option}>"

        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "body": text,
                "format": "org.matrix.custom.html",
                "formatted_body": text
            }
        )