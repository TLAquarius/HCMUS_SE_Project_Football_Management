from . import db

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    score_time = db.Column(db.Integer, nullable=False)
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_type.id'), nullable=False)

    match = db.relationship('Match', backref=db.backref('results', cascade='all, delete-orphan', lazy=True))
    team = db.relationship('Team', backref=db.backref('results', lazy=True))
    player = db.relationship('Player', backref=db.backref('score_events', lazy=True))
    score_type = db.relationship('ScoreType', backref=db.backref('results', lazy=True))

    def get_season_id(self):
        return self.team.season_id
    
    def get_score_type(self):
        return self.score_type.name