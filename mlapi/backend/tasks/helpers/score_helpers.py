from .text_processor import clean_text
from ..models.model import detect_emotions, detect_audio_sentiment
from .av_processing import extract_audio
from .statistics import (
    calculate_overall_audio_sentiment,
    grab_top_five_keywords,
)
import re
from .text_structure_ml import analyze_text_structure_ml
from backend.tasks.types import (AudioSentimentResult,  EmotionDetectionResult, ExtractedAudio, StructureDetails, TextStructureResult, BigFiveScoreResult)
from typing import Tuple


def score_text_structure(audio_answer) -> TextStructureResult:
    """
    Score how structured the user's answers are using a hybrid approach:
    1. Rule-based analysis for basic structure indicators
    2. Optional pre-trained model integration (if configured)

    Returns dict with:
    - prediction_score: 0-100 score indicating structure quality
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

    structure_score, structure_details = _analyze_text_structure(text=cleaned_text)

    binary_prediction = 1 if structure_score >= 50 else 0

    return {
        "prediction_score": structure_score,
        "binary_prediction": binary_prediction,
        "output_text": cleaned_text,
        "details": structure_details,
    }


def _analyze_text_structure(text: str) -> Tuple[float, StructureDetails]: 
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
    metrics: StructureDetails = {
        "paragraph_count": 0,
        "avg_paragraph_length": 0,
        "transition_words": 0,
        "has_intro": False,
        "has_conclusion": False,
        "sentence_variety": 0,
    }
    # Split into paragraphs (could be any reasonable separator)
    paragraphs = re.split(r"\n\s*\n|\r\n\s*\r\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    metrics["paragraph_count"] = len(paragraphs)
    # Calculate average paragraph length
    if metrics["paragraph_count"] > 0:
        total_sentences = 0
        for p in paragraphs:
            sentences = re.split(r"[.!?]+", p)
            sentences = [s.strip() for s in sentences if s.strip()]
            total_sentences += len(sentences)
        metrics["avg_paragraph_length"] = total_sentences // metrics["paragraph_count"]
    # Check for transition words/phrases
    transition_words = [
        "first",
        "second",
        "third",
        "finally",
        "consequently",
        "in conclusion",
        "for example",
        "moreover",
        "however",
        "therefore",
        "in addition",
        "furthermore",
        "thus",
        "meanwhile",
        "nevertheless",
        "subsequently",
    ]
    lower_text = text.lower()
    for word in transition_words:
        if word in lower_text:
            metrics["transition_words"] += 1
    # Check for introduction and conclusion
    intro_patterns = ["introduce", "begin", "start", "first", "today", "topic"]
    conclusion_patterns = [
        "conclude",
        "conclusion",
        "summary",
        "finally",
        "in summary",
        "to sum up",
    ]
    # Assuming paragraphs are separated by newlines
    first_para = paragraphs[0].lower() if paragraphs else ""
    last_para = paragraphs[-1].lower() if paragraphs else ""
    metrics["has_intro"] = any(pattern in first_para for pattern in intro_patterns)
    metrics["has_conclusion"] = any(
        pattern in last_para for pattern in conclusion_patterns
    )
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
    calculate_score = max(min(score, 100), 0)
    # ML model feedback
    score, _ = analyze_text_structure_ml(text)
    # weighted average
    final_score = (calculate_score + score) / 2
    return final_score, metrics


def score_audio(content) -> AudioSentimentResult:
    """
    Score user's audio.
    """
    audio: ExtractedAudio = extract_audio(content["fname"], content["rename"])
    sentiment = detect_audio_sentiment(audio["path_to_file"]) 
    sentiment["clip_length_seconds"] = audio["clip_length_seconds"] 
    return sentiment


def score_facial(content) -> EmotionDetectionResult:
    """
    score user's facial expressions
    """
    res = detect_emotions(content["fname"])
    # TODO: handle data.csv file
    return res 


def score_bigFive(audio_answer, facial_stats, text_answer) -> BigFiveScoreResult:
    """
    Attempts to approximate Big Five personality traits on a scale of 0-7.
    The Big Five traits are:
    - O: Openness to experience
    - C: Conscientiousness
    - E: Extraversion
    - A: Agreeableness
    - N: Neuroticism (emotional stability)
    """
    # Default base scores (neutral starting points at middle of scale)
    o_score, c_score, e_score, a_score, n_score = 3.5, 3.5, 3.5, 3.5, 3.5
    
    # Get relevant signals from the analysis
    sentiment_score = 0
    overall_sentiment = calculate_overall_audio_sentiment(audio_answer)
    if overall_sentiment == "POSITIVE":
        sentiment_score = 1
    elif overall_sentiment == "NEGATIVE":
        sentiment_score = -1
    elif overall_sentiment == "NEUTRAL":
        sentiment_score = -0.5
    
    # Adjust scores based on keyword complexity (weak signal)
    keywords = grab_top_five_keywords(audio_answer)
    avg_keyword_length = 0
    if keywords:
        avg_keyword_length = sum(min(len(kw["text"]), 10) for kw in keywords) / len(keywords)
        o_score += (avg_keyword_length - 5) / 5 * 2  # Scale adjusted for 0-7 range
    
    # Facial expression adjustments (weak signal)
    if facial_stats and len(facial_stats) > 0:
        top_emotion = facial_stats[0]
        if top_emotion == "happy":
            e_score += 1
            a_score += 1
            n_score -= 0.5
        elif top_emotion == "neutral":
            pass
        elif top_emotion in ["sad", "fear", "disgust", "angry"]:
            n_score += 1
            e_score -= 0.5
            a_score -= 0.5
    
    # Adjust based on text structure
    structure_score = text_answer.get("prediction_score", 50) / 100
    c_score += (structure_score - 0.5) * 2  # normalized to roughly -1 to 1
    
    # Sentiment affects extraversion, agreeableness, and neuroticism
    e_score += sentiment_score
    a_score += sentiment_score * 0.5
    n_score -= sentiment_score * 0.5
    
    # Final normalization to ensure scores are within 0-7 scale
    def normalize_score(score):
        return max(min(round(score * 10) / 10, 7), 0)
    
    return {
        "o": normalize_score(o_score),
        "c": normalize_score(c_score),
        "e": normalize_score(e_score),
        "a": normalize_score(a_score),
        "n": normalize_score(n_score),
        "_disclaimer": "This is a weak approximation of Big Five traits and should not be used for serious assessments.",
    }
