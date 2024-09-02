from . import db
from .match import Match
from .match_result import MatchResult
from .season import Season
from .team import Team


class TeamRanking(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)  # Foreign key and primary key
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    total_draws = db.Column(db.Integer, default=0)
    win_loss_difference = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    total_goals = db.Column(db.Integer, default=0)
    ranking = db.Column(db.Integer, nullable=False, default=0)

    # Relationship with Team
    team = db.relationship('Team', backref=db.backref('team_ranking', uselist=False, cascade='all, delete-orphan'))

    @property
    def team_name(self):
        return self.team.name

    @property
    def season_id(self):
        return self.team.season_id

    @classmethod
    def insert_default_value(cls, team_id):
        existing_ranking = TeamRanking.query.filter_by(team_id=team_id).first()
        if not existing_ranking:
            # Create a new TeamRanking with default values
            new_ranking = TeamRanking(
                team_id=team_id,
                total_wins=0,
                total_losses=0,
                total_draws=0,
                win_loss_difference=0,
                total_points=0,
                total_goals=0,
                ranking=0
            )
            db.session.add(new_ranking)
            db.session.commit()

    def update_score(self):
        wins_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score > Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()

        wins_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score < Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()
        self.total_wins = wins_as_host + wins_as_guest

        lose_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score < Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()

        lose_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score > Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()
        self.total_losses = lose_as_host + lose_as_guest

        draw_as_host = Match.query.filter(
            Match.host_team_id == self.team_id,
            Match.host_score == Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()

        draw_as_guest = Match.query.filter(
            Match.guest_team_id == self.team_id,
            Match.host_score == Match.guest_score,
            Match.host_score.isnot(None),
            Match.guest_score.isnot(None)
        ).count()
        self.total_draws = draw_as_host + draw_as_guest
        self.win_loss_difference = self.total_wins - self.total_losses
        db.session.commit()

    def update_points(self):
        season = self.team.season
        rule = season.rule

        self.total_points = (
                self.total_wins * rule.win_point +
                self.total_draws * rule.draw_point +
                self.total_losses * rule.lose_point
        )
        db.session.commit()

    def update_total_goals(self):
        # Count the number of MatchResult records for the current team
        total_goals = MatchResult.query.filter(
            MatchResult.team_id == self.team_id
        ).count()

        self.total_goals = total_goals
        db.session.commit()

    @classmethod
    def update_rankings(cls, season_id):
        # Retrieve the rule for the specific season
        season = Season.query.get(season_id)
        rule = season.rule

        # Retrieve all team rankings for the specific season
        team_rankings = TeamRanking.query.join(Team).filter(Team.season_id == season_id).all()

        # Define a function to get head-to-head comparison between two teams
        def head_to_head_comparison(team_ranking_a, team_ranking_b):
            # Find matches where these two teams played against each other
            matches = Match.query.filter(
                ((Match.host_team_id == team_ranking_a.team_id) & (Match.guest_team_id == team_ranking_b.team_id)) |
                ((Match.host_team_id == team_ranking_b.team_id) & (Match.guest_team_id == team_ranking_a.team_id))
            ).all()

            # Count wins for both teams in head-to-head matches
            wins_a = sum(1 for match in matches if
                         (match.host_team_id == team_ranking_a.team_id and match.host_score > match.guest_score) or
                         (match.guest_team_id == team_ranking_a.team_id and match.guest_score > match.host_score))

            wins_b = sum(1 for match in matches if
                         (match.host_team_id == team_ranking_b.team_id and match.host_score > match.guest_score) or
                         (match.guest_team_id == team_ranking_b.team_id and match.guest_score > match.host_score))

            if wins_a != wins_b:
                return wins_a - wins_b  # Return the difference in wins

            # If the number of wins is equal, compare total goals in head-to-head matches
            total_goals_a = sum(match.host_score for match in matches if match.host_team_id == team_ranking_a.team_id) + \
                            sum(match.guest_score for match in matches if match.guest_team_id == team_ranking_a.team_id)

            total_goals_b = sum(match.host_score for match in matches if match.host_team_id == team_ranking_b.team_id) + \
                            sum(match.guest_score for match in matches if match.guest_team_id == team_ranking_b.team_id)

            return total_goals_a - total_goals_b  # Return the difference in goals

        # Define a function to get the sorting key based on priority
        def get_sorting_key(team_ranking):
            # Extract priority values
            p1 = rule.priority1
            p2 = rule.priority2
            p3 = rule.priority3
            p4 = rule.priority4

            # Define priorities mapping
            priorities = {
                1: team_ranking.total_points,
                2: team_ranking.win_loss_difference,
                3: team_ranking.total_goals,
                4: lambda tr: head_to_head_comparison(team_ranking, tr)  # Lambda for head-to-head comparison
            }

            # Generate a sorting tuple based on priority order
            def priority_value(p):
                # If the priority is a callable (lambda function), execute it
                if callable(priorities.get(p)):
                    return -priorities.get(p)(team_ranking)  # Use negative for descending order
                return -priorities.get(p, 0)  # Use negative for descending order if it's a value

            return (
                priority_value(p1),
                priority_value(p2),
                priority_value(p3),
                priority_value(p4)
            )

        # Sort team rankings using the custom key function
        team_rankings.sort(key=lambda tr: get_sorting_key(tr))

        # Update rankings
        for index, team_ranking in enumerate(team_rankings):
            team_ranking.ranking = index + 1

        # Commit changes to the database
        db.session.commit()
