from flask import Flask, jsonify, request, send_from_directory, session
from config.config import Config
from extensions import db, bcrypt
from models.admin import Admin
from models.staff import Staff
import os
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from flask_login import LoginManager
from flask_cors import CORS


# Custom static folder for scripts


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "staff_login" 

    @login_manager.user_loader
    def load_user(user_id):
      role = session.get('role')
      if role == 'admin':
          return Admin.query.filter_by(id=int(user_id)).first()
      elif role == 'staff':
          return Staff.query.filter_by(id=int(user_id)).first()
      return None

    # Unauthorized handler
    def unauthorized_handler():
        if request.path.startswith('/admin'):
            login_manager.login_view = 'admin_login'
        else:
            login_manager.login_view = 'staff_login'
        return jsonify({"error": "Please log in"}), 401

    # Set the unauthorized handler
    login_manager.unauthorized_handler(unauthorized_handler)

    # Enable CORS
    CORS(app, origins=["http://127.0.0.1:3000", "http://192.168.1.15:3000"], supports_credentials=True)

    @app.route('/scripts/<path:filename>')
    def serve_scripts(filename):
        script_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'static', 'scripts')
        return send_from_directory(script_folder, filename)
    with app.app_context():
        db.create_all()  # Create tables

    # Register Blueprints (optional)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)