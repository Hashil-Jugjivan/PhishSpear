""" Handle web routes for the application (URLs)"""

from flask import Blueprint, request
from app.utils import send_phishing_email

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "PhishSpear Backend Running!"

@main.route('/send_email')
def test_email():
    email = request.args.get('to')
    if not email:
        return "Please specify ?to=email@example.com", 400

    tracking_url = f"http://localhost:5000/login?uid=test123"
    send_phishing_email(email, 'cred_harvest', tracking_url)
    return "Email sent!"


"""
Defines the / route. When you visit http://localhost:5000, you will see this message.

We use a Blueprint, which is Flasks way of organizing routes cleanly when the app gets bigger.
"""