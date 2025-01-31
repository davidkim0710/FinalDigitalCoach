import uuid
from helpers.score import create_answer


def get_results():
    content = {
        # Add an mp4 sample file and rename to "video.mp4"
        "fname": "test2.mp4",
        "rename": str(uuid.uuid4()) + ".mp3",
    }
    result = create_answer(content)
    # Write result to log
    with open("test.log", "w") as f:
        f.write(str(result))


get_results()
