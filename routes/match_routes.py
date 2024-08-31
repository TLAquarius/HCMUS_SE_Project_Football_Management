from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Team, Match, Season, MatchResult, Player

def setup_match_routes(app):
    @app.route('/season/<int:season_id>/match_schedule', methods=['GET', 'POST'])
    def match_schedule(season_id):
        matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id).order_by(Match.round_number).all()
        return render_template('match_schedule.html', season_id=season_id, matches=matches)

    @app.route('/season/<int:season_id>/auto_schedule', methods=['GET'])
    def auto_schedule(season_id):
        teams = Team.query.filter_by(season_id=season_id).all()

        round = 1
        for i in range(len(teams)-1):
            if(Match.query.filter((Match.host_team_id == teams[i].id) | (Match.guest_team_id == teams[i].id)).count() == 2*len(teams)-2):
                continue
            for j in range(i + 1, len(teams)):
                if(Match.query.filter((Match.host_team_id == teams[i].id), (Match.guest_team_id == teams[j].id)).count() > 0):
                    continue
                match_num = 0
                while(True):
                    if(Match.query.filter(Match.round_number==round, 
                                          ((Match.host_team_id == teams[i].id) | (Match.guest_team_id == teams[j].id) | 
                                           (Match.host_team_id == teams[j].id) | (Match.guest_team_id == teams[i].id))).count() > 0):
                        round += 1
                        continue  
                    new_match = Match(round_number=round, match_datetime=datetime(2099, 12, 31), host_team_id=teams[i].id, guest_team_id=teams[j].id)
                    db.session.add(new_match)
                    match_num+=1
                    if(match_num<2):
                        i, j = j, i
                        continue
                    i, j = j, i
                    match_num = 0
                    round = 1
                    break

        db.session.commit()
        return match_schedule(season_id)

    @app.route('/season/<int:season_id>/save_match', methods=['POST'])
    def save_match(season_id):
        match_datetime = request.form['match_datetime']
        host_team = request.form['host_team_id']
        guest_team = request.form['guest_team_id']
        round_number = int(request.form['round_number'])
        
        match = Match.query.filter_by(host_team_id=host_team, guest_team_id=guest_team).first()
        if match:
            if match.round_number != round_number:
                message = ''
                if round_number<1:
                    message = 'Vòng đấu không hợp lệ! Hủy bỏ thay đổi.'
                if Match.query.filter(((Match.host_team_id == host_team) | (Match.guest_team_id == host_team)), Match.round_number == round_number).count() > 0:
                    message = 'Đội nhà đã có trận đấu tại vòng đó! Hủy bỏ thay đổi.'
                if Match.query.filter((Match.host_team_id == guest_team) | (Match.guest_team_id == guest_team), Match.round_number == round_number).count() > 0:
                    message = 'Đội khách đã có trận đấu tại vòng đó! Hủy bỏ thay đổi.'
                if message:
                    matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id).order_by(Match.round_number).all()
                    return render_template('match_schedule.html', season_id=season_id, matches=matches, round_error=message)
                match.round_number = round_number

            try:
                match.match_datetime = datetime.strptime(match_datetime, '%Y-%m-%dT%H:%M')
            except ValueError:
                message = "Ngày tháng không hợp lệ! Hủy bỏ thay đổi."
                matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id).order_by(Match.round_number).all()
                return render_template('match_schedule.html', season_id=season_id, matches=matches, time_error=message)
            db.session.commit()
        return redirect(url_for('match_schedule', season_id=season_id))

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