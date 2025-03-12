from flask import Blueprint, render_template, request, jsonify, Response, abort
import json
import uuid
import logging
from rq.job import Job
from redisStore import add_task_to_queue, get_redis_con

# Configure logger
logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)

# List of valid routes that should be handled
VALID_ROUTES = {
    "",  # root path
    "routes",
    "results",
    "star-feedback",
    "predict",
    "big-five-feedback",
}


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors.
    Returns a JSON response with error details.
    """
    logger.error(f"404 error: {error}")
    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "The requested resource was not found on the server.",
                "status_code": 404,
            }
        ),
        404,
    )


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors.
    Returns a JSON response with error details.
    """
    logger.error(f"500 error: {error}")
    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred on the server.",
                "status_code": 500,
            }
        ),
        500,
    )


@bp.app_errorhandler(Exception)
def handle_exception(error):
    """
    Handle all other unhandled exceptions.
    Returns a JSON response with error details.
    """
    logger.error(f"Unhandled exception: {error}")
    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": str(error),
                "status_code": 500,
            }
        ),
        500,
    )


def init_app(app):
    """
    Initialize the application with all routes.

    This function registers the blueprint with the provided Flask application,
    setting up all the routes defined in the blueprint.

    Args:
        app (Flask): The Flask application instance to which the blueprint will be registered.
    """
    app.register_blueprint(bp)


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def catch_all(path):
    """
    Catch-all route that either renders the index page for valid routes
    or returns a 404 error for invalid routes.

    Args:
        path (str): The path accessed by the user.

    Returns:
        Response: The rendered index.html template or 404 error.
    """
    # Split the path and check the first segment
    path_segment = path.split("/")[0] if path else ""

    if path_segment not in VALID_ROUTES:
        logger.warning(f"Invalid route accessed: {path}")
        abort(404)

    if path == "":
        path = "Home Route Accessed"

    logger.info(f"Route accessed: {path}")
    return render_template("index.html")


@bp.route("/api/routes", methods=["GET"])
def test():
    logger.info("Test route accessed")
    return render_template("index.html")


@bp.route("/results/<job_id>", methods=["GET"])
def get_results(job_id):
    """
    GET route that returns the results of a job.

    This endpoint fetches the results of a job from the Redis queue using the job ID.
    It checks the status of the job and returns the result if the job is finished.
    If the job is not found or not finished, it returns an appropriate message.

    Args:
        job_id (str): The unique identifier of the job.

    Returns:
        Response: A JSON response containing the job result if finished, or a message indicating the job status.
    """
    logger.info(f"Fetching results for job_id: {job_id}")
    # get connection
    conn = get_redis_con()

    try:
        # Try to fetch the job
        job = Job.fetch(job_id, connection=conn)
    except Exception as e:
        # If job_id doesn't exist, Job.fetch will raise an exception
        logger.warning(f"Job not found: {job_id}. Error: {str(e)}")
        return jsonify({"message": "Job not found.", "status": "error"}), 404

    if not job.is_finished:
        logger.info(f"Job is not finished yet: {job_id}")
        return jsonify({"message": "Job is not finished yet.", "status": "pending"})

    try:
        # get result
        result = job.result
        json_string = json.dumps(result)
        logger.info(f"Job finished successfully: {job_id}")
        return jsonify({"result": json.loads(json_string), "status": "success"})
    except Exception as e:
        logger.error(f"Error processing job result for job_id {job_id}: {str(e)}")
        return (
            jsonify(
                {
                    "message": "Error processing job result",
                    "error": str(e),
                    "status": "error",
                }
            ),
            500,
        )


@bp.route("/star-feedback", methods=["POST"])
def get_star_feedback():
    """
    POST route that processes STAR feedback.

    This endpoint receives JSON data from the request, enqueues a task to predict STAR scores,
    and returns the job ID of the enqueued task. The STAR method is used to evaluate the
    situation, task, action, and result in feedback.

    Returns:
        Response: A JSON response containing the job ID of the enqueued task for STAR feedback.
    """
    from ..tasks.starPredictions import predict_star_scores

    data = request.get_json()
    logger.info("Received data for STAR feedback")
    # Add task to queue
    job = add_task_to_queue(predict_star_scores, data)
    logger.info(f"Job enqueued for STAR feedback: {job.get_id()}")
    return jsonify(job.get_id())


@bp.route("/predict", methods=["POST"])
def predict() -> Response:
    """
    POST route that processes video predictions.

    This endpoint receives JSON data containing a video URL, enqueues a task to process the video,
    and subsequently enqueues another task to create an answer based on the processed video.
    It returns the job ID of the enqueued task for answer creation.

    Returns:
        Response: A JSON response containing the job ID of the enqueued task for answer creation.
    """
    # Function-level imports to avoid circular dependencies at module load time
    from ..tasks.videoProcess import output_video
    from ..tasks.score import create_answer

    req = request.get_json()
    logger.info("Received data for prediction")
    # get video url
    video_url = req.get("videoUrl")
    if not video_url:
        logger.warning("Required fields missing in prediction request")
        return jsonify(errors="Required fields missing.")
    # enqueue job
    process_video = add_task_to_queue(output_video, video_url)
    logger.info(f"Job enqueued for video processing: {process_video.get_id()}")
    content = {"fname": "output.mp4", "rename": str(uuid.uuid4()) + ".mp3"}
    # Add task to queue
    answer = add_task_to_queue(create_answer, content, depends_on=[process_video])
    logger.info(f"Job enqueued for answer creation: {answer.get_id()}")
    return jsonify(answer.get_id())


@bp.route("/big-five-feedback", methods=["POST"])
def get_big_five_feedback():
    """
    POST route that processes Big Five feedback.

    This endpoint receives JSON data from the request, enqueues a task to process Big Five scores,
    and returns the job ID of the enqueued task. The Big Five method is used to evaluate personality
    traits based on the feedback provided.

    Returns:
        Response: A JSON response containing the job ID of the enqueued task for Big Five feedback.
    """
    # Function-level import to avoid circular dependency at module load time
    from ..tasks.bigFiveScores import big_five_feedback

    data = request.get_json()
    logger.info("Received data for Big Five feedback")
    big_five = add_task_to_queue(big_five_feedback, data)
    logger.info(f"Job enqueued for Big Five feedback: {big_five.get_id()}")
    return jsonify(big_five.get_id())

