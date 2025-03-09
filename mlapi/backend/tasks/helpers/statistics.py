from nltk.parse import earleychart
import numpy as np
from .av_processing import build_timeline_interval_facial
from heapq import nlargest
from .rubric import (
    AUDIO_EMOTION_POINTS,
    AV_ASSOCIATIONS,
    FACIAL_EMOTION_POINTS,
    OVERAL_FACIAL_POINTS,
    OVERALL_AUDIO_POINTS,
)


def calculate_overall_facial_sentiment(facial_data):
    """
    It takes in a dictionary of facial data, and returns the emotion with the highest sum

    :param facial_data: a dictionary containing the following keys:
    :return: The emotion with the highest sum.
    """
    emotion_sums = dict(facial_data["emotion_sums"])
    return max(emotion_sums, key=lambda key: emotion_sums[key])


def calculate_overall_audio_sentiment(audio_data):
    """
    It takes a list of dictionaries, each of which has a key called "sentiment" and a value that is
    either "positive", "negative", or "neutral". It returns the most common value of "sentiment" in the
    list

    :param audio_data: the audio data that you want to analyze
    :return: The most common sentiment in the list of sentiments.
    """
    sentiments = audio_data["sentiment_analysis"]
    sent_list = [i["sentiment"] for i in sentiments]
    counted_sents = max(set(sent_list), key=sent_list.count)
    return counted_sents


def grab_top_five_keywords(audio_data):
    """
    It takes the audio data from the Watson API and returns the top five keywords

    :param audio_data: the JSON data returned from the API
    :return: A list of the top five keywords
    """
    keywords = audio_data["highlights"]
    top_five = nlargest(5, keywords, key=lambda item: item["rank"])
    return top_five


def calculate_top_three_facial_with_count(facial_data):
    """
    It takes a list of facial data, builds a timeline interval, gets the emotions per interval, gets the
    frequency distribution of the emotions per interval, gets the top three emotions, and then returns
    the top three emotions, the top emotion's frequency, the second emotion's frequency, and the third
    emotion's frequency

    :param facial_data: a list of dictionaries, each dictionary containing the following keys:
    :return: The top three emotions, and the percentage of time spent in each of the top three emotions.
    """
    timeline_interval = build_timeline_interval_facial(facial_data)
    emotions_per_interval = list(timeline_interval.values())
    fdist = dict(zip(*np.unique(emotions_per_interval, return_counts=True)))
    top_three = sorted(fdist, key=lambda k: int(fdist[k]), reverse=True)[:3]
    if len(top_three) < 3:
        iterations = 3 - len(top_three)
        for _ in range(iterations):
            top_three.append("N/A")
        fdist["N/A"] = 0.0
    top_three_with_count = [
        (top_three[0], fdist[top_three[0]]),
        (top_three[1], fdist[top_three[1]]),
        (top_three[2], fdist[top_three[2]]),
    ]
    denominator = (
        top_three_with_count[0][1]
        + top_three_with_count[1][1]
        + top_three_with_count[2][1]
    )
    top_stat = top_three_with_count[0][1] / denominator
    second_stat = top_three_with_count[1][1] / denominator
    third_stat = top_three_with_count[2][1] / denominator
    return top_three, top_stat, second_stat, third_stat


def _compute_av_sentiment_matches(timeline):
    """
    > For each entry in the timeline, if the facial emotion matches the audio sentiment, add 2 points.
    If only one of the facial emotions matches the audio sentiment, add 1 point. Then, divide the total
    points by the total possible points (2 points per entry) and multiply by 30 to get the final score

    :param timeline: the timeline of the video
    :return: the percentage of matches between the audio and visual sentiment.
    """
    total_pts = len(timeline) * 2
    pts = 0
    for entry in timeline:
        if (
            entry["facialEmotion"][0] in AV_ASSOCIATIONS[entry["audioSentiment"]]
            and entry["facialEmotion"][1] in AV_ASSOCIATIONS[entry["audioSentiment"]]
        ):
            pts += 2
        elif (
            entry["facialEmotion"][0] in AV_ASSOCIATIONS[entry["audioSentiment"]]
            and entry["facialEmotion"][1]
            not in AV_ASSOCIATIONS[entry["audioSentiment"]]
        ):
            pts += 1
        elif (
            entry["facialEmotion"][0] not in AV_ASSOCIATIONS[entry["audioSentiment"]]
            and entry["facialEmotion"][1] in AV_ASSOCIATIONS[entry["audioSentiment"]]
        ):
            pts += 1
        else:
            continue
    av_matches = (pts / total_pts) * 30
    return av_matches


def _compute_pts_for_emotion_occurences(timeline):
    """
    It takes a list of dictionaries, each dictionary containing a facial emotion and an audio sentiment,
    and returns a number between 0 and 10, where 0 is the worst and 10 is the best

    :param timeline: the timeline of the video
    :return: the percentage of the total points that the user has earned.
    """
    total_pts = len(timeline) * 6
    pts = 0
    for entry in timeline:
        pts += AUDIO_EMOTION_POINTS[entry["audioSentiment"]]
        pts += (
            FACIAL_EMOTION_POINTS[entry["facialEmotion"][0]]
            + FACIAL_EMOTION_POINTS[entry["facialEmotion"][1]]
        )

    if pts <= 0:
        return 0
    return (pts / total_pts) * 10


def compute_aggregate_score(result):
    """
    It takes the result of the API call and computes the aggregate score based on the following:

    - Text score: 40% of the text score
    - Overall facial emotion: the points associated with the overall facial emotion
    - Overall audio sentiment: the points associated with the overall audio sentiment
    - Average sentiment matches: the average sentiment matches
    - Emotion occurences: the points associated with the emotion occurences

    The aggregate score is then rounded to 2 decimal places

    :param result: The JSON response from the API
    :return: The aggregate score is being returned.
    """
    text_score = 40
    overall_facial = OVERAL_FACIAL_POINTS[result["overallFacialEmotion"]]
    overall_audio = OVERALL_AUDIO_POINTS[result["overallSentiment"]]
    av_matches = _compute_av_sentiment_matches(result["timeline"])
    emotion_occurences = _compute_pts_for_emotion_occurences(result["timeline"])
    print(text_score, overall_facial, overall_audio, av_matches, emotion_occurences)
    aggregate = (
        text_score + overall_facial + overall_audio + av_matches + emotion_occurences
    )
    return round(aggregate, 2)
