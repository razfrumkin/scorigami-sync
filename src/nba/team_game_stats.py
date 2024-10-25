from dataclasses import dataclass
from datetime import datetime

@dataclass
class TeamGameStats:
    game_id: str
    team_id: str
    points: int
    season_id: str
    time: datetime
    matchup: str