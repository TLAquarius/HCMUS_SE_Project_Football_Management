from flask import render_template, request, redirect, url_for
from models import db, Season, Team, Player, Match, MatchResult, TeamRanking, ScoreType
import os
from werkzeug.utils import secure_filename
from datetime import datetime

def setup_season_routes(app):
    @app.route('/season/<int:season_id>')
    def view_season(season_id):
        season = Season.query.get_or_404(season_id)
        teams = Team.query.filter_by(season_id=season_id).all()
        players = Player.query.filter_by(season_id=season_id).all()
        matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.match_datetime < datetime.utcnow()).order_by(Match.match_datetime.desc()).all()
        match_results = MatchResult.query.filter_by(season_id=season_id).all()
        team_rankings = TeamRanking.query.join(Team).filter(Team.season_id == season_id).order_by(TeamRanking.ranking).all()
        return render_template('season_main.html', season=season, teams=teams, players=players, matches=matches, match_results=match_results, team_rankings=team_rankings)
    @app.route('/add_season', methods=['GET', 'POST'])
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
                profile_picture_filename = 'default_season_logo.png'

            new_season = Season(name=season_name, note=season_note, profile_picture='images/' + profile_picture_filename)
            new_season.update_latest_rule_id()

            db.session.add(new_season)
            db.session.commit()

            score_types = request.form.getlist('score_types')
            for score_type in score_types:
                new_score_type = ScoreType(name=score_type, season_id=new_season.id)
                db.session.add(new_score_type)
            db.session.commit()
            return redirect(url_for('view_season', season_id=new_season.id))
        return render_template('add_season.html')

    @app.route('/delete_season/<int:season_id>', methods=['POST'])
    def delete_season(season_id):
        season = Season.query.get_or_404(season_id)
        db.session.delete(season)
        db.session.commit()
        return redirect(url_for('home'))
    
    @app.route('/delete_seasons', methods=['GET', 'POST'])
    def delete_seasons():
        if request.method == 'POST':
            season_ids = request.form.getlist('season_ids')
            for season_id in season_ids:
                season = Season.query.get_or_404(int(season_id))
                db.session.delete(season)
            db.session.commit()
            return redirect(url_for('home'))
        seasons = Season.query.all()
        return render_template('delete_season.html', seasons = seasons)