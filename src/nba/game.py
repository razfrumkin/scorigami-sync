from datetime import datetime
from dataclasses import dataclass

@dataclass
class Game:
    id: str
    season: str
    time: datetime
    winner_points: int
    loser_points: int
    winner_matchup: str
    loser_matchup: str
    winner_id: int
    loser_id: int