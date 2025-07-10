from flask import Flask

"""Initialize the Flask application"""
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'your-secret-key'  # Use a strong random key in production
                           
    from .routes import main
    app.register_blueprint(main)

    return app

"""
This file creates and configures a Flask app instance.

app.config.from_object('config.Config') loads the email server settings from config.py.

app.register_blueprint(main) imports your routes (URL handlers) from routes.py.

🧠 Why use this? This “factory” style makes your code more modular and testable — ideal for real-world or production use.
"""