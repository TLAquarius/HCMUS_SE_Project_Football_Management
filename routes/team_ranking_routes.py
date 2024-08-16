from flask import render_template, request, redirect, url_for
from models import db, Season, Team, Player, Match, MatchResult, TeamRanking
import os
from datetime import date
from werkzeug.utils import secure_filename

def setup_team_ranking_routes(app):
    @app.route('/season/<int:season_id>/rank_team', methods=['GET'])
    def view_team_rank(season_id):
        season = Season.query.get_or_404(season_id)
        teams = Team.query.filter_by(season_id=season_id).all()
        # Get ranking information for each team
        team_rankings = []
        for team in teams:
            team_ranking = TeamRanking.query.filter_by(team_id=team.id).first()
            if team_ranking:
                team_rankings.append(team_ranking)
            else:
                # Create a placeholder TeamRanking object if not found
                team_ranking = TeamRanking(team_id=team.id, total_wins=0, total_losses=0, total_draws=0, win_loss_difference=0, total_points=0, total_goals=0, ranking=0)
                team_rankings.append(team_ranking)
        team_rankings.sort(key=lambda x: (x.ranking), reverse=False)
        return render_template('team_ranking.html', season=season, team_rankings=team_rankings, today=date.today().strftime("%d-%m-%Y"))