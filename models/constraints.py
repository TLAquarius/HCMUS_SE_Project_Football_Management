from models import db, Rule, Season, Team, Player, Match, MatchSchedule,MatchResult, TeamRanking

def validate_match_schedule(match):
    # Ensure that each team plays only one game per round
    existing_matches = MatchSchedule.query.filter_by(round_number=match.round_number).all()
    for existing_match in existing_matches:
        if (existing_match.host_team_id == match.host_team_id or
                existing_match.guest_team_id == match.host_team_id or
                existing_match.host_team_id == match.guest_team_id or
                existing_match.guest_team_id == match.guest_team_id):
            raise ValueError("Team is already scheduled to play in this round.")

    # Ensure any pair of teams only meet twice with different roles
    meetings = Match.query.filter(
        (Match.host_team_id == match.host_team_id) &
        (Match.guest_team_id == match.guest_team_id) |
        (Match.host_team_id == match.guest_team_id) &
        (Match.guest_team_id == match.host_team_id)
    ).all()

    if len(meetings) >= 2:
        raise ValueError("Teams have already met twice in different roles.")

    return True
