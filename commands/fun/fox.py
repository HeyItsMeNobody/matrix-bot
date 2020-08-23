import requests
from nio import Api as MatrixApi
from io import BufferedReader, BytesIO
from util.general import get_image_width_and_height, send_generic_msg, allowed_image_type, requests_upload_helper, get_file_and_upload
from mimetypes import guess_extension
from util.BaseCommand import BaseCommand
from nio import UploadError
from PIL import UnidentifiedImageError

class fox(BaseCommand):
    def __init__(self) -> None:
        super().__init__()
        self.description = "Sends fox pictures (Broken thumbnail)"

    async def execute(self, client, room, args):
        # Get and upload the dog picture
        upload_response, request, content_type, filesize, extension = await self.get_and_upload_fox_picture(client)

        # Get the width and height
        try:
            width, height = get_image_width_and_height(BytesIO(request.content))
        except UnidentifiedImageError as e:
            return await send_generic_msg(client, room, f"{e.strerror} | Filesize: {filesize} | Extension: {extension}")

        # Send the UploadError message if there is one
        if type(upload_response) == UploadError:
            return await send_generic_msg(client, room, f"{upload_response.message} | Filesize: {filesize} | Extension: {extension}")

        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content = {
                "msgtype": MatrixApi.mimetype_to_msgtype(content_type),
                "body": "fox" + extension,
                "url": upload_response.content_uri,
                "info": {
                    "size": filesize,
                    "mimetype": content_type,
                    "thumbnail_info": {
                        "w": width,
                        "h": height,
                        "mimetype": content_type,
                        "size": filesize,
                    },
                    "w": width,
                    "h": height,
                    "thumbnail_url": upload_response.content_uri,
                },
            }
        )

    async def get_and_upload_fox_picture(self, client):
        """ Returns upload_response, request, content_type, filesize, extension """
        # Get the image url
        image_url = "https://foxrudor.de/"

        # Get the image and upload it
        upload_response, request, content_type, filesize = await get_file_and_upload(client, image_url)
        extension = guess_extension(content_type)

        # See if the extension is allowed
        if not allowed_image_type("fox" + extension):
            return await self.get_and_upload_fox_picture(client)

        return upload_response, request, content_type, filesize, extension
