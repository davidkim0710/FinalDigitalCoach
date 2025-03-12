import os
import logging
import assemblyai as aai
import pandas as pd
import numpy as np
from fer import Video, FER
from typing import Any, Dict, List, Optional, Union, cast
from pandas import DataFrame
from backend.utils import (
    get_video_path,
    get_output_path,
    get_video_dir,
    get_output_dir,
    get_audio_dir,
)

# Configure logger
logger = logging.getLogger(__name__)

# Get AssemblyAI API key from environment
AAPI_KEY = os.getenv("AAPI_KEY")


# Use fer to detect emotions in a video
def detect_emotions(video_fname, freq=10):
    """
    Detect emotions in a video using FER

    Args:
        video_fname: Name of the video file or full path
        freq: Frequency to sample frames for emotion detection

    Returns:
        dict: Dictionary with emotion detection results
    """
    # Check if video_fname is a full path or just a filename
    if os.path.isabs(video_fname):
        videofile_path = video_fname
    else:
        # Look in standard locations - check video dir first since that's where files are uploaded
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
                return {"errors": f"Video file {video_fname} not found"}

    logger.info(f"Detecting emotions from video file: {videofile_path}")

    face_detection = FER(mtcnn=True)
    try:
        input_video = Video(videofile_path)
        try:
            processed_data = input_video.analyze(
                face_detection, display=False, frequency=freq
            )

            if not processed_data:
                logger.error("No facial data detected in video")
                return {"errors": "No facial expressions detected in video"}

            # Convert to pandas DataFrame and ensure proper type
            vid_df = cast(DataFrame, input_video.to_pandas(processed_data))
            if vid_df.empty:
                logger.error("No data in video analysis DataFrame")
                return {"errors": "Failed to process video data"}

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
                return {"errors": "Failed to detect emotion data in video"}

            # Calculate emotion sums and timelines
            sum_emotions = {}
            timelines = {}
            for emotion in emotion_cols:
                sum_emotions[emotion] = float(vid_df[emotion].sum())
                timelines[emotion] = vid_df[emotion].values.tolist()
        except Exception as e:
            logger.error(f"Error calculating emotion scores: {str(e)}")
            return {"errors": f"Failed to process emotion data: {str(e)}"}
        response = {
            "total_frames": len(list(vid_df.loc[:, "angry"])),
            "frame_inference_rate": freq,
            "emotion_sums": sum_emotions,
            "timeline": timelines,
        }
        return response
    except OSError as exception:
        logger.error(f"Error detecting emotions: {str(exception)}")
        return {"errors": str(exception)}


def detect_audio_sentiment(fname):
    """
    Detects audio sentiment using the AssemblyAI API package

    Args:
        fname: Path to the audio file

    Returns:
        dict: Dictionary with sentiment analysis results
    """
    try:
        # Initialize the AssemblyAI client
        if not AAPI_KEY:
            logger.error("No AssemblyAI API key found in environment")
            return {"errors": "No AssemblyAI API key configured"}

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

        # Create response dictionary
        response: Dict[str, Any] = {
            "sentiment_analysis": [],
            "highlights": [],
            "iab_results": {},
            "clip_length_seconds": 0,
        }

        # Sentiment Analysis
        if transcript.sentiment_analysis:
            response["sentiment_analysis"] = [
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
            response["highlights"] = [
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

        # Initialize empty IAB results
        response["iab_results"] = {}

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
                        response["iab_results"] = {
                            "text": str(first_result.text),
                            "labels": [],
                        }
                        labels = getattr(first_result, "labels", None)
                        if labels and isinstance(labels, (list, tuple)):
                            response["iab_results"]["labels"] = [
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
        # Audio Duration
        response["clip_length_seconds"] = transcript.audio_duration
        logger.info(f"Transcript processing completed for {fname}")
        logger.info(f"transcript: {transcript.text}")
        return response

    except Exception as e:
        logger.error(f"Exception in audio sentiment detection: {str(e)}")
        return {"errors": str(e)}
