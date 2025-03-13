from typing import Dict, List, Union, TypedDict, Any
"""Sub-types for EmotionDetectionResult"""
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


"""Sub-types for AudioSentimentResult from AssemblyAI"""
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
    rank: float                   # Importance ranking (0-1)
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
