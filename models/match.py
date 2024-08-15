from . import db
from models import MatchResult

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    match_datetime = db.Column(db.DateTime, nullable=False)
    host_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    guest_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    host_score = db.Column(db.Integer, default=0, nullable=False)
    guest_score = db.Column(db.Integer, default=0, nullable=False)

    # Relationship with Teams
    host_team = db.relationship('Team', foreign_keys=[host_team_id],backref=db.backref('home_matches', cascade='all, delete-orphan', lazy=True))
    guest_team = db.relationship('Team', foreign_keys=[guest_team_id],backref=db.backref('away_matches', cascade='all, delete-orphan', lazy=True))

    @property
    def stadium(self):
        return self.host_team.stadium

    @property
    def host_team_name(self):
        return self.host_team.name

    @property
    def guest_team_name(self):
        return self.guest_team.name
    @property
    def season_id(self):
        return self.host_team.season_id
    
    def update_match_score(self):
        host_team_score = MatchResult.query.filter_by(match_id = self.id, team_id= self.host_team_id).count()
        guest_team_score = MatchResult.query.filter_by(match_id = self.id, team_id= self.guest_team_id).count()
        self.host_score = host_team_score
        self.guest_score = guest_team_score
        db.session.commit()