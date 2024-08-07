from flask import render_template, request, redirect, url_for
from datetime import datetime
from models import db, Team, Match, Season

def setup_match_routes(app):
    @app.route('/season/<int:season_id>/match_schedule', methods=['GET', 'POST'])
    def match_schedule(season_id):
        season = Season.query.get_or_404(season_id)
        teams = Team.query.filter_by(season_id=season_id).all()

        if request.method == 'POST':
            round_number = request.form.get('round_number')
            match_datetime = request.form.get('match_datetime')
            host_team_id = request.form.get('host_team_id')
            guest_team_id = request.form.get('guest_team_id')

            new_match = Match(
                round_number=int(round_number),
                match_datetime=datetime.strptime(match_datetime, '%Y-%m-%dT%H:%M'),
                host_team_id=int(host_team_id),
                guest_team_id=int(guest_team_id),
                season_id=season_id
            )

            db.session.add(new_match)
            db.session.commit()
            return redirect(url_for('view_season', season_id=season_id))

        return render_template('match_schedule.html', season=season, teams=teams)