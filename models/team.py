from . import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    stadium = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Fixed typo
    note = db.Column(db.String(255), nullable=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)  # Foreign key to Season

    # Relationship with Season
    season = db.relationship('Season', backref=db.backref('teams', cascade='all, delete-orphan', lazy=True))