from . import db
from .rule import Rule


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Fixed typo
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    note = db.Column(db.String(255), nullable=True)

    rule = db.relationship('Rule', backref=db.backref('seasons', lazy=True))
    def update_latest_rule_id(self):
        latest_rule = Rule.query.order_by(Rule.id.desc()).first()
        if latest_rule:
            self.rule_id = latest_rule.id
        else:
            Rule.insert_default_rule()
            latest_rule = Rule.query.order_by(Rule.id.desc()).first()
            self.rule_id = latest_rule.id