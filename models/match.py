from . import db


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