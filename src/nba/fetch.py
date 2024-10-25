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
    
    if procedure == 'games':
        return fetch_games(*arguments[1:])
    
    if procedure == 'teams':
        return fetch_teams()
    
    print(f'Invalid procedure type \'{procedure}\'')
    
def fetch_teams():
    if not os.path.exists('data/stats'):
        os.makedirs('data/stats')
        
    with open(f'data/stats/teams.json', 'w') as file:\
        file.write(json.dumps(teams))
        
    print(f'Successfully saved teams as a raw json')
    
def fetch_games(*arguments: list[str]):
    if len(arguments) == 0:
        return print('No season type provided')

    season_type = arguments[0]
    
    if season_type == 'latest':
        return fetch_latest_games()
    
    if season_type == 'all':
        return fetch_all_games(5)
        
    if season_type == 'specific':
        if len(arguments) == 1:
            return print('No season provided')
        
        season = arguments[1]
        return fetch_specific_games(season)
    
    print(f'Invalid season type \'{season_type}\'')

def fetch_latest_games():
    fetch_specific_games(current_season())
    
def fetch_all_games(timeout_seconds: float):
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