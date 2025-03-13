import os
import assemblyai as aai
from fer import Video, FER
from pandas import DataFrame
from backend.utils import (
    get_video_dir,
    get_output_dir,
)
from typing import cast, Any
from backend.tasks.types import EmotionDetectionResult, EmotionTotals, EmotionTimelines, AudioSentimentResult 
from backend.utils.logger_config import get_logger

logger = get_logger(__name__)

AAPI_KEY = os.getenv("AAPI_KEY")

# Use fer to detect emotions in a video
def detect_emotions(video_fname, freq=10) -> EmotionDetectionResult:
    """
    Detect emotions in a video using FER

    Args:
        video_fname: Name of the video file or full path
        freq: Frequency to sample frames for emotion detection

    Returns:
        dict: Dictionary with emotion detection results
    """
    # Check if video_fname is a full path or just a filename
    result: Any = {}
    if os.path.isabs(video_fname):
        logger.info(f"Setting videofile_path to absolute path: {video_fname}")
        videofile_path = video_fname
    else:
        # TODO: handle files donwload from URL 
        path_video = os.path.join(get_video_dir(), video_fname)
        path_output = os.path.join(get_output_dir(), video_fname)
        if os.path.exists(path_video):
            videofile_path = path_video
        elif os.path.exists(path_output):
            videofile_path = path_output
        else:
            # Try test directory if this might be a test file
            tests_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests"
            )
            test_file_path = os.path.join(tests_dir, "data", video_fname)
            if os.path.exists(test_file_path):
                videofile_path = test_file_path
            else:
                logger.error(f"Could not find video file {video_fname} in any location")
                result["error"] = "Could not find video file"
    logger.info(f"Detecting emotions from video file: {videofile_path}")
    face_detection = FER(mtcnn=True) # type: ignore
    try:
        input_video = Video(videofile_path)
        try:
            processed_data = input_video.analyze(
                face_detection, display=False, frequency=freq
            ) # type: ignore
            if not processed_data:
                logger.error("No facial data detected in video")
                result["error"] = "No facial data detected in video"
            # Convert to pandas DataFrame and ensure proper type
            vid_df = cast(DataFrame, input_video.to_pandas(processed_data))
            if vid_df.empty:
                logger.error("No data in video analysis DataFrame")
                result["error"] = "No data in video analysis DataFrame"
            vid_df = cast(DataFrame, input_video.get_first_face(vid_df))
            vid_df = cast(DataFrame, input_video.get_emotions(vid_df))
            # Verify DataFrame structure
            emotion_cols = [
                "angry",
                "disgust",
                "fear",
                "happy",
                "sad",
                "surprise",
                "neutral",
            ]
            if not all(col in vid_df.columns for col in emotion_cols):
                logger.error("Missing required emotion columns in DataFrame")
                result["error"] = "Missing required emotion columns in DataFrame"
            # Calculate emotion sums and timelines
            sum_emotions: EmotionTotals | Any = {}
            timelines: EmotionTimelines | Any = {}
            for emotion in emotion_cols:
                sum_emotions[emotion] = float(vid_df[emotion].sum())
                timelines[emotion] = vid_df[emotion].values.tolist()
        except Exception as e:
            logger.error(f"Error calculating emotion scores: {str(e)}")
            result["errors"] = f"Failed to process emotion data: {str(e)}"
        result = {
            "total_frames": len(list(vid_df.loc[:, "angry"])),
            "frame_inference_rate": freq,
            "emotion_sums": sum_emotions,
            "timeline": timelines,
        }
    except OSError as exception:
        logger.error(f"Error detecting emotions: {str(exception)}")
        result["error"] = f"Error detecting emotions: {str(exception)}"
    return result

def detect_audio_sentiment(fname) -> AudioSentimentResult:
    """
    Detects audio sentiment using the AssemblyAI API package

    Args:
        fname: Path to the audio file

    Returns:
        dict: Dictionary with sentiment analysis results
    """
    result: Any = {}
    try:
        # Initialize the AssemblyAI client
        if not AAPI_KEY:
            logger.error("No AssemblyAI API key found in environment")
            result["errors"] = "No AssemblyAI API key configured"
        aai.settings.api_key = AAPI_KEY
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(
            sentiment_analysis=True,
            auto_highlights=True,
            iab_categories=True,
        )
        logger.info(f"Transcribing audio file: {fname}")
        transcript: aai.Transcript = transcriber.transcribe(
            fname,
            config,
        )
        if transcript.error:
            raise Exception(transcript.error)
        
        # Sentiment Analysis
        if transcript.sentiment_analysis:
            result["sentiment_analysis"] = [
                {
                    "text": result.text,
                    "sentiment": result.sentiment.value,
                    "confidence": result.confidence,
                    "start": result.start,
                    "end": result.end,
                }
                for result in transcript.sentiment_analysis
            ]
        # Auto Highlights (Key Phrases)
        if transcript.auto_highlights and transcript.auto_highlights.results:
            result["highlights"] = [
                {
                    "text": result.text,
                    "rank": result.rank,
                    "count": result.count,
                    "timestamps": [
                        {"start": ts.start, "end": ts.end} for ts in result.timestamps
                    ],
                }
                for result in transcript.auto_highlights.results
            ]
        result["iab_results"] = {}
        # IAB Categories (Topic Detection)
        try:
            categories = transcript.iab_categories
            if categories is not None:
                results = getattr(categories, "results", None)
                if results and isinstance(results, (list, tuple)) and len(results) > 0:
                    first_result = results[0]
                    if hasattr(first_result, "text") and hasattr(
                        first_result, "labels"
                    ):
                        result["iab_results"] = {
                            "text": str(first_result.text),
                            "labels": [],
                        }
                        labels = getattr(first_result, "labels", None)
                        if labels and isinstance(labels, (list, tuple)):
                            result["iab_results"]["labels"] = [
                                {
                                    "label": str(getattr(label, "label", "")),
                                    "relevance": float(
                                        getattr(label, "relevance", 0.0)
                                    ),
                                }
                                for label in labels
                                if hasattr(label, "label")
                                and hasattr(label, "relevance")
                            ]
        except Exception as e:
            logger.warning(f"Failed to process IAB categories: {str(e)}")
        logger.info(f"Transcript processing completed for {fname}")
        logger.info(f"transcript: {transcript.text}")
    except Exception as e:
        logger.error(f"Exception in audio sentiment detection: {str(e)}")
        result["errors"] = str(e)
    return result 
