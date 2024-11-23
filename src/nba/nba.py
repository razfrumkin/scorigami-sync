from .fetch import fetch
from .sync import sync

def execute(*arguments: list[str]):
    if len(arguments) == 0:
        return print('No arguments provided')
    
    command = arguments[0]

    actions = {
        'fetch': lambda: fetch(*arguments[1:]),
        'sync': lambda: sync(*arguments[1:])
    }

    actions.get(command, lambda: print(f'Invalid command \'{command}\''))()