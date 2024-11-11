"""
Main Flask application as well as routes of the app.
"""
import uuid
import redis
from threading import Thread
from rq import Queue
from flask import Flask, jsonify, request
from flask_cors import CORS
from helpers.download_url import download_video_link
from helpers.score import create_answer
from db_monitor import poll_connection

from models.BigFiveScores import BigFiveScores

# initalize the Flask object
app = Flask(__name__)
CORS(app)
r = redis.Redis()
q = Queue(connection=r)


@app.before_first_request
def launch_polling_script():
    Thread(target=poll_connection, args=(r,), daemon=True).start()
    print("Launched polling script in different thread.")

@app.route("/predict", methods=["POST"])
def predict():
    """
    POST route that returns total text, audio and video predictions.
    """
    req = request.get_json()
    print(req);
	# video_url, user_id, interview_id, question_id, answer_id = (
    #     req["videoUrl"],
    #     req["userId"],
    #     req["interviewId"],
    #     req["questionId"],
    #     req["answerId"],
    # )
    # if (
    #     not video_url
    #     or not user_id
    #     or not interview_id
    #     or not question_id
    #     or not answer_id
    # ):
    #     return jsonify(errors="Required fields not in request body.")
    # print(video_url)
    # download = download_video_link(video_url)
    # print('download successful!!')
    # if "errors" in download:
    #     return jsonify(message="Download failed.", errors=str(download["errors"]))

    content = {
        "fname": "video.mp4",
        "rename": str(uuid.uuid4()) + ".mp3",
        # "user_id": user_id,
        # "interview_id": interview_id,
        # "question_id": question_id,
        # "answer_id": answer_id,
    }
    job = q.enqueue(create_answer, content)
    message = "Task " + str(job.id) + " added to queue at " + str(job.enqueued_at) + "."
    return jsonify(message=message)

@app.route('/big-five-feedback', methods=['POST'])
def get_big_five_feedback():
    data = request.get_json()
    big_five = BigFiveScores(
        data['big_five']['o'],
        data['big_five']['c'],
        data['big_five']['e'],
        data['big_five']['a'],
        data['big_five']['n']
    )

    user_feedback = []

    # Ensure the correct mapping of traits to their attributes
    for trait, attr in zip(['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'], ['o', 'c', 'e', 'a', 'n']):
        trait_level = big_five.determine_level(getattr(big_five, attr))
        user_feedback.append(BigFiveScores.FEEDBACK[trait][trait_level])
        

    return jsonify({'feedback': user_feedback})


@app.route("/", methods=["GET"])
def index():
    """
    Home route.
    """
    return "Welcome to the ML API for Digital Coach"


if __name__ == "___main__":
    app.run(debug=True, host="0.0.0.0")
