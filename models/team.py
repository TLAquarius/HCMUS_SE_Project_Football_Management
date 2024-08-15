from . import db
from models import Player

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Fixed typo
    note = db.Column(db.String(255), nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)  # Foreign key to Season

    # Relationship with Season
    season = db.relationship('Season', backref=db.backref('teams', cascade='all, delete-orphan', lazy=True))

    def count_native(self):
        return Player.query.filter_by(team_id=self.id, player_type="Trong nước").count()
    
    def count_foreign(self):
        return Player.query.filter_by(team_id=self.id, player_type="Nước ngoài").count()