from . import db
from .rule import Rule
from .match import Match


class TeamRanking(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)  # Foreign key and primary key
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    total_draws = db.Column(db.Integer, default=0)
    win_loss_difference = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    total_goals = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer, nullable=False)

    # Relationship with Team
    team = db.relationship('Team', backref=db.backref('team_ranking', uselist=False, cascade='all, delete-orphan'))

    @property
    def team_name(self):
        return self.team.name

    def update_score(self):
        wins_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score > Match.guest_score
        ).count()

        wins_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score < Match.guest_score
        ).count()
        self.total_wins = wins_as_host + wins_as_guest

        lose_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score < Match.guest_score
        ).count()

        lose_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score > Match.guest_score
        ).count()
        self.total_losses = lose_as_host + lose_as_guest

        draw_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score == Match.guest_score
        ).count()

        draw_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score == Match.guest_score
        ).count()
        self.total_draws = draw_as_host + draw_as_guest
        db.session.commit()