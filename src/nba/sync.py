import json
import requests
from .utilities import current_season, current_season_year, NBA_START_YEAR, year_to_season, parse_date, season_to_year
from .game import Game
from .team_game_stats import TeamGameStats

def sync(*arguments: list[str]):
    if len(arguments) == 0:
        return print('No remote base url provided')
    
    base_url = arguments[0]

    if len(arguments) == 1:
        return print('No password provided')
    
    password = arguments[1]

    if len(arguments) == 2:
        return print('No season type provided')
    
    procedure = arguments[2]

    procedures = {
        'games': lambda: sync_games(base_url, password, *arguments[3:])
    }

    procedures.get(procedure, lambda: print(f'Invalid procedure type \'{procedure}\''))()
    
def sync_games(base_url: str, password: str, *arguments: list[str]):
    if len(arguments) == 0:
        return print('No season type provided')
        
    season_type = arguments[0]

    actions = {
        'latest': lambda: sync_latest_games(base_url, password),
        'all': lambda: sync_all_games(base_url, password),
        'specific': lambda: sync_specific_games(base_url, password, arguments[1]) if len(arguments) > 1 else print('No season provided') 
    }

    actions.get(season_type, lambda: print(f'Invalid season type \'{season_type}\''))()

def sync_latest_games(base_url: str, password: str):
    sync_specific_games(base_url, password, current_season)

def sync_all_games(base_url: str, password: str):
    end_year = current_season_year

    for year in range(NBA_START_YEAR, end_year):
        season = year_to_season(year)
        sync_specific_games(base_url, password, season)


def sync_specific_games(base_url: str, password: str, season: str):
    with open(f'data/nba/seasons/{season}.json', 'r') as file:
        data = json.loads(file.read())

    games = organize_season_by_games(data, season, season_to_year(season))
    data = [construct_dto(game) for game in games]

    response = requests.post(f'{base_url}/api/nba/games', json={'games': data}, headers={'x-admin-password': password})

    print(f'{'Successfully synced' if response.ok else 'Failed to sync'} data for the {season} season to the remote server')

def organize_season_by_games(data: dict, season: str, year: int) -> list[Game]:
    rows = data['resultSets'][0]['rowSet']
    games: dict[str, list[TeamGameStats]] = {}

    for row in rows:
        stats = parse_row_traditional(row, season) if year < 1996 else parse_row_modern(row, season)

        if stats.game_id in games: games[stats.game_id].append(stats)
        else: games[stats.game_id] = [stats]

    return [construct_game(game) for game in list(games.values())]

def construct_game(scores: list[TeamGameStats]) -> Game:
    winner_index = 0 if scores[0].points > scores[1].points else 1
    loser_index = 1 - winner_index

    winner = scores[winner_index]
    loser = scores[loser_index]

    return Game(id=winner.game_id, season=winner.season, time=winner.time, winner_points=winner.points, loser_points=loser.points, winner_matchup=winner.matchup, loser_matchup=loser.matchup, winner_id=winner.team_id, loser_id=loser.team_id)

def parse_row_traditional(row: list, season: str) -> TeamGameStats:
    return TeamGameStats(game_id=row[4], team_id=row[1], points=row[26], season=season, time=parse_date(row[5]), matchup=row[6])

def parse_row_modern(row: list, season: str) -> TeamGameStats:
    return TeamGameStats(game_id=row[4], team_id=row[1], points=row[28], season=season, time=parse_date(row[5]), matchup=row[6])

def construct_dto(game: Game) -> dict[str]:
    return {
        'id': game.id,
        'season': game.season,
        'time': str(game.time),
        'winnerPoints': game.winner_points,
        'loserPoints': game.loser_points,
        'winnerMatchup': game.winner_matchup,
        'loserMatchup': game.loser_matchup,
        'winnerId': game.winner_id,
        'loserId': game.loser_id
    }