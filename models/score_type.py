from . import db


class ScoreType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)  # Foreign key to Season

    # Relationship with Season
    season = db.relationship('Season', backref=db.backref('score_types', cascade='all, delete-orphan', lazy=True))
