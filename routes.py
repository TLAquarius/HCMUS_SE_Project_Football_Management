from flask import render_template, request, redirect, url_for, abort
from models import db,Rule, Season, Team, Player, Match, MatchResult, MatchSchedule, TeamRanking

def setup_routes(app):
    @app.route('/')
    def main_page():
        # Fetch any necessary data for the main page
        # For example, seasons or other entities
        # seasons = Season.query.all()  # Example if you need to pass data
        return render_template('index.html')  # Render the main page template

    @app.route('/season/<int:season_id>')
    def season_page(season_id):
        season = Season.query.get(season_id)
        if season is None:
            abort(404)  # Return a 404 error if the season is not found
        return render_template('season.html', season=season)

    @app.route('/add-season', methods=['GET', 'POST'])
    def add_season():
        if request.method == 'POST':
            season_name = request.form['season_name']
            new_season = Season(name=season_name)
            db.session.add(new_season)
            db.session.commit()
            return redirect(url_for('home'))  # Adjust the 'home' endpoint to your main page route
        return render_template('add_season.html')