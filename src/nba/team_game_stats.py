from datetime import datetime
from dataclasses import dataclass

@dataclass
class TeamGameStats:
    game_id: str
    team_id: str
    points: int
    season: str
    time: datetime
    matchup: str