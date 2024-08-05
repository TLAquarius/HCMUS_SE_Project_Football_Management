from sqlalchemy import event
from models import db,Rule, Season, Team, Player, Match, MatchResult, TeamRanking

# Event listener for after a Player is inserted
@event.listens_for(Player, 'after_insert')
@event.listens_for(Player, 'before_delete')
def update_team_player_count_after_insert(mapper, connection, target):
    team = Team.query.get(target.team_id)
    if team:
        team.national_players_count = Player.query.filter_by(team_id=team.id, player_type='national').count()
        team.foreign_players_count = Player.query.filter_by(team_id=team.id, player_type='foreign').count()
        db.session.commit()

def update_team_ranking(match_id):
    match = Match.query.get(match_id)
    if not match:
        return

    host_team_id = match.host_team_id
    guest_team_id = match.guest_team_id
    host_score = match.host_score
    guest_score = match.guest_score

    # Update host team ranking
    host_ranking = TeamRanking.query.filter_by(team_id=host_team_id).first()
    guest_ranking = TeamRanking.query.filter_by(team_id=guest_team_id).first()
    if host_ranking:
        if host_score > guest_score:
            host_ranking.total_wins += 1
            guest_ranking.total_losses += 1
        elif host_score < guest_score:
            host_ranking.total_losses += 1
            guest_ranking.total_wins += 1
        else:
            host_ranking.total_draws += 1
            guest_ranking.total_draws += 1
        host_ranking.win_loss_difference = host_ranking.total_wins - host_ranking.total_losses
        guest_ranking.win_loss_difference = guest_ranking.total_wins - guest_ranking.total_losses
        db.session.commit()

# Event listener for after a Match is inserted
@event.listens_for(Match, 'after_insert')
@event.listens_for(Match, 'after_update')
@event.listens_for(Match, 'after_delete')
def update_team_point(mapper, connection, target):
    update_team_ranking(target.id)


def update_player_scores(match_id):
    match_results = MatchResult.query.filter_by(match_id=match_id).all()

    # Collect scores to update
    scores = {}
    for result in match_results:
        player_id = result.player_id
        if player_id:
            if player_id not in scores:
                scores[player_id] = 0
            scores[player_id] += 1
            # Add more conditions as needed

    # Perform bulk update
    for player_id, total_score in scores.items():
        db.session.query(Player).filter_by(id=player_id).update({Player.total_score: total_score})

    db.session.commit()


@event.listens_for(MatchResult, 'after_insert')
@event.listens_for(MatchResult, 'after_update')
@event.listens_for(MatchResult, 'before_delete')
def handle_match_result_change(mapper, connection, target):
    update_player_scores(target.match_id)


def update_match_scores(match_id):
    match = Match.query.get(match_id)
    if match:
        # Initialize scores
        host_score = 0
        guest_score = 0

        # Get all match results for the given match
        match_results = MatchResult.query.filter_by(match_id=match_id).all()

        # Calculate the scores based on match results
        for result in match_results:
            if result.team_id == match.host_team_id:
                host_score += 1
            elif result.team_id == match.guest_team_id:
                guest_score += 1


        # Update the match scores
        match.host_score = host_score
        match.guest_score = guest_score
        db.session.commit()