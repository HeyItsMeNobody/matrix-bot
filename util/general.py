from glob import glob
from importlib import import_module

import jinja2

def get_command(command):
    # Find the command file in the commands dir
    for command_path in glob(f'./commands/**/{command}.py', recursive=True):
        # Get command_name and command_dir
        command_name = command_path.rsplit('/', 1)[1].replace(".py", "")
        command_module_path = command_path.replace('./', '').replace('/', '.').replace('.py', '')
        # Import command
        command = getattr(import_module(command_module_path), f'{command_name}')

        return command

    return None

def list_all_commands():
    commands = {}
    # Find the command file in the commands dir
    for command_path in glob(f'./commands/**/*.py', recursive=True):
        # Get command_name and command_dir
        command_name = command_path.rsplit('/', 1)[1].replace(".py", "")
        command_dir = command_path.rsplit('/', 1)[0].rsplit('/',1)[1]

        if command_name != "__init__":
            if not command_dir in commands:
                commands[command_dir] = []
            commands[command_dir].append(command_name)

    return commands

async def send_generic_msg(client, room, text):
    await client.room_send(
        room_id=room.room_id,
        message_type="m.room.message",
        content = {
            "msgtype": "m.text",
            "body": text,
        }
    )

async def send_formatted_msg(client, room, text, text_html):
    await client.room_send(
        room_id=room.room_id,
        message_type="m.room.message",
        content = {
            "msgtype": "m.text",
            "body": text,
            "format": "org.matrix.custom.html",
            "formatted_body": text_html
        }
    )

def get_jinja_template(name):
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_environment = jinja2.Environment(loader=template_loader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
    return template_environment.get_template(name)