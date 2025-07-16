from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from pathlib import Path
 
# Load environment variables FIRST, before anything else
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
    app = Flask(__name__)

    print("=== OS ENVIRONMENT ===")
    for k in ["SMTP_SERVER", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "DEFAULT_SENDER"]:
        print(f"{k}: {os.environ.get(k)}")
    
    # Configure the app directly with environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///phishspear.db')
    app.config['SMTP_SERVER'] = os.getenv('SMTP_SERVER', 'sandbox.smtp.mailtrap.io')
    app.config['SMTP_PORT'] = int(os.getenv('SMTP_PORT', 587))
    app.config['SMTP_USERNAME'] = os.getenv('SMTP_USERNAME', '')
    app.config['SMTP_PASSWORD'] = os.getenv('SMTP_PASSWORD', '')
    app.config['DEFAULT_SENDER'] = os.getenv('DEFAULT_SENDER', 'noreply@awareness.local')
    
    # Debug: Print configuration to verify it's loaded
    print("=== Flask App Configuration ===")
    print(f"SMTP_SERVER: {app.config.get('SMTP_SERVER')}")
    print(f"SMTP_PORT: {app.config.get('SMTP_PORT')}")
    print(f"SMTP_USERNAME: {app.config.get('SMTP_USERNAME')}")
    print(f"SMTP_PASSWORD: {'***' if app.config.get('SMTP_PASSWORD') else 'NOT SET'}")
    print(f"DEFAULT_SENDER: {app.config.get('DEFAULT_SENDER')}")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    from .models import User  # Import User model

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # Import and register blueprints
    from .models import User  # Import User model
    from .routes import main  # Import main routes
    from .auth import auth    # Import authentication routes

    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

