from flask import Flask

def setup_routes(app):
    from .home_routes import setup_home_routes
    from .season_routes import setup_season_routes
    from .team_routes import setup_team_routes
    from .rule_routes import setup_rule_routes
    from .player_routes import setup_player_routes

    setup_home_routes(app)
    setup_season_routes(app)
    setup_team_routes(app)
    setup_rule_routes(app)
    setup_player_routes(app)