from flask import render_template, request, redirect, url_for
from models import db, Player, Team
import os
from werkzeug.utils import secure_filename

def setup_player_routes(app):
    @app.route('/register-player', methods=['GET', 'POST'])
    def register_player():
        if request.method == 'POST':
            player_name = request.form['player_name']
            player_type = request.form['player_type']
            player_birthday = request.form['player_birthday']
            player_note = request.form['player_note']
            team_id = request.form['team_id']

            profile_picture = request.files['profile_picture']
            if profile_picture:
                profile_picture_filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join('static/images', profile_picture_filename)
                profile_picture.save(profile_picture_path)
            else:
                profile_picture_filename = None

            new_player = Player(
                name=player_name,
                player_type=player_type,
                birthday=player_birthday,
                note=player_note,
                profile_picture='images/' + profile_picture_filename if profile_picture_filename else None,
                team_id=team_id
            )

            db.session.add(new_player)
            db.session.commit()
            return redirect(url_for('view_season', season_id=Team.query.get_or_404(team_id).season_id))

        teams = Team.query.all()
        return render_template('player_register.html', teams=teams)

    @app.route('/search-player/<int:season_id>', methods=['GET'])
    def search_player(season_id):
        players = Player.query.filter_by(season_id=season_id).all()

        # Fetch the team names
        players_with_team_name = []
        for player in players:
            team = Team.query.get(player.team_id)
            team_name = team.name if team else 'Unknown'
            player_info = {
                'id': player.id,
                'name': player.name,
                'player_type': player.player_type,
                'birthday': player.birthday.strftime('%Y-%m-%d') if player.birthday else 'Unknown',
                'note': player.note,
                'profile_picture': player.profile_picture,
                'team_name': team_name
            }
            players_with_team_name.append(player_info)

        return render_template('search_player.html', players=players_with_team_name, season_id=season_id)