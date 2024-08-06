from flask import render_template
from models import Season

def setup_home_routes(app):
    @app.route('/')
    def home():
        seasons = Season.query.all()
        return render_template('index.html', seasons=seasons)
