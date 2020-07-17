from util.general import send_generic_msg
from nio import Api as MatrixApi
from nio import UploadError
from util.general import get_file_and_upload, get_image_width_and_height, UnidentifiedImageError
from io import BytesIO

class avatar:
    def __init__(self) -> None:
        super().__init__()
        self.description = "Changes the bots avatar."
        self.bot_admin_only = True

    async def execute(self, client, room, args):
        url = "".join(args)

        upload_response, request, content_type, filesize = await get_file_and_upload(client, url)

        # Get the width and height
        try:
            width, height = get_image_width_and_height(BytesIO(request.content))
        except UnidentifiedImageError as e:
            return await send_generic_msg(client, room, f"{e.strerror} | Filesize: {filesize} | Extension: {extension}")

        # Check if width and height is OK
        if width != height:
            await send_generic_msg(client, room, "This image isn't cubical, But I will still try and set it!")

        # Send the UploadError message if there is one
        if type(upload_response) == UploadError:
            return await send_generic_msg(client, room, f"{upload_response.message} | Filesize: {filesize} | Extension: {extension}")

        print(await client.set_avatar(upload_response.content_uri))
        return await send_generic_msg(client, room, f'I set my avatar to "{url}"!')