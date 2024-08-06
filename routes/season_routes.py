from flask import render_template, request, redirect, url_for
from models import db, Season, Team, Player, Match, MatchResult, TeamRanking
import os
from werkzeug.utils import secure_filename

def setup_season_routes(app):
    @app.route('/season/<int:season_id>')
    def view_season(season_id):
        season = Season.query.get_or_404(season_id)
        teams = Team.query.filter_by(season_id=season_id).all()
        players = Player.query.filter_by(season_id=season_id).all()
        matches = Match.query.filter_by(season_id=season_id).all()
        match_results = MatchResult.query.filter_by(season_id=season_id).all()
        team_rankings = TeamRanking.query.filter_by(season_id=season_id).all()
        return render_template('season_main.html', season=season, teams=teams, players=players, matches=matches, match_results=match_results, team_rankings=team_rankings)
    @app.route('/add-season', methods=['GET', 'POST'])
    def add_season():
        if request.method == 'POST':
            season_name = request.form['season_name']
            season_note = request.form['note']

            profile_picture = request.files['profile_picture']
            if profile_picture:
                profile_picture_filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join('static/images', profile_picture_filename)
                profile_picture.save(profile_picture_path)
            else:
                profile_picture_filename = None

            new_season = Season(name=season_name, note=season_note, profile_picture='images/' + profile_picture_filename)
            new_season.update_latest_rule_id()

            db.session.add(new_season)
            db.session.commit()
            return redirect(url_for('view_season', season_id=new_season.id))
        return render_template('add_season.html')

    @app.route('/delete-season/<int:season_id>', methods=['POST'])
    def delete_season(season_id):
        season = Season.query.get_or_404(season_id)
        db.session.delete(season)
        db.session.commit()
        return redirect(url_for('home'))
