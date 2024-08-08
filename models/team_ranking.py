from . import db
from .rule import Rule
from .match import Match


class TeamRanking(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)  # Foreign key and primary key
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    total_draws = db.Column(db.Integer, default=0)
    win_loss_difference = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    total_goals = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer, nullable=False)

    # Relationship with Team
    team = db.relationship('Team', backref=db.backref('team_ranking', uselist=False, cascade='all, delete-orphan'))