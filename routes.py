from flask import render_template, request, redirect, url_for, abort
from models import db,Rule, Season, Team, Player, Match, MatchResult, TeamRanking

def setup_routes(app):
    @app.route('/')
    def home():
        seasons = Season.query.all()
        return render_template('index.html', seasons=seasons)

    @app.route('/season/<int:season_id>')
    def view_season(season_id):
        season = Season.query.get_or_404(season_id)
        teams = Team.query.filter_by(season_id=season_id).all()
        players = Player.query.filter_by(season_id=season_id).all()
        matches = Match.query.filter_by(season_id=season_id).all()
        match_results = MatchResult.query.filter_by(season_id=season_id).all()
        team_rankings = TeamRanking.query.filter_by(season_id=season_id).all()
        return render_template('season_main.html', season=season, teams=teams, players=players, matches=matches,match_results=match_results, team_rankings=team_rankings)

    @app.route('/add-season', methods=['GET', 'POST'])
    def add_season():
        if request.method == 'POST':
            season_name = request.form['season_name']
            new_season = Season(name=season_name)
            db.session.add(new_season)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('add_season.html')