from flask import Flask
from threading import Thread
import logging
from backend.redisStore.myConnection import get_redis_con

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)
# Set JSON_AS_ASCII to False to allow UTF-8 encoding in JSON responses
app.config["JSON_AS_ASCII"] = False


def create_app():
    """
    Factory function to create and configure the Flask application
    """
    from redisStore.monitor import poll_connection
    from .routes import init_app
    init_app(app)
    def _launch_polling_script():
        """Launches the polling script in a different thread."""
        Thread(target=poll_connection, args=(get_redis_con(),), daemon=True).start()
        logger.info("Launched Redis polling script in a separate thread.")
    with app.app_context():
        _launch_polling_script()
    return app

