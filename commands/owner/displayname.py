from util.general import send_generic_msg
from nio import Api as MatrixApi

class displayname:
    def __init__(self) -> None:
        super().__init__()
        self.description = "Changes the bots display name."
        self.bot_admin_only = True

    async def execute(self, client, room, args):
        text = " ".join(args)

        print(await client.set_displayname(text))
        return await send_generic_msg(client, room, f'I set my display name to "{text}"!')