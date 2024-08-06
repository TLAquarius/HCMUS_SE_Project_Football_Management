from flask import render_template, request, redirect, url_for
from models import db, Rule

def setup_rule_routes(app):
    @app.route('/rule-change', methods=['GET', 'POST'])
    def rule_change():
        if request.method == 'POST':
            # Get data from the form
            min_players = request.form.get('min_players')
            max_players = request.form.get('max_players')
            min_age = request.form.get('min_age')
            max_age = request.form.get('max_age')
            max_foreign_players = request.form.get('max_foreign_players')
            max_score_type = request.form.get('max_score_type')
            min_match_time = request.form.get('min_match_time')
            max_match_time = request.form.get('max_match_time')
            win_points = request.form.get('win_points')
            draw_points = request.form.get('draw_points')
            lose_points = request.form.get('lose_points')

            # Create a new rule
            new_rule = Rule(
                min_players=min_players,
                max_players=max_players,
                min_age=min_age,
                max_age=max_age,
                max_foreign_players=max_foreign_players,
                max_score_type=max_score_type,
                min_match_time=min_match_time,
                max_match_time=max_match_time,
                win_points=win_points,
                draw_points=draw_points,
                lose_points=lose_points
            )

            db.session.add(new_rule)
            db.session.commit()

            return redirect(url_for('home'))

        return render_template('rule_change.html')
