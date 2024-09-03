from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Team, Match, Season, MatchResult, Player, ScoreType, TeamRanking

def setup_match_routes(app):
    @app.route('/season/<int:season_id>/match_schedule', methods=['GET', 'POST'])
    def match_schedule(season_id):
        finished_matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.isnot(None)).order_by(Match.round_number).all()
        matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.is_(None)).order_by(Match.round_number).all()
        return render_template('match_schedule.html', season_id=season_id, finished_matches=finished_matches, matches = matches)

    @app.route('/season/<int:season_id>/auto_schedule', methods=['GET'])
    def auto_schedule(season_id):
        finished_matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.isnot(None)).order_by(Match.round_number).all()
        if finished_matches:
            message = 'Giải đã bắt đầu, không thể khỏi tạo thêm trận đấu.'
            matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.is_(None)).order_by(Match.round_number).all()
            return render_template('match_schedule.html', season_id=season_id, finished_matches=finished_matches, matches = matches, match_error=message)
    
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
                    finished_matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.isnot(None)).order_by(Match.round_number).all()
                    matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.is_(None)).order_by(Match.round_number).all()
                    return render_template('match_schedule.html', season_id=season_id, finished_matches=finished_matches, matches=matches, round_error=message)
                match.round_number = round_number

            try:
                match.match_datetime = datetime.strptime(match_datetime, '%Y-%m-%dT%H:%M')
            except ValueError:
                message = "Ngày tháng không hợp lệ! Hủy bỏ thay đổi."
                finished_matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.isnot(None)).order_by(Match.round_number).all()
                matches = Match.query.join(Match.host_team).filter(Team.season_id == season_id, Match.host_score.is_(None)).order_by(Match.round_number).all()
                return render_template('match_schedule.html', season_id=season_id, finished_matches=finished_matches, matches=matches, time_error=message)
            db.session.commit()
        return redirect(url_for('match_schedule', season_id=season_id))

    @app.route('/season/<int:season_id>/update_result', methods=['GET', 'POST'])
    def update_result(season_id):
        if request.method == 'POST':
            # Get the match_id from the form
            match_id = request.form.get('match_id')

            # Step 1: Delete existing results for the given match_id
            MatchResult.query.filter_by(match_id=match_id).delete()
            db.session.commit()

            # Step 2: Collect new results from the form
            i = 0
            results = []
            while True:
                score_time = request.form.get(f'result[{i}][score_time]')
                team_id = request.form.get(f'result[{i}][team_id]')
                player_id = request.form.get(f'result[{i}][player_id]')
                score_type_id = request.form.get(f'result[{i}][score_type_id]')

                if score_time is None or team_id is None or player_id is None or score_type_id is None:
                # No more results
                    break

                # Create a new Result object and add it to the database
                new_result = MatchResult(
                    match_id=match_id,
                    score_time=score_time,
                    team_id=team_id,
                    player_id=player_id,
                    score_type_id=score_type_id
                )
                db.session.add(new_result)

                result = {
                    'match_id': match_id,
                    'score_time': score_time,
                    'team_id': team_id,
                    'player_id': player_id,
                    'score_type_id': score_type_id
                }
                results.append(result)
                i += 1

            # Commit the new results to the database
            db.session.commit()

            # Step 3: Update match scores
            match = Match.query.get(match_id)
            if match:
                match.update_match_score()

            match_teams = set()
            match_teams.add(match.host_team_id)
            match_teams.add(match.guest_team_id)

            player_ids_with_scores = {result['player_id'] for result in results}
            for player_id in player_ids_with_scores:
                player = Player.query.get(player_id)
                if player:
                    player.update_total_score()

            team_ids = db.session.query(Team.id).filter_by(season_id=season_id).all()
            for team_id in team_ids:
                team_ranking = TeamRanking.query.get(team_id[0])
                if not team_ranking:
                    TeamRanking.insert_default_value(team_id[0])

            # Step 4: Update team rankings and player score
            for team_id in match_teams:
                team_ranking = TeamRanking.query.get(team_id)
                players = Player.query.filter_by(team_id=team_id).all()

                for player in players:
                    player.update_total_score()

                if not team_ranking:
                    TeamRanking.insert_default_value(team_id)
                    team_ranking = TeamRanking.query.get(team_id)
                team_ranking.update_score()
                team_ranking.update_total_goals()
                team_ranking.update_points()

            TeamRanking.update_rankings(season_id)


        # GET request to fetch match details and results

        # Handle the main page with match search/filter options
        team_name = request.args.get('team_name')
        round_number = request.args.get('round_number')
        match_date = request.args.get('match_date')

        matches_query = Match.query.join(Team, Match.host_team_id == Team.id) \
            .filter(Team.season_id == season_id)

        if team_name:
            matches_query = matches_query.filter(
                Team.name.ilike(f'%{team_name}%') |
                Match.guest_team.has(Team.name.ilike(f'%{team_name}%'))
            )

        if round_number:
            matches_query = matches_query.filter(Match.round_number == round_number)

        if match_date:
            matches_query = matches_query.filter(db.func.date(Match.match_datetime) == match_date)

        matches = matches_query.all()
        score_types = ScoreType.query.filter_by(season_id=season_id).all()
        match_ids = [match.id for match in matches]
        results = MatchResult.query.filter(MatchResult.match_id.in_(match_ids)).all()

        players = Player.query.filter(Player.team_id.in_(
            [team.id for team in Team.query.filter_by(season_id=season_id).all()]
        )).all()
        season = Season.query.get(season_id)
        rule = season.rule

        return render_template('update_result.html', matches=matches, players=players, season_id=season_id,results=results,score_types=score_types,maximum_score_time=rule.maximum_score_time)
