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

    print("=== Email Configuration Debug ===")
    print("Available config keys:", list(current_app.config.keys()))
    
    # Use .get() method instead of direct key access to avoid KeyError
    smtp_server = current_app.config.get('SMTP_SERVER')
    smtp_port = current_app.config.get('SMTP_PORT')
    smtp_username = current_app.config.get('SMTP_USERNAME')
    smtp_password = current_app.config.get('SMTP_PASSWORD')
    default_sender = current_app.config.get('DEFAULT_SENDER')

    print(f"SMTP_SERVER: {smtp_server}")
    print(f"SMTP_PORT: {smtp_port}")
    print(f"SMTP_USERNAME: {smtp_username}")
    print(f"SMTP_PASSWORD: {'***' if smtp_password else 'NOT SET'}")
    print(f"DEFAULT_SENDER: {default_sender}")

    # Check if configuration is missing
    if not smtp_server:
        raise ValueError("SMTP_SERVER configuration is missing")
    if not smtp_port:
        raise ValueError("SMTP_PORT configuration is missing")
    if not smtp_username:
        raise ValueError("SMTP_USERNAME configuration is missing")
    if not smtp_password:
        raise ValueError("SMTP_PASSWORD configuration is missing")
    if not default_sender:
        raise ValueError("DEFAULT_SENDER configuration is missing")

    template = get_template_by_id(template_id)
    if not template:
        raise ValueError(f"Template with ID {template_id} not found.")
    
    body = template['body'].replace("{{tracking_url}}", tracking_url)

    msg = MIMEText(body, 'html')
    msg['Subject'] = template['subject']
    msg['From'] = default_sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(smtp_username, smtp_password)  # Log in to the SMTP server
            server.sendmail(msg['From'], [msg['To']], msg.as_string())  # Send the email
        print(f"[+] Email sent to {recipient} using template {template_id}")
    except Exception as e:
        current_app.logger.error(f"Error sending email to {recipient}: {e}")
        print(f"[-] Error sending email to {recipient}: {e}")

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