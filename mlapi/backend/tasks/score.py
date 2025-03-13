from .helpers.av_processing import av_timeline_resolution
from .helpers.statistics import (
    calculate_top_three_facial_with_count,
    compute_aggregate_score,
    calculate_overall_audio_sentiment,
    grab_top_five_keywords,
)
from .helpers.score_helpers import (
    score_audio,
    score_facial,
    score_text_structure,
    score_bigFive,
    map_bigfive_to_competencies,
)
from .helpers.competency_analysis import generate_competency_feedback
from rq.decorators import job
from backend.redisStore.myConnection import get_redis_con


@job("default", connection=get_redis_con())
def create_answer(content):
    """
    Creates feedback answer. 
    """
    facial_answer = score_facial(content)
    audio_answer = score_audio(content)

    text_answer = score_text_structure(audio_answer)
    timeline = av_timeline_resolution(
        audio_answer["clip_length_seconds"],
        facial_answer,
        audio_answer["sentiment_analysis"],
    )
    (
        facial_stats,
        top_stat,
        second_stat,
        third_stat,
    ) = calculate_top_three_facial_with_count(facial_answer)

    bigFive = score_bigFive(audio_answer, facial_stats, text_answer)

    competency_feedback = generate_competency_feedback(
        facial_answer, audio_answer, text_answer
    )

    bigfive_derived_competencies = map_bigfive_to_competencies(bigFive)

    result = {
        "timeline": timeline,
        "isStructured": text_answer["binary_prediction"],
        "isStructuredPercent": text_answer["percent_prediction"],
        "facialStatistics": {
            "topThreeEmotions": facial_stats,
            "frequencyOfTopEmotion": top_stat,
            "frequencyOfSecondEmotion": second_stat,
            "frequencyOfThirdEmotion": third_stat,
        },
        "overallFacialEmotion": facial_stats[0],
        "overallSentiment": calculate_overall_audio_sentiment(audio_answer),
        "topFiveKeywords": grab_top_five_keywords(audio_answer),
        "transcript": text_answer["output_text"],
        "bigFive": bigFive,
        "competencyFeedback": competency_feedback,
        "bigFiveDerivedCompetencies": bigfive_derived_competencies,
    }
    result["aggregateScore"] = compute_aggregate_score(result)
    response = {}
    response["evaluation"] = result
    return str(response)
