import time
import logging
from typing import Never

logger = logging.getLogger(__name__)

ALL_JOBS = set()
RESULT_ENCODING = "result".encode("utf-8")
FINISHED_ENCODING = "finished".encode("utf-8")


def _update_all_jobs(redis_conn):
    """
    Get finished jobs from Redis.
    """
    try:
        keys = redis_conn.keys("rq:job:*")
        for key in keys:
            key_str = key.decode("utf-8")
            status = redis_conn.hgetall(key)
            status = {k.decode("utf-8"): v for k, v in status.items()}
            if status.get("status") == FINISHED_ENCODING:
                yield key_str
    except Exception as e:
        logger.error(f"Error updating jobs: {str(e)}")


def poll_connection(redis_connection) -> Never:
    """
    Continuously poll the Redis connection for jobs.
    """
    while True:
        try:
            finished_jobs = list(_update_all_jobs(redis_connection))
            if finished_jobs:
                logger.info(f"Finished jobs: {len(finished_jobs)} {finished_jobs}")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error in poll_connection: {str(e)}")
            time.sleep(5)
