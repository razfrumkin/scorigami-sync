import os
import time
import json
from nba_api.stats.static.teams import teams
from nba_api.stats.endpoints import teamgamelogs
from .utilities import year_to_season, current_year, current_season, NBA_START_YEAR

def fetch(*arguments: list[str]):
    if len(arguments) == 0:
        return print('No data type provided')
    
    procedure = arguments[0]
    
    procedures = {
        'games': lambda: fetch_games(*arguments[1:])
    }

    procedures.get(procedure, lambda: print(f'Invalid procedure type \'{procedure}\''))()
    
def fetch_games(*arguments: list[str], timeout_seconds=7.5):
    if len(arguments) == 0:
        return print('No season type provided')

    season_type = arguments[0]

    actions = {
        'latest': lambda: fetch_latest_games(),
        'all': lambda: fetch_all_games(timeout_seconds=timeout_seconds),
        'specific': lambda: fetch_specific_games(arguments[1]) if len(arguments) > 1 else print('No season provided') 
    }

    actions.get(season_type, lambda: print(f'Invalid season type \'{season_type}\''))()
    
def fetch_latest_games():
    fetch_specific_games(current_season())
    
def fetch_all_games(timeout_seconds=7.5):
    end_year = current_year()
    
    for year in range(NBA_START_YEAR, end_year):
        season = year_to_season(year)
        fetch_specific_games(season)
        time.sleep(timeout_seconds)
        
def fetch_specific_games(season: str):
    logs = teamgamelogs.TeamGameLogs(season_nullable=season)
    data = logs.get_json()
        
    if not os.path.exists('data/nba/seasons'):
        os.makedirs('data/nba/seasons')
        
    with open(f'data/nba/seasons/{season}.json', 'w') as file:
        file.write(data)
        
    print(f'Successfully saved data for the {season} season as a raw json')