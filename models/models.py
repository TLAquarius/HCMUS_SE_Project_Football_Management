from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)

    rules = db.relationship('Rule', backref=db.backref('seasons', lazy=True))


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter1 = db.Column(db.String(50))
    parameter2 = db.Column(db.String(50))
    # Add more rule parameters as needed


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    national_players_count = db.Column(db.Integer, default=0)
    foreign_players_count = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    profile_picture = db.Column(db.String(255))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    player_type = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    total_score = db.Column(db.Integer, default=0, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    team = db.relationship('Team', backref=db.backref('players', lazy=True))


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    match_datetime = db.Column(db.DateTime, nullable=False)
    host_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    guest_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    host_team = db.relationship('Team', foreign_keys=[host_team_id], backref=db.backref('home_matches', lazy=True))
    guest_team = db.relationship('Team', foreign_keys=[guest_team_id], backref=db.backref('away_matches', lazy=True))

    host_score = db.Column(db.Integer, default=0, nullable=False)
    guest_score = db.Column(db.Integer, default=0, nullable=False)

    @property
    def stadium(self):
        return self.host_team.stadium


class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    score_time = db.Column(db.Integer, nullable=False)
    score_type = db.Column(db.String(10), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    match = db.relationship('Match', backref=db.backref('results', lazy=True))
    team = db.relationship('Team', backref=db.backref('results', lazy=True))
    player = db.relationship('Player', backref=db.backref('score_events', lazy=True))

    def __repr__(self):
        return f'<MatchResult {self.id} - Match {self.match_id}, Team {self.team_id}, Player {self.player_id}>'


class TeamRanking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    total_draws = db.Column(db.Integer, default=0)
    win_loss_difference = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    team = db.relationship('Team', backref=db.backref('ranking', uselist=False))

