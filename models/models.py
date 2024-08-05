from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_param_1 = db.Column(db.String(100), nullable=True)  # Example parameter
    rule_param_2 = db.Column(db.String(100), nullable=True)  # Example parameter
    # Add more parameters as needed

    def __repr__(self):
        return f'<Rule {self.id} - Params {self.rule_param_1}, {self.rule_param_2}>'


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=True)  # Foreign key to Rule

    # Relationships
    rule = db.relationship('Rule', backref=db.backref('seasons', lazy=True))

    teams = db.relationship('Team', backref='season', lazy=True)
    players = db.relationship('Player', backref='season', lazy=True)
    matches = db.relationship('Match', backref='season', lazy=True)
    match_results = db.relationship('MatchResult', backref='season', lazy=True)
    team_rankings = db.relationship('TeamRanking', backref='season', lazy=True)

    def __repr__(self):
        return f'<Season {self.id} - Name {self.name}>'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    national_players_count = db.Column(db.Integer, default=0)
    foreign_players_count = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    players = db.relationship('Player', backref='team', lazy=True, cascade="all, delete-orphan")
    matches_hosted = db.relationship('Match', foreign_keys='Match.host_team_id', backref='host_team', lazy=True)
    matches_visited = db.relationship('Match', foreign_keys='Match.guest_team_id', backref='guest_team', lazy=True)

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

class MatchSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    match = db.relationship('Match', backref=db.backref('schedule', uselist=False))


class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    score_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    score_type = db.Column(db.String(10), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    match = db.relationship('Match', backref=db.backref('results', lazy=True))
    team = db.relationship('Team', backref=db.backref('results', lazy=True))
    player = db.relationship('Player', backref=db.backref('score_events', lazy=True))

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
