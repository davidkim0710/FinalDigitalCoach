from .file_management import (
    move_cv_files,
)
from .text_processor import clean_text
from ..models.model import detect_emotions, detect_audio_sentiment
from .av_processing import extract_audio
from .statistics import (
    calculate_overall_audio_sentiment,
    grab_top_five_keywords,
)
from typing import Dict, Any 
import re


def score_text_structure(audio_answer):
    """
    Score how structured the user's answers are using a hybrid approach:
    1. Rule-based analysis for basic structure indicators
    2. Optional pre-trained model integration (if configured)
    
    Returns dict with:
    - percent_prediction: 0-100 score indicating structure quality
    - binary_prediction: 1 if structured, 0 if not
    - output_text: processed text
    - details: Additional information about the structure assessment
    """
    # Extract text from sentiment analysis
    sentiments: list[dict] = audio_answer["sentiment_analysis"]
    text = ""
    for i in sentiments:
        text += i["text"]
    cleaned_text: str = clean_text(answer=text)
    
    # Apply rule-based structure analysis
    structure_score, structure_details = analyze_text_structure(text=cleaned_text)
    
    # Convert to binary prediction (threshold at 50%)
    binary_prediction = 1 if structure_score >= 50 else 0
    
    return {
        "percent_prediction": structure_score,
        "binary_prediction": binary_prediction,
        "output_text": cleaned_text,
        "details": structure_details
    }

# TODO use ML model to create weighted Average of the two scores. Make sure to use rq worker for the model. 
def analyze_text_structure(text: str) -> tuple[float, Dict[str, Any]]:
    """
    Analyzes text structure using rule-based heuristics.
    
    Args:
        text: The text to analyze
        
    Returns:
        tuple containing:
        - float: Structure score (0-100)
        - dict: Detailed breakdown of structure components
    """
    # Initialize structure metrics
    metrics = {
        "paragraph_count": 0,
        "avg_paragraph_length": 0,
        "transition_words": 0,
        "has_intro": False,
        "has_conclusion": False,
        "sentence_variety": 0,
    }
    # Split into paragraphs (could be any reasonable separator)
    paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    metrics["paragraph_count"] = len(paragraphs)
    # Calculate average paragraph length
    if metrics["paragraph_count"] > 0:
        total_sentences = 0
        for p in paragraphs:
            sentences = re.split(r'[.!?]+', p)
            sentences = [s.strip() for s in sentences if s.strip()]
            total_sentences += len(sentences)
        metrics["avg_paragraph_length"] = total_sentences / metrics["paragraph_count"]
    
    # Check for transition words/phrases
    transition_words = [
        'first', 'second', 'third', 'finally', 'consequently', 'in conclusion', 
        'for example', 'moreover', 'however', 'therefore', 'in addition', 
        'furthermore', 'thus', 'meanwhile', 'nevertheless', 'subsequently'
    ]
    lower_text = text.lower()
    for word in transition_words:
        if word in lower_text:
            metrics["transition_words"] += 1
    # Check for introduction and conclusion
    intro_patterns = ['introduce', 'begin', 'start', 'first', 'today', 'topic']
    conclusion_patterns = ['conclude', 'conclusion', 'summary', 'finally', 'in summary', 'to sum up']
    # Assuming paragraphs are separated by newlines 
    first_para = paragraphs[0].lower() if paragraphs else ""
    last_para = paragraphs[-1].lower() if paragraphs else ""
    metrics["has_intro"] = any(pattern in first_para for pattern in intro_patterns)
    metrics["has_conclusion"] = any(pattern in last_para for pattern in conclusion_patterns)
    # Calculate overall structure score (weighted components)
    score = 0
    # Good paragraph structure (3-5 paragraphs ideal)
    if 3 <= metrics["paragraph_count"] <= 5:
        score += 30
    elif metrics["paragraph_count"] > 1:
        score += 15
    # Good paragraph length (2-5 sentences per paragraph)
    if 2 <= metrics["avg_paragraph_length"] <= 5:
        score += 15
    elif metrics["avg_paragraph_length"] > 0:
        score += 5
    # Has transition words
    score += min(20, metrics["transition_words"] * 5)
    # Has intro
    if metrics["has_intro"]:
        score += 15
    # Has conclusion
    if metrics["has_conclusion"]:
        score += 20
    # Ensure score is between 0-100
    final_score = max(min(score, 100), 0)
    return final_score, metrics


def score_audio(content):
    """
    score user's audio.
    """
    if "fname" not in content or "rename" not in content:
        return {"errors": "File name and rename does not exist"}
    fname, rename = (
        content["fname"],
        content["rename"],
    )
    audio = extract_audio(fname, rename)
    if "errors" in audio:
        return {"errors": audio["errors"]}
    audio_file_path = audio["path_to_file"]
    sentiment = detect_audio_sentiment(audio_file_path)
    sentiment["clip_length_seconds"] = audio["clip_length_seconds"]
    if "errors" in sentiment:
        return {"errors": sentiment["errors"]}
    return sentiment


def score_facial(content):
    """
    score user's facial expressions
    """
    if "fname" not in content:
        return {"errors": "Video file name does not exist"}
    video_fname = content["fname"]
    total_emotion_score = detect_emotions(video_fname)
    move_cv_files()
    if "errors" in total_emotion_score:
        return {"errors": total_emotion_score["errors"]}
    return total_emotion_score


def score_bigFive(audio_answer, facial_stats, text_answer):
    """
    Attempts to approximate Big Five personality traits.
    
    NOTE: This method has significant limitations and should not be considered
    validated for personality assessment. We recommend using the competency-based feedback instead.
    
    The Big Five traits are:
    - O: Openness to experience
    - C: Conscientiousness
    - E: Extraversion
    - A: Agreeableness
    - N: Neuroticism (emotional stability)
    """
    # Return normalized scores that avoid extreme values
    # Range constraint between -3 and 3 for each trait to avoid misinterpretation
    # Default base scores (neutral starting points)
    o_score, c_score, e_score, a_score, n_score = 0, 0, 0, 0, 0
    # Get relevant signals from the analysis
    sentiment_score = 0
    overall_sentiment = calculate_overall_audio_sentiment(audio_answer)
    if overall_sentiment == "POSITIVE":
        sentiment_score = 1
    elif overall_sentiment == "NEGATIVE":
        sentiment_score = -1
    # Adjust scores based on keyword complexity (weak signal)
    keywords = grab_top_five_keywords(audio_answer)
    avg_keyword_length = 0
    if keywords:
        avg_keyword_length = sum(min(len(kw["text"]), 10) for kw in keywords) / len(keywords)
        o_score += (avg_keyword_length - 5) / 5  # normalize to roughly -1 to 1 range
    # Facial expression adjustments (weak signal)
    if facial_stats and len(facial_stats) > 0:
        top_emotion = facial_stats[0]
        if top_emotion == "happy":
            e_score += 1
            a_score += 1
            n_score -= 0.5
        elif top_emotion == "neutral":
            # Neutral doesn't tell us much
            pass
        elif top_emotion in ["sad", "fear", "disgust", "angry"]:
            n_score += 1
            e_score -= 0.5
            a_score -= 0.5
    # Text structure adjustments (weak signal)
    structure_score = text_answer.get("percent_prediction", 50) / 100
    c_score += (structure_score - 0.5) * 2  # normalize to roughly -1 to 1
    # Sentiment adjustments
    e_score += sentiment_score
    a_score += sentiment_score * 0.5
    n_score -= sentiment_score * 0.5
    # Final normalization to ensure scores are within reasonable bounds
    def normalize_score(score):
        return max(min(round(score), 3), -3)
    # Return the scores. 
    bigFive = {
        "o": normalize_score(o_score),
        "c": normalize_score(c_score),
        "e": normalize_score(e_score),
        "a": normalize_score(a_score),
        "n": normalize_score(n_score),
        "_disclaimer": "This is a weak approximation of Big Five traits and should not be used for serious assessments.",
    }
    
    return bigFive


def map_bigfive_to_competencies(bigfive_scores):
    """
    Maps Big Five trait scores to interview competencies as a transitional approach.
    
    
    Returns:
        dict: Mapped competency scores on a 0-10 scale
    """
    # Extract scores
    o_score = bigfive_scores.get('o', 0)
    c_score = bigfive_scores.get('c', 0)
    e_score = bigfive_scores.get('e', 0)
    a_score = bigfive_scores.get('a', 0)
    n_score = bigfive_scores.get('n', 0)
    
    # Convert from -3 to 3 scale to 0-10 scale
    normalize = lambda score: (score + 3) / 6 * 10
    
    # Map traits to competencies
    competencies = {
        "communication_clarity": normalize((c_score + o_score) / 2),  # Structure (C) and articulation (O)
        "confidence": normalize((e_score - n_score) / 2),  # Extraversion boosts, neuroticism reduces confidence
        "engagement": normalize((e_score + o_score + a_score) / 3),  # Engagement combines multiple factors
        "adaptability": normalize((o_score - n_score) / 2),  # Openness and emotional stability
    }
    
    return competencies
