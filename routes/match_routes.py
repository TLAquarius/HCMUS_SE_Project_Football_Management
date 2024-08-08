from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Team, Match, Season, MatchResult, Player

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

    @app.route('/season/<int:season_id>/update_result', methods=['GET', 'POST'])
    def update_result(season_id):
        if request.method == 'POST':
            match_id = request.form['match_id']
            host_score = request.form['host_score']
            guest_score = request.form['guest_score']

            match = Match.query.get(match_id)
            if not match:
                return redirect(url_for('update_result', season_id=season_id))

            # Update match scores
            match.host_score = host_score
            match.guest_score = guest_score

            # Delete old results
            MatchResult.query.filter_by(match_id=match_id).delete()

            # Add new results
            for key, value in request.form.items():
                if key.startswith('player_id_'):
                    row_index = key.split('_')[2]
                    player_id = value
                    score_type = request.form.get(f'score_type_{row_index}')
                    score_time = request.form.get(f'score_time_{row_index}')
                    if player_id and score_type and score_time:
                        result = MatchResult(
                            match_id=match_id,
                            team_id=Team.query.filter(Team.players.any(id=player_id)).first().id,
                            player_id=player_id,
                            score_time=score_time,
                            score_type=score_type,
                            season_id=season_id
                        )
                        db.session.add(result)

            db.session.commit()
            return redirect(url_for('update_result', season_id=season_id))

        # GET request: Render the page with matches and players
        matches = Match.query.filter_by(season_id=season_id).all()
        players = Player.query.all()

        return render_template('update_result.html', matches=matches, players=players, season_id=season_id)