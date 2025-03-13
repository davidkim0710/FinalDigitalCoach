from typing import Dict, List, Union, TypedDict, Any, Optional
from enum import Enum

class FER_Emotions(Enum):
    """
        Unused just for reference
    """
    angry = "angry"
    disgust = "disgust"
    fear = "fear"
    happy = "happy"
    sad = "sad"
    surprise = "surprise"
    neutral = "neutral"


class ASM_Sentiments(Enum):
    """
        Unused just for reference
    """
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

class EmotionTotals(TypedDict):
    angry: float
    disgust: float
    fear: float
    happy: float
    sad: float
    surprise: float
    neutral: float


class EmotionTimelines(TypedDict):
    angry: List[float]
    disgust: List[float]
    fear: List[float]
    happy: List[float]
    sad: List[float]
    surprise: List[float]
    neutral: List[float]


class EmotionDetectionResult(TypedDict):
    """
    Result of facial emotion detection processing by FER
    """
    total_frames: int             # Total number of frames analyzed
    frame_inference_rate: int     # Frequency of frame sampling
    emotion_sums: EmotionTotals   # Sum of emotion scores across all frames
    timeline: EmotionTimelines    # Per-frame emotion score data
    clip_length_seconds: float    # Audio duration in seconds
    errors: Optional[str]


class SentimentResult(TypedDict):
    """Individual sentiment analysis result for a text segment"""
    text: str
    sentiment: str                # "POSITIVE", "NEUTRAL", or "NEGATIVE" 
    confidence: float             # Confidence score 0.0-1.0
    start: int                    # Start time in milliseconds
    end: int                      # End time in milliseconds


class TimestampData(TypedDict):
    """Timestamp info for keyword occurrences"""
    start: int                    # Start time in milliseconds
    end: int                      # End time in milliseconds


class HighlightData(TypedDict):
    """Data for auto-highlighted keywords/phrases"""
    text: str                     # The highlighted word or phrase
    rank: float                   # Importance ranking (0-1), words relevant to the content.
    count: int                    # Number of occurrences
    timestamps: List[TimestampData]  # When this word appears in the audio


class IABLabel(TypedDict):
    """IAB category label with relevance score"""
    label: str                    # Category name
    relevance: float              # Relevance score (0-1)


class IABResult(TypedDict):
    """IAB category detection results"""
    text: str                     # Input text that was analyzed
    labels: List[IABLabel]        # Detected category labels


class AudioSentimentResult(TypedDict):
    """
        Result of audio sentiment analysis by AssemblyAI
    """
    sentiment_analysis: List[SentimentResult]    # Sentiment analysis per segment
    highlights: List[HighlightData]              # Auto-detected key phrases
    iab_results: Union[IABResult, Dict[str, Any]]  # Category detection results
    clip_length_seconds: float  # Audio duration in seconds
    errors: Optional[str]       # Error message if any


class ExtractedAudio(TypedDict):
    """
        Result of audio extraction by MoviePy
    """
    path_to_file: str
    clip_length_seconds: float


class Content(TypedDict):
    """
        Content to be processed by `create_answer`
    """
    fname: str # Full path to the video file
    rename: str # Filename to be used for audio file


class StructureDetails(TypedDict):
    """
        Metrics for text structure analysis
    """
    paragraph_count: int
    avg_paragraph_length: int
    transition_words: int
    has_intro: bool
    has_conclusion: bool
    sentence_variety: int


class TextStructureResult(TypedDict):
    """
        Text Structure Analysis
    """
    prediction_score: float
    binary_prediction: int
    output_text: str
    details: StructureDetails


class TimelineStructure(TypedDict):
    """
        Timeline Structure Analysis
    """
    start: int # in milliseconds
    end: int # in milliseconds
    audioSentiment: str
    facialEmotion: List[str]


class BigFiveScoreResult(TypedDict):
    """
        Big Five Score Analysis
    """
    o: float
    c: float
    e: float
    a: float
    n: float
    _disclaimer: str


class CompetencyFeedback(TypedDict):
    """
        Competency Feedback
    """
    score: float
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]

class OverallCompetencyFeedback(TypedDict):
    """
        Overall Competency Competency Feedback
    """
    communication_clarity: CompetencyFeedback
    confidence: CompetencyFeedback
    engagement: CompetencyFeedback
    overall_score: float
    summary: str
    key_recommendations: List[str]

class FacialStatistics(TypedDict):
    """
    Result of facial emotion detection processing by FER
    """
    topThreeEmotions: List[str]  # Most frequent emotion
    frequencyOfTopEmotion: float  # 0-100 % of total response
    frequencyOfSecondEmotion: float  # 0-100 % of total response
    frequencyOfThirdEmotion: float  # 0-1 ratio % of total response

class CreateAnswerEvaluation(TypedDict):
    """
    Result of creating an answer
    """
    timeline: List[TimelineStructure]
    isStructured: int # 1 or 0
    predictionScore: float # 0-100
    facialStatistics: FacialStatistics 
    overallFacialEmotion: str # Most common facial emotion
    overallSentiment: str # Overall audio sentiment from assemblyAI
    topFiveKeywords: List[HighlightData] # Top 5 keywords
    transcript: str # Full transcript of speech
    bigFive: BigFiveScoreResult
    competencyFeedback: OverallCompetencyFeedback
    aggregateScore: float # Overall score (0-100)


class CreateAnswerResult(TypedDict):
    """
    Result of creating an answer
    """
    evaluation: CreateAnswerEvaluation

