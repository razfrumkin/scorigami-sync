from datetime import datetime
from dataclasses import dataclass
from .team_game_stats import TeamGameStats

@dataclass
class Game:
    id: str
    season_id: str
    time: datetime
    winner: TeamGameStats
    loser: TeamGameStats