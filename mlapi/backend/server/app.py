"""
Initializes the Flask application for the development server in `backend/main.py`
"""
# Import Flask application factory
from . import create_app
# Create Flask application
app = create_app()
# Expose for WSGI servers like gunicorn
application = app
if __name__ == "__main__":
    # Only use Flask's development server when running directly
    app.run(debug=False, host="0.0.0.0", port=5000)

