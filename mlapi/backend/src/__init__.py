from flask import Flask
from threading import Thread
from .db_monitor import poll_connection, get_redis_con
from .routes import init_app

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.template_folder = "templates"


# Background polling script
def _launch_polling_script():
    """Launches the polling script in a different thread."""
    Thread(target=poll_connection, args=(get_redis_con(),), daemon=True).start()
    print("Launched polling script in a separate thread.")


with app.app_context():
    _launch_polling_script()

init_app(app)


@app.route("/", methods=["GET"])
def index():
    """
    Home route.
    """
    return "Welcome to the ML API for Digital Coach"
