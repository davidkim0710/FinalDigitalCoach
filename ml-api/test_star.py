from models.StarMethod import predict_star_scores


def test_star_predict():
    """
    Tests the star predict function by calling it from hugging face
    returns:
    {
    [{'label': 'LABEL_3', 'score': 0.8075820207595825}]
    {'fufilledStar': False, 'percentages': {'action': 0.0, 'result': 0.0, 'situation': 0.0, 'task': 100.0}, 'classifications': [['This is supposed to be an action sentence', 'Task']]}
    }
    """
    data = {"text": "I completed some fixes for the backend project"}
    star_scores = predict_star_scores(data)
    print(star_scores)


if __name__ == "__main__":
    test_star_predict()
