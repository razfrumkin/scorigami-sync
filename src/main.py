import sys
from nba import nba

def main(*arguments: list[str]):
    if len(arguments) == 0:
        return print('No league provided')
    
    league = arguments[0]

    leagues = {
        'nba': lambda: nba.execute(*arguments[1:])
    }

    return leagues.get(league, lambda: print(f'League \'${league}\' does not exist'))()

if __name__ == '__main__':
    main(*sys.argv[1:])