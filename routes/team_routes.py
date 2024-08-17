from flask import render_template, request, redirect, url_for
from models import db, Team, Player
import os
from werkzeug.utils import secure_filename
from datetime import datetime

def setup_team_routes(app):
    @app.route('/season/<int:season_id>/register-team', methods=['GET', 'POST'])
    def register_team(season_id):
        if request.method == 'POST':
            team_name = request.form['team_name']
            team_stadium = request.form['team_stadium']
            profile_picture = request.files['profile_picture']
            season_id = request.form.get('season_id')  # Retrieve the season ID from the form

            if profile_picture:
                profile_picture_filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join('static/images', profile_picture_filename)
                profile_picture.save(profile_picture_path)
            else:
                profile_picture_filename = None

            new_team = Team(
                name=team_name,
                stadium=team_stadium,
                profile_picture='images/' + profile_picture_filename if profile_picture_filename else None,
                season_id=season_id
            )
            db.session.add(new_team)
            db.session.commit()

            # Adding players to the team
            player_names = request.form.getlist('player_name[]')
            player_types = request.form.getlist('player_type[]')
            player_birthdays = request.form.getlist('player_birthday[]')
            player_notes = request.form.getlist('player_note[]')
            player_profile_pictures = request.files.getlist('player_profile_picture[]')

            for name, p_type, birthday_str, note, profile_picture in zip(player_names, player_types, player_birthdays, player_notes, player_profile_pictures):
                try:
                    birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                except ValueError:
                    birthday = None  # Handle invalid date format if necessary

                if profile_picture:
                    profile_picture_filename = secure_filename(profile_picture.filename)
                    profile_picture_path = os.path.join('static/images', profile_picture_filename)
                    profile_picture.save(profile_picture_path)
                else:
                    profile_picture_filename = None

                new_player = Player(
                    name=name,
                    player_type=p_type,
                    birthday=birthday,
                    note=note,
                    profile_picture='images/' + profile_picture_filename if profile_picture_filename else None,
                    team_id=new_team.id,
                )
                db.session.add(new_player)

            db.session.commit()
            return redirect(url_for('view_season', season_id=season_id))

        return render_template('team_register.html', season_id=season_id)
    
    @app.route('/season/<int:season_id>/search_team', methods=['GET'])
    def search_team(season_id, team_id=None):
        search_term = request.args.get('search')
        if search_term:
            teams = Team.query.filter(Team.name.ilike(f"%{search_term}%")).all()
        else:
            teams = Team.query.filter_by(season_id=season_id).all()
        details=None
        if team_id:
            details = Team.query.filter_by(id=team_id).first()
        return render_template('search_team.html', teams=teams, season_id=season_id, details=details)
