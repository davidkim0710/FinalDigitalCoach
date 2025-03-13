import uuid
import os
import logging
import shutil
import json
import ast
from backend.tasks.score import create_answer
from backend.utils import get_video_dir, get_output_dir

DIR_NAME = os.path.dirname(__file__)
OUTPUT_DIR = get_output_dir()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_video_output():
    # Create test data directory if it doesn't exist
    os.makedirs(os.path.join(DIR_NAME, "data"), exist_ok=True)

    # Ensure test video is accessible
    test_video = os.path.join(DIR_NAME, "data", "test2.mp4")
    assert os.path.exists(test_video), f"Test video file not found: {test_video}"

    # Copy the test video to our video directory for processing
    video_dir = get_video_dir()
    temp_video = os.path.join(video_dir, "test2.mp4")
    shutil.copy2(test_video, temp_video)

    # Generate a unique audio filename
    audio_filename = f"{uuid.uuid4()}.mp3"
    # _audio_path = get_audio_path(audio_filename)

    # Create content dictionary with the temp paths
    content = {
        "fname": temp_video,
        "rename": audio_filename,
    }

    result = create_answer(content)
    logger.info(f"Processing result: {result}")

    # Write result to log file
    test_path = os.path.join(DIR_NAME, "test.log")
    with open(test_path, "w") as f:
        f.write(str(result))
        f.flush()
    # to make sure the json file is correct, cat test.json | jq to pretty print
    with open(test_path, "r") as f:
        result = ast.literal_eval(f.read())
    with open(os.path.join(DIR_NAME, "test.json"), "w") as f:
        json.dump(result, f, indent=4)

    # Assert that we have a valid result
    assert result is not None, "Processing result should not be None"
    # Fix for the error - check if result is a dictionary before using .get()
    if isinstance(result, dict):
        assert (
            "errors" not in result
        ), f"Processing failed with errors: {result.get('errors')}"
    else:
        assert "errors" not in str(
            result
        ), f"Processing failed with errors in result: {result}"
