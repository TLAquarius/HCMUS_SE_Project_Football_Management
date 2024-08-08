from . import db


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    minimum_age = db.Column(db.Integer, default=16)
    maximum_age = db.Column(db.Integer, default=40)
    minimum_players = db.Column(db.Integer, default=15)
    maximum_players = db.Column(db.Integer, default=22)
    maximum_foreign_players = db.Column(db.Integer, default=3)
    maximum_score_time = db.Column(db.Integer, default=96)
    win_point = db.Column(db.Integer, default=3)
    draw_point = db.Column(db.Integer, default=1)
    lose_point = db.Column(db.Integer, default=0)
    priority1 = db.Column(db.Integer, default=1)
    priority2 = db.Column(db.Integer, default=2)
    priority3 = db.Column(db.Integer, default=3)
    priority4 = db.Column(db.Integer, default=4)

    @staticmethod
    def insert_default_rule():
        if Rule.query.count() == 0:
            default_rule = Rule()
            db.session.add(default_rule)
            db.session.commit()