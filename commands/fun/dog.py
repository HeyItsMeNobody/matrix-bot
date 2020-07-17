import requests
from nio import Api as MatrixApi
from io import BufferedReader, BytesIO
from util.general import get_image_width_and_height, send_generic_msg
from mimetypes import guess_extension
from util.BaseCommand import BaseCommand
from nio import UploadError

class dog(BaseCommand):
    def __init__(self) -> None:
        self.description = "Sends dog pictures (Broken thumbnail)"
        self.arguments = {"--example -e": {"accepts": None, "description": None}}

    async def execute(self, client, room, args):
        # Get the dog picture
        request, content_type, extension = self.get_dog_picture()
        # Get the filesize
        filesize = request.headers['Content-length']
        # Get the width and height
        width, height = get_image_width_and_height(BytesIO(request.content))
        # Convert image to BufferedReader for client.upload
        image = BufferedReader(BytesIO(request.content))
        # Upload the image
        upload_response, maybe_keys = await client.upload(
            image,
            content_type=MatrixApi.mimetype_to_msgtype(content_type),
            filesize=filesize
        )

        # Send the UploadError message if there is one
        if type(upload_response) == UploadError:
            return await send_generic_msg(client, room, upload_response.message)

        await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content = {
                "msgtype": MatrixApi.mimetype_to_msgtype(content_type),
                "body": "dog" + extension,
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

    def get_dog_picture(self):
        """ Returns request, content_type and extension """
        # Get the image url
        image_url_request = requests.get("https://random.dog/woof")
        image_url = "https://random.dog/" + image_url_request.text
        # Get the image
        request = requests.get(image_url)

        # Get the content_type and extension
        content_type = request.headers['Content-Type']
        extension = guess_extension(content_type)
        # See if the extension is allowed
        if not self.allowed_image_type("dog" + extension):
            return self.get_dog_picture()

        return request, content_type, extension