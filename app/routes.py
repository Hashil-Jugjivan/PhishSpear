""" Handle web routes for the application (URLs)"""

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models import db, Campaign, User, Interaction
from app.utils import send_phishing_email, log_interaction, generate_uid, load_templates
from urllib.parse import quote, unquote

# Specify the template folder for the Blueprint
main = Blueprint('main', __name__, template_folder='templates') 

@main.route('/')
def home():
    templates = load_templates()
    return render_template('landing.html', templates=templates)

@main.route('/dashboard')
def dashboard():
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to view the dashboard.")
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.login'))

    campaigns = Campaign.query.filter_by(user_id=user.id).all()

    campaign_data = []
    for c in campaigns:
        clicks = [i for i in c.interactions if i.action == "clicked"]
        submissions = [i for i in c.interactions if i.action == "submitted"]
        campaign_data.append({
            "recipient": c.recipient_email,
            "template": c.template_id,
            "uid": c.uid,
            "clicks": len(clicks),
            "submissions": len(submissions),
            "submitted_email": submissions[0].submitted_email if submissions else None,
            "submitted_password": submissions[0].submitted_password if submissions else None,
        })

    return render_template("dashboard.html", campaigns=campaign_data)


@main.route('/send_email', methods=['POST'])
def send_email():
    if 'user_id' not in session:
        flash("You must be logged in to send emails.")
        return redirect(url_for('auth.login'))

    to_email = request.form.get('to')
    template_id = request.form.get('template_id', 'office365_security')

    if not to_email:
        flash("No recipient specified.")
        return redirect(url_for('main.home'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User session invalid.")
        return redirect(url_for('auth.login'))

    uid = generate_uid()
    tracking_url = f"http://localhost:5000/phish_login?uid={uid}"

    campaign = Campaign(
        recipient_email=to_email,
        template_id=template_id,
        tracking_url=tracking_url,
        uid=uid,
        user=user
    )

    db.session.add(campaign)
    db.session.commit()

    send_phishing_email(to_email, template_id, tracking_url)

    flash(f"Email sent to {to_email}")
    return redirect(url_for('main.home'))

@main.route('/phish_login', methods=['GET', 'POST'])
def phishing_login():
    uid = request.args.get('uid') or request.form.get('uid')
    campaign = Campaign.query.filter_by(uid=uid).first()

    if not campaign:
        return "Invalid or expired link."

    if request.method == 'GET':
        db.session.add(Interaction(campaign=campaign, action="clicked"))
        db.session.commit()
        return render_template('phishing_login.html', uid=uid)

    email = request.form.get('email')
    password = request.form.get('password')
    db.session.add(Interaction(
        campaign=campaign,
        action="submitted",
        submitted_email=email,
        submitted_password=password
    ))
    db.session.commit()

    return "Thank you for verifying. You may close this tab."


@main.route('/admin/report')
def admin_report():
    if 'user_id' not in session:
        flash("You must be logged in to view the report.")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User session invalid.")
        return redirect(url_for('auth.login'))

    campaigns = Campaign.query.filter_by(user=user).all()

    report = []
    for c in campaigns:
        clicks = [i for i in c.interactions if i.action == "clicked"]
        submissions = [i for i in c.interactions if i.action == "submitted"]
        report.append({
            "uid": c.uid,
            "target": c.recipient_email,
            "template": c.template_id,
            "clicks": len(clicks),
            "submissions": len(submissions),
            "submitted_email": submissions[0].submitted_email if submissions else None,
            "submitted_password": submissions[0].submitted_password if submissions else None,
        })

    return render_template("report.html", campaigns=report)


"""
Defines the / route. When you visit http://localhost:5000, you will see this message.

We use a Blueprint, which is Flasks way of organizing routes cleanly when the app gets bigger.
"""

