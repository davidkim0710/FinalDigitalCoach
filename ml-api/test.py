import uuid
from helpers.score import create_answer


def get_results():
    content = {
        # Add an mp4 sample file and rename to "video.mp4"
        "fname": "test.mp4",
        "rename": str(uuid.uuid4()) + ".mp3",
        # "user_id": user_id,
        # "question_id": question_id,
        # "answer_id": answer_id
    }
    result = create_answer(content)
    
    print(result)


get_results()
