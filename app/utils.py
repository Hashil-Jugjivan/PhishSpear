"""Utility function for sending emails"""

from flask import current_app
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import json
import uuid
import csv
import os

def load_templates():
    """Loads and parses the JSON file to return a list of templates."""

    try:
        with open('campaigns/templates.json', encoding = 'utf-8') as file:
            templates = json.load(file)
        return templates
    except FileNotFoundError:
        current_app.logger.error("Templates file not found.")
        return []
    except json.JSONDecodeError:
        current_app.logger.error("Error decoding JSON from templates file.")
        return []

def get_template_by_id(template_id: str):
    """Fetches a template by its ID from the loaded templates."""
    
    templates = load_templates()
    return next((t for t in templates if t['id'] == template_id), None)

def send_phishing_email(recipient: str, template_id: str, tracking_url: str):
    """Sends a phishing email using the specified template and tracking URL"""

    template = get_template_by_id(template_id)
    if not template:
        raise ValueError(f"Template with ID {template_id} not found.")
    
    body = template['body'].replace("{{tracking_url}}", tracking_url)

    msg = MIMEText(body, 'html')
    msg['Subject'] = template['subject']
    print("Flask Config DEFAULT_SENDER:", current_app.config.get('DEFAULT_SENDER'))
    msg['From'] = current_app.config['DEFAULT_SENDER']
    print(f"DEBUG: msg['From'] = {msg['From']}")
    print(f"DEBUG: config DEFAULT_SENDER = {current_app.config['DEFAULT_SENDER']}")
    msg['To'] = recipient

    with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
        server.starttls() # Upgrade to secure connection
        server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD']) # Log in to the SMTP server
        print(f"Sending email from: {msg['From']} to: {msg['To']}")
        server.sendmail(msg['From'], [msg['To']], msg.as_string()) # Send the email

    print(f"[+] Email sent to {recipient} using template {template_id}")

def generate_uid():
    """Generates a unique identifier for the user."""
    return uuid.uuid4().hex[:10] # 10-character unique ID

def log_interaction(user_id: str, email: str = None, password: str = None, action: str = "clicked"):
  """
  Logs user interactions with the phishing email, such as clicking a link or entering credentials.
  """  

  log_path = 'campaigns/logs/campaign_log.csv'
  os.makedirs(os.path.dirname(log_path), exist_ok=True)

  with open(log_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        datetime.now().isoformat(),
        user_id,
        action,
        email if email else "",
        password if password else ""
        ])

    print(f"[+] Logged {action} for UID={user_id}")


"""
Loads the correct template using its ID
Replaces {{tracking_link}} in the email body with the real URL
Builds an HTML email message using MIMEText
Connects to the SMTP server (e.g., Mailtrap or Gmail)
Logs in and sends the email securely
Prints a success message
"""