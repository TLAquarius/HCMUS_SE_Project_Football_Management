from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .season import Season
from .rule import Rule
from .team import Team
from .player import Player
from .match import Match
from .match_result import MatchResult
from .team_ranking import TeamRanking