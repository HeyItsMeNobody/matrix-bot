from glob import glob
from importlib import import_module

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