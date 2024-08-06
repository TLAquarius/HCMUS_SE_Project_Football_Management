from . import db


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    note = db.Column(db.String(255), nullable=True)

    rules = db.relationship('Rule', backref=db.backref('seasons', lazy=True))