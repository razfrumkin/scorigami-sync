from datetime import datetime

def year_to_season(year: int) -> str:
    last_two_digits = str(year + 1)[-2:]
    return f'{year}-{last_two_digits}'

def season_to_year(season: str) -> int:
    year_str = season.split('-')[0]
    return int(year_str)

def current_year() -> int:
    return datetime.now().year

def current_season() -> str:
    return year_to_season(current_year() - 1)

def parse_date(date_str) -> datetime:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

NBA_START_YEAR = 1946