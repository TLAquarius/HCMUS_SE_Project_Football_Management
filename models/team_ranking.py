from . import db
from .rule import Rule
from .match import Match


class TeamRanking(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    total_draws = db.Column(db.Integer, default=0)
    win_loss_difference = db.Column(db.Integer, default=0)
    total_point = db.Column(db.Integer, default=0)
    total_goals = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    team = db.relationship('Team', backref='team_ranking')

    def calculate__difference(self):
        self.win_loss_difference = self.total_wins - self.total_losses
        db.session.commit()

    def update_deleted_match(self, win=False, loss=False, draw=False):
        if win:
            self.total_wins -= 1
        if loss:
            self.total_losses -= 1
        if draw:
            self.total_draws -= 1
        self.calculate_win_loss_difference()
        db.session.commit()

    def update_match_record(self, win=False, loss=False, draw=False):
        if win:
            self.total_wins += 1
        if loss:
            self.total_losses += 1
        if draw:
            self.total_draws += 1
        self.calculate_win_loss_difference()
        db.session.commit()

    def update_total_points(self):
        rule = Rule.query.filter_by(id=self.season.rule_id).first()
        if rule:
            win_points = rule.win_point
            draw_points = rule.draw_point
            self.total_points = (self.total_wins * win_points) + (self.total_draws * draw_points)
            db.session.commit()

    def update_total_goals(self):
        # Assuming you have a Match model that tracks goals
        matches = Match.query.filter((Match.host_team_id == self.team_id)|(Match.guest_team_id == self.team_id)).all()

        total_goals = 0
        for match in matches:
            if match.host_team_id == self.team_id:
                total_goals += match.host_score
            if match.guest_team_id == self.team_id:
                total_goals += match.guest_score

        self.total_goals = total_goals
        db.session.commit()

    def update_team_rankings(self):
        rankings = TeamRanking.query.filter_by(season_id=self.season_id).all()

        # Sort the teams based on ranking criteria
        rankings.sort(key=lambda r: (
            r.total_points,
            r.win_loss_difference,
            r.total_goals,
            # Additional head-to-head comparison should be implemented if needed
        ), reverse=True)

        # Update the rank attribute based on the sorted order
        for rank, team_ranking in enumerate(rankings, start=1):
            team_ranking.ranking = rank

        db.session.commit()