import pytest
from backend.tasks.starPredictions import predict_star_scores
from enum import Enum


class StarScore(Enum):
    ACTION = "Action"
    RESULT = "Result"
    SITUATION = "Situation"
    TASK = "Task"


def test_predict_star_scores():
    # Replace with your input data.
    input_data = {"text": "I hope this is an Action sentence."}
    expected_score = StarScore.TASK  # Replace with the actual expected score
    result = predict_star_scores(input_data)
    result = result["classifications"][0][1]
    assert (
        result == expected_score.value
    ), f"Expected {expected_score.value}, got {result}"
