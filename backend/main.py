from flask import Flask
from config.config import Config
from models import db
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from extensions import bcrypt



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables

    # Register Blueprints (optional)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)