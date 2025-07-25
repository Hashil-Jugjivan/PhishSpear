"""This file contains configuration settings for the Flask application."""

from dotenv import load_dotenv
import os

# Load .env from the same folder as this script, explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path) # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///phishspear.db')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    DEFAULT_SENDER = os.getenv('DEFAULT_SENDER', 'noreply@awareness.local')

    