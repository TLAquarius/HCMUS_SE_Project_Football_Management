from flask import Flask
from models import db

def create_app(test_config=None):
    app = Flask(__name__)

    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = False

    # Apply test configuration if provided
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Import and register routes
    from routes import setup_routes
    setup_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
