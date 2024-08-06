from . import db


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