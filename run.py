"""Entry point to start the Flask web application"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    
#/send_email?to=test@example.com
# 2e19a05cd813a4484b5e81797ca8ded5

