import os
import logging
import moviepy.editor as mp
import pandas as pd
from backend.utils import (
    get_audio_path,
    get_video_dir,
    get_output_dir,
)
from backend.tasks.types import ExtractedAudio
from typing import Any

logger = logging.getLogger(__name__)


def _build_timeline_intervals_sentiment(sent_analysis_lst):
    """
    Iterates through the sentiment analysis list from the
    AssemblyAI Audio results to construct a list of lists
    in which the inner list corresponds to the format of
    [start_in_ms, end_in_ms, audio_sentiment_of_interval]
    """
    timeline = []
    for k in sent_analysis_lst:
        interval = [k["start"], k["end"], k["sentiment"]]
        timeline.append(interval)
    timeline.sort(key=lambda x: x[0])
    return timeline


def build_timeline_interval_facial(facial_data):
    """
    Builds the facial data timeline.
    """
    df = pd.DataFrame(data=facial_data["timeline"])
    max_val_index = df.idxmax(axis=1)
    emotion_per_frame = [i for i in max_val_index]
    facial_timeline = {
        k: v
        for k, v in zip(list(range(facial_data["total_frames"])), emotion_per_frame)
    }
    return facial_timeline


def _emotion_sentiment_match(start, end, interval_length, facial_timeline):
    try:
        return [
            facial_timeline[start // interval_length],
            facial_timeline[end // interval_length],
        ]
    except Exception:
        logger.error("Error in sentiment matching")
        logger.error(f"Facial timeline: {facial_timeline}")
        logger.error(
            f"Parameters: start={start}, end={end}, interval_length={interval_length}"
        )
        logger.error(
            f"Calculations: start//interval={start // interval_length}, end//interval={end // interval_length}"
        )
        return [-1, -1]


def av_timeline_resolution(clip_length, facial_data, audio_sentiments):
    """
    It takes the audio and facial data, and creates a timeline of the emotions and sentiments of the
    video

    :param clip_length: The length of the video in seconds
    :param facial_data: a dictionary containing the facial data
    :param audio_sentiments: a list of tuples, each tuple containing the start and end time of a segment
    of audio, and the sentiment of that segment
    :return: A list of dictionaries.
    """
    total_frames = facial_data["total_frames"]
    fps = round(total_frames / clip_length)
    interval_length = 1000 // fps
    audio_timeline = _build_timeline_intervals_sentiment(audio_sentiments)
    facial_timeline = build_timeline_interval_facial(facial_data)
    timeline = []
    for stats in audio_timeline:
        entry = {
            "start": stats[0],
            "end": stats[1],
            "audioSentiment": stats[2],
            "facialEmotion": _emotion_sentiment_match(
                stats[0], stats[1], interval_length, facial_timeline
            ),
        }
        timeline.append(entry)

    timeline = list(filter(lambda x: x["facialEmotion"] != [-1, -1], timeline))
    return timeline


def extract_audio(fname, des_fname) -> ExtractedAudio:
    """
    It takes a video file, extracts the audio to mp3, and returns the path to the audio file and the length of
    the video clip. Ensure ffmpeg is installed and the video path is correct if this is causing issues.

    :param fname: The name of the file you want to extract audio from
    :param des_fname: The name of the file you want to save the audio as
    :return: A dictionary with the path to the file and the clip length in seconds.
    """
    # Check if fname is a full path or just a filename
    result: Any = {}
    if os.path.isabs(fname):
        path = fname
    else:
        # Check in output directory first, then in video directory
        path_output = os.path.join(get_output_dir(), fname)
        path_video = os.path.join(get_video_dir(), fname)

        if os.path.exists(path_output):
            path = path_output
        elif os.path.exists(path_video):
            path = path_video
        else:
            # Try test directory if file might be a test resource
            tests_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests"
            )
            test_file_path = os.path.join(tests_dir, "data", fname)
            if os.path.exists(test_file_path):
                path = test_file_path
            else:
                logger.error(f"File {fname} not found in any expected locations")
    # Generate the output audio path
    if des_fname:
        des_path = get_audio_path(des_fname)
    else:
        des_path = get_audio_path()
    if not os.path.exists(path):
        logger.error(f"File {path} does not exist")
    logger.info(f"Processing file: {path}")
    try:
        mv_clip = mp.VideoFileClip(path)
        mv_clip.audio.write_audiofile(des_path)  # type: ignore
        logger.info(f"Clip length: {mv_clip.duration}")
        result["path_to_file"] = str(des_path)
        result["clip_length_seconds"] = mv_clip.duration
    except OSError as exception:
        logger.error(f"Error extracting audio: {str(exception)}")
    return result


