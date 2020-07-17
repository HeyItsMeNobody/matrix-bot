import re
import html2markdown

from util.BaseCommand import BaseCommand
from util.general import get_command, send_generic_msg, list_all_commands, get_jinja_template, send_formatted_msg

class help(BaseCommand):
    def __init__(self) -> None:
        super().__init__()
        self.description = "Helps you!"

    async def execute(self, client, room, args):
        # Check if args[0] doesn't exist
        if not 0 <= 0 < len(args):
            commands_list = list_all_commands()
            list_template = get_jinja_template("command_list.j2").render(categories=commands_list)
            list_markdown = html2markdown.convert(list_template)
            return await send_formatted_msg(client, room, list_markdown, list_template)

        # Search the command and send a message if it isn't found
        command_search = get_command(args[0])
        if command_search == None:
            return await send_generic_msg(client, room, "I couldn't find the command you are searching help for!")

        # Initialize the command
        command = command_search()

        help_template = get_jinja_template("help.j2").render(command=command)
        help_markdown = html2markdown.convert(help_template)

        return await send_formatted_msg(client, room, help_markdown, help_template)