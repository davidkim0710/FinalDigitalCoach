"""
Module for competency-based interview feedback analysis.
This provides a more practical alternative to Big 5 personality scoring.
"""

def analyze_communication_clarity(text_analysis, audio_analysis):
    """
    Analyzes communication clarity based on speech patterns and text structure.
    
    Returns:
        dict: Score and specific feedback on communication clarity
    """
    # Calculate a clarity score based on speech rate, pauses, and text structure
    speech_rate = audio_analysis.get("speech_rate", 0)
    text_structure = text_analysis.get("percent_prediction", 0)
    
    clarity_score = (speech_rate * 0.4 + text_structure * 0.6) / 100
    
    feedback = {
        "score": min(clarity_score * 10, 10),  # Scale to 0-10
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": []
    }
    
    # Add specific feedback based on the analysis
    if text_structure > 0.7:
        feedback["strengths"].append("Well-structured and organized response")
    elif text_structure < 0.4:
        feedback["areas_for_improvement"].append("Response structure could be improved")
        feedback["recommendations"].append("Try using the STAR method (Situation, Task, Action, Result) for structuring your answers")
    
    return feedback


def analyze_confidence(facial_analysis, audio_analysis):
    """
    Analyzes confidence level based on facial expressions and voice tone.
    
    Returns:
        dict: Score and specific feedback on perceived confidence
    """
    # Get relevant metrics
    positive_emotions = sum(facial_analysis.get(emotion, 0) for emotion in ["happy", "confident"])
    negative_emotions = sum(facial_analysis.get(emotion, 0) for emotion in ["fear", "nervous", "sad"])
    audio_sentiment = audio_analysis.get("average_sentiment", 0)
    
    # Calculate confidence score
    confidence_score = (positive_emotions - negative_emotions) * 0.6 + audio_sentiment * 0.4
    confidence_score = min(max(confidence_score, 0), 1)  # Normalize between 0 and 1
    
    feedback = {
        "score": confidence_score * 10,  # Scale to 0-10
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": []
    }
    
    # Add specific feedback
    if confidence_score > 0.7:
        feedback["strengths"].append("Projected strong confidence throughout your response")
    elif confidence_score < 0.4:
        feedback["areas_for_improvement"].append("Confidence level appears lower than optimal")
        feedback["recommendations"].append("Practice power posing before interviews and maintain eye contact")
    
    return feedback


def analyze_engagement(facial_analysis, audio_analysis, text_analysis):
    """
    Analyzes how engaging the response is likely to be to interviewers.
    
    Returns:
        dict: Score and specific feedback on engagement level
    """
    # Metrics for engagement could include:
    # - Emotional variation in face and voice
    # - Speech rate variation
    # - Use of keywords/relevant terminology
    # - Storytelling elements
    
    # Simplified implementation
    emotion_variety = len([e for e, v in facial_analysis.items() if v > 0.1])
    speech_variation = audio_analysis.get("pitch_variation", 0.5)
    keyword_usage = len(audio_analysis.get("keywords", []))
    
    engagement_score = (emotion_variety * 0.3 + speech_variation * 0.4 + min(keyword_usage / 10, 1) * 0.3)
    
    feedback = {
        "score": min(engagement_score * 10, 10),  # Scale to 0-10
        "strengths": [],
        "areas_for_improvement": [],
        "recommendations": []
    }
    
    # Add engagement-specific feedback
    if speech_variation > 0.7:
        feedback["strengths"].append("Good vocal variety keeps your answer engaging")
    elif speech_variation < 0.3:
        feedback["areas_for_improvement"].append("Your vocal tone could use more variation")
        feedback["recommendations"].append("Practice adding emphasis to key points in your responses")
    
    return feedback


def generate_competency_feedback(facial_analysis, audio_analysis, text_analysis):
    """
    Generates comprehensive competency-based feedback from all analysis components.
    
    Returns:
        dict: Structured feedback on key interview competencies with actionable recommendations
    """
    feedback = {
        "communication_clarity": analyze_communication_clarity(text_analysis, audio_analysis),
        "confidence": analyze_confidence(facial_analysis, audio_analysis),
        "engagement": analyze_engagement(facial_analysis, audio_analysis, text_analysis),
        "overall_score": 0,
        "summary": "",
        "key_recommendations": []
    }
    
    # Calculate overall score
    scores = [
        feedback["communication_clarity"]["score"],
        feedback["confidence"]["score"],
        feedback["engagement"]["score"]
    ]
    feedback["overall_score"] = sum(scores) / len(scores)
    
    # Generate summary and key recommendations
    strengths = []
    improvements = []
    
    for category in ["communication_clarity", "confidence", "engagement"]:
        strengths.extend(feedback[category].get("strengths", []))
        improvements.extend(feedback[category].get("areas_for_improvement", []))
    
    # Generate summary based on overall performance
    if feedback["overall_score"] >= 7:
        feedback["summary"] = "Your response demonstrates strong interview skills with some specific areas to refine."
    elif feedback["overall_score"] >= 5:
        feedback["summary"] = "Your response has good elements but could benefit from targeted improvements."
    else:
        feedback["summary"] = "Your response needs development in several key areas to increase interview effectiveness."
    
    # Select top recommendations from all categories
    all_recommendations = []
    for category in ["communication_clarity", "confidence", "engagement"]:
        all_recommendations.extend(feedback[category].get("recommendations", []))
    
    feedback["key_recommendations"] = all_recommendations[:3]  # Top 3 recommendations
    
    return feedback
