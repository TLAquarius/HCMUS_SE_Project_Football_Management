from flask import render_template, request, redirect, url_for
from models import db, Team
import os
from werkzeug.utils import secure_filename

def setup_team_routes(app):
    @app.route('/register-team/<int:season_id>', methods=['GET', 'POST'])
    def register_team(season_id):
        if request.method == 'POST':
            team_name = request.form['team_name']
            team_stadium = request.form['team_stadium']

            profile_picture = request.files['profile_picture']
            if profile_picture:
                profile_picture_filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join('static/images', profile_picture_filename)
                profile_picture.save(profile_picture_path)
            else:
                profile_picture_filename = None

            new_team = Team(name=team_name, stadium=team_stadium, profile_picture='images/' + profile_picture_filename, season_id=season_id)
            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for('view_season', season_id=season_id))
        return render_template('team_register.html', season_id=season_id)