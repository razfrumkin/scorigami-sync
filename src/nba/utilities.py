from datetime import datetime
from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog

def year_to_season(year: int) -> str:
    last_two_digits = str(year + 1)[-2:]
    return f'{year}-{last_two_digits}'

def season_to_year(season: str) -> int:
    year_str = season.split('-')[0]
    return int(year_str)

def parse_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

NBA_START_YEAR = 1946

current_season = str(LeagueGameLog(season_type_all_star='Regular Season').get_dict()['parameters']['Season'])
current_season_year = season_to_year(current_season) + 1