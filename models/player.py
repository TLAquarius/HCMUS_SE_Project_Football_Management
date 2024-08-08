from . import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    player_type = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    total_score = db.Column(db.Integer, default=0, nullable=False)

    team = db.relationship('Team', backref=db.backref('players', cascade='all, delete-orphan', lazy=True))