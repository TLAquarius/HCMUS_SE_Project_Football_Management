from flask import Flask

def setup_routes(app):
    from .home_routes import setup_home_routes
    from .season_routes import setup_season_routes
    from .team_routes import setup_team_routes

    setup_home_routes(app)
    setup_season_routes(app)
    setup_team_routes(app)