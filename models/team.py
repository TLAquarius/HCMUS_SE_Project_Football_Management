from . import db
from .player import Player

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    national_players_count = db.Column(db.Integer, default=0)
    foreign_players_count = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    profile_picture = db.Column(db.String(255))

    def update_player_counts(self):
        self.total_native_players = Player.query.filter_by(team_id=self.id, player_type='native').count()
        self.total_foreign_players = Player.query.filter_by(team_id=self.id, player_type='foreign').count()
        db.session.commit()

    def total_player(self):
        return self.total_native_players + self.total_foreign_players