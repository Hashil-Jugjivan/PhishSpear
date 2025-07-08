"""Entry point to start the Flask web application"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

"""
This is the main Python file you run to start the application.

create_app() is a function (in __init__.py) that sets up the Flask app.

app.run(debug=True) starts the Flask server on localhost:5000, and enables debug mode so you can see errors in the browser while developing.
"""

#/send_email?to=test@example.com
# 2e19a05cd813a4484b5e81797ca8ded5