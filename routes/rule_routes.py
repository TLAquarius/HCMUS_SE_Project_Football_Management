from flask import render_template, request, redirect, url_for
from models import db, Rule

def setup_rule_routes(app):
    @app.route('/rule_change', methods=['GET', 'POST'])
    def rule_change():
        if request.method == 'POST':
            # Get data from the form
            min_players = request.form.get('minimum_players')
            max_players = request.form.get('maximum_players')
            min_age = request.form.get('minimum_age')
            max_age = request.form.get('maximum_age')
            max_foreign_players = request.form.get('maximum_foreign_players')
            max_match_time = request.form.get('maximum_score_time')
            win_points = request.form.get('win_point')
            draw_points = request.form.get('draw_point')
            lose_points = request.form.get('lose_point')

            # Get ranking priorities
            priority1 = request.form.get('priority1')
            priority2 = request.form.get('priority2')
            priority3 = request.form.get('priority3')
            priority4 = request.form.get('priority4')

            # Create or update the rule
            new_rule = Rule(
                minimum_players=min_players,
                maximum_players=max_players,
                minimum_age=min_age,
                maximum_age=max_age,
                maximum_foreign_players=max_foreign_players,
                maximum_score_time=max_match_time,
                win_point=win_points,
                draw_point=draw_points,
                lose_point=lose_points,
                priority1=priority1,
                priority2=priority2,
                priority3=priority3,
                priority4=priority4
            )

            db.session.add(new_rule)
            db.session.commit()

        rule = Rule.query.order_by(Rule.id.desc()).first() or Rule()
        return render_template('rule_change.html', rule=rule)
