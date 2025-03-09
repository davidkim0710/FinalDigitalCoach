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


def create_answer(content):
    """Accessed by the create an answer."""
    facial_answer = score_facial(content)
    if "errors" in facial_answer:
        return {"errors": facial_answer["errors"]}
        
    audio_answer = score_audio(content)
    if "errors" in audio_answer:
        return {"errors": audio_answer["errors"]}
        
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
    
    # Generate both traditional Big5 scoring and new competency feedback
    bigFive = score_bigFive(audio_answer, facial_stats, text_answer)
    
    # New competency-based feedback
    competency_feedback = generate_competency_feedback(
        facial_answer, 
        audio_answer,
        text_answer
    )
    
    # Also include a transition mapping from Big Five to competencies
    # This helps with backward compatibility and shows how the two relate
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
        "bigFive": bigFive,
        "competencyFeedback": competency_feedback,
        "bigFiveDerivedCompetencies": bigfive_derived_competencies,
    }
    result["aggregateScore"] = compute_aggregate_score(result)
    response = {}
    response["evaluation"] = result
    # response["text_analysis"] = text_answer
    # response["audio_analysis"] = audio_answer
    # response["userId"] = content["user_id"]
    # response["interviewId"] = content["interview_id"]
    # response["questionId"] = content["question_id"]
    # response["answerId"] = content["answer_id"]
    return str(response)
