"""
Main entry point for the backend application running dev server.
"""

from backend.server.app import app
from backend.utils import move_misplaced_files
from backend.utils.logger_config import get_logger 

logger = get_logger(__name__)

# Check for and move misplaced temporary files on startup
move_misplaced_files()

# Application server WSGI entry point
application = app

if __name__ == "__main__":
    # Only use Flask's development server when running directly
    # Run from command line with `gunicorn --bind 0.0.0.0:5000 --pythonpath /app backend.main:application`
    logger.info("Starting development server")
    app.run(debug=False, host="0.0.0.0", port=5000)

