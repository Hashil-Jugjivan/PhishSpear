""" Handle web routes for the application (URLs)"""

from flask import Blueprint, request, render_template
from app.utils import send_phishing_email, log_interaction, generate_uid
from urllib.parse import quote, unquote
from collections import defaultdict
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

@main.route('/admin/report')
def admin_report():
   # Load uid_map.csv to get UID to target email mapping
    uid_to_target = {}
    try:
        with open("campaigns/logs/uid_map.csv", newline='') as f:
            for row in csv.reader(f):
                if len(row) >= 2:
                    uid_to_target[row[0]] = row[1]
    except FileNotFoundError:
        uid_to_target = {}

    # Collect user data from campaign_log.csv
    user_data = defaultdict(lambda: {"target": "", "clicked": False, "submitted_email": None, "submitted_password": None, "logs": []})

    try:
        with open("campaigns/logs/campaign_log.csv", newline='') as f:
            for row in csv.reader(f):
                if len(row) < 3:
                    continue

                timestamp, uid, action = row[:3]
                email = row[3] if len(row) > 3 else ""
                password = row[4] if len(row) > 4 else ""

                user = user_data[uid]
                user["target"] = uid_to_target.get(uid, "Unknown")
                user["logs"].append((timestamp, action, email))

                if action == "clicked":
                    user["clicked"] = True
                elif action == "submitted":
                    user["submitted_email"] = email
                    user["submitted_password"] = password
    except FileNotFoundError:
        pass

    return render_template("report.html", user_data=user_data)

"""
Defines the / route. When you visit http://localhost:5000, you will see this message.

We use a Blueprint, which is Flasks way of organizing routes cleanly when the app gets bigger.
"""