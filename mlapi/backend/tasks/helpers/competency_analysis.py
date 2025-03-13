"""
Module for competency-based interview feedback analysis.
Added in addition to Big Five scores to be more practical.
TODO: Add more or different types of feedback.
"""
from backend.tasks.types import CompetencyFeedback, OverallCompetencyFeedback
from backend.utils.logger_config import get_logger

logger = get_logger(__name__)


def _analyze_communication_clarity(text_analysis, audio_analysis) -> CompetencyFeedback:
    """
    Analyzes communication clarity based on speech rate and text structure.
    Returns:
        dict: Score and specific feedback on communication clarity
    """
    result: CompetencyFeedback = {
        "score": 0,
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": [],
    }
    speech_rate = len(text_analysis["output_text"]) / audio_analysis["clip_length_seconds"] # words per second
    text_structure = text_analysis["prediction_score"] 
    clarity_score = (speech_rate * 0.1 + text_structure * 0.9 / 10)
    clarity_score = round(min( clarity_score , 10), 2) # Scale to 0-10
    result["score"] = clarity_score  
    if clarity_score > 5:
        result["strengths"].append("Well-structured and organized response")
    elif clarity_score < 5:
        result["areas_for_improvement"].append("Response structure could be improved")
        result["recommendations"].append(
            "Try using the STAR method (Situation, Task, Action, Result) for structuring your answers"
        )
    return result 


def _analyze_confidence(_facial_analysis, audio_analysis) -> CompetencyFeedback:
    """
    Analyzes confidence level based on facial expressions and voice tone.
    NOTE: Maybe use facial analysis in future, maybe fear/suprise/sad subtract from confidence
    Returns:
        dict: Score and specific feedback on perceived confidence
    """
    result: CompetencyFeedback = {
        "score": 0,
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": [],
    }
    confidence_attr = 0
    for i in audio_analysis["sentiment_analysis"]:
        confidence_attr += i["confidence"]
    confidence_score = round(min(confidence_attr, 10), 2) # Scale to 0-10
    result["score"] = confidence_score  
    if confidence_score > 5:
        result["strengths"].append(
            "Projected strong confidence throughout your response"
        )
    elif confidence_score < 5: 
        result["areas_for_improvement"].append(
            "Confidence level appears lower than optimal"
        )
        result["recommendations"].append(
            "Practice maintaining eye contact and speaking clearly"
        )
    return result 


def _analyze_engagement(facial_analysis, audio_analysis, _text_analysis) -> CompetencyFeedback:
    """
    Analyzes how engaging the response is likely to be to interviewers.
    Metrics for engagement could include:
    - Emotional variation in face and voice
    - Speech rate variation
    - Use of keywords/relevant terminology
    - Storytelling elements
    Returns:
        dict: Score and specific feedback on engagement level
    """
    result: CompetencyFeedback = {
        "score": 0,
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": [],
    }
    emotion_data = {}
    for key, value in facial_analysis.items():
        if isinstance(value, (int, float)) and key not in ["emotion_sums", "timeline"]:
            emotion_data[key] = value
    emotion_variety = len([e for e, v in emotion_data.items() if v > 0.1])
    keyword_usage = 0
    for i in audio_analysis["highlights"]:
        if i["rank"] > 0.5:
            keyword_usage += 1
    engagement_score = (
        min(emotion_variety / 3, 1) * 0.3  # Normalize to max of 1
        + min(keyword_usage / 10, 1) * 0.3
    )
    result["score"] = round(min(engagement_score * 10, 10), 2)  # Scale to 0-10
    if keyword_usage > 3:
        result["strengths"].append("Good keyword usage")
    elif keyword_usage < 3:
        result["areas_for_improvement"].append(
            "Try to use more keywords related to the content."
        )
        result["recommendations"].append(
            "Practice adding emphasis to key points in your responses"
        )
    return result 


def generate_competency_feedback(facial_analysis, audio_analysis, text_analysis) -> OverallCompetencyFeedback:
    """
    Generates comprehensive competency-based feedback from all analysis components.
    Returns:
        dict: Structured feedback on key interview competencies with actionable recommendations
    """
    feedback: OverallCompetencyFeedback = {
        "communication_clarity": _analyze_communication_clarity(
            text_analysis, audio_analysis
        ),
        "confidence": _analyze_confidence(facial_analysis, audio_analysis),
        "engagement": _analyze_engagement(
            facial_analysis, audio_analysis, text_analysis
        ),
        "overall_score": 0,
        "summary": "",
        "key_recommendations": [],
    }
    scores = [
        feedback["communication_clarity"]["score"],
        feedback["confidence"]["score"],
        feedback["engagement"]["score"],
    ]
    feedback["overall_score"] = sum(scores) / len(scores)
    strengths = []
    improvements = []
    for category in ["communication_clarity", "confidence", "engagement"]:
        strengths.extend(feedback[category].get("strengths", []))
        improvements.extend(feedback[category].get("areas_for_improvement", []))
    if feedback["overall_score"] >= 7:
        feedback["summary"] = (
            "Your response demonstrates strong interview skills with some specific areas to refine."
        )
    elif feedback["overall_score"] >= 5:
        feedback["summary"] = (
            "Your response has good elements but could benefit from targeted improvements."
        )
    else:
        feedback["summary"] = (
            "Your response needs development in several key areas to increase interview effectiveness."
        )
    all_recommendations = []
    for category in ["communication_clarity", "confidence", "engagement"]:
        all_recommendations.extend(feedback[category].get("recommendations", []))
    feedback["key_recommendations"] = all_recommendations[:3]  # Top 3 recommendations
    feedback["overall_score"] = round(feedback["overall_score"], 2)
    return feedback
