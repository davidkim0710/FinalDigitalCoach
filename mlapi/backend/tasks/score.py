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
)
from .helpers.competency_analysis import generate_competency_feedback
from rq.decorators import job
from backend.redisStore.myConnection import get_redis_con
from typing import List
from backend.tasks.types import (
    EmotionDetectionResult, 
    AudioSentimentResult, 
    TextStructureResult, 
    TimelineStructure, 
    BigFiveScoreResult, 
    OverallCompetencyFeedback,
    CreateAnswerResult,
    CreateAnswerEvaluation
)


@job("default", connection=get_redis_con())
def create_answer(content) -> CreateAnswerResult:
    """
    Creates feedback answer. 
    """
    # errors could occur here
    facial_answer: EmotionDetectionResult = score_facial(content)
    audio_answer: AudioSentimentResult = score_audio(content)
    text_answer: TextStructureResult = score_text_structure(audio_answer)
    #  
    timeline: List[TimelineStructure] = av_timeline_resolution(
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
    bigFive: BigFiveScoreResult = score_bigFive(audio_answer, facial_stats, text_answer)
    competency_feedback: OverallCompetencyFeedback = generate_competency_feedback(
        facial_answer, audio_answer, text_answer
    )
    result: CreateAnswerEvaluation = {
        "timeline": timeline,
        "isStructured": text_answer["binary_prediction"],
        "predictionScore": text_answer["prediction_score"],
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
        "aggregateScore": 0.0,
    }
    result["aggregateScore"] = compute_aggregate_score(result)
    response: CreateAnswerResult = {
        "evaluation": result
    }
    # str(response) ???
    return response
