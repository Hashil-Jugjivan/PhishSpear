"""Entry point to start the Flask web application"""

from flask import Flask
from app.routes import main
from app.models import db
from app.auth import auth

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishspear.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


"""
This is the main Python file you run to start the application.

create_app() is a function (in __init__.py) that sets up the Flask app.

app.run(debug=True) starts the Flask server on localhost:5000, and enables debug mode so you can see errors in the browser while developing.
"""

#/send_email?to=test@example.com
# 2e19a05cd813a4484b5e81797ca8ded5

