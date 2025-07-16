from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uid():
    return uuid.uuid4().hex[:16]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    campaigns = db.relationship("Campaign", backref="user", lazy=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(32), default=generate_uid, unique=True)
    recipient_email = db.Column(db.String(150), nullable=False)
    template_id = db.Column(db.String(50), nullable=False)
    tracking_url = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interactions = db.relationship('Interaction', backref='campaign', lazy=True)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(20))  # clicked / submitted
    submitted_email = db.Column(db.String(150))
    submitted_password = db.Column(db.String(150))
