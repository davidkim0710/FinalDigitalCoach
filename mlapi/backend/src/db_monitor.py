from typing import Callable, Never
import time
import os
from redis import Redis
from rq.job import Job
from rq.queue import Queue
import logging


ALL_JOBS = set()
RESULT_ENCODING = "result".encode("utf-8")
FINISHED_ENCODING = "finished".encode("utf-8")

logger = logging.getLogger(__name__)

""" Redis functions """


def get_redis_con() -> Redis:
    """
    Create a secure Redis connection with authentication.
    
    Returns:
        Redis: Authenticated Redis connection
    """
    try:
        redis_conn = Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=False,
            socket_timeout=5,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30
        )
        # Test the connection
        return redis_conn
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise


def get_queue(queue_name="default") -> Queue:
    """
    Get a Queue instance with the specified name.
    
    Args:
        queue_name (str): Name of the queue
    
    Returns:
        Queue: RQ Queue instance
    """
    conn = get_redis_con()
    return Queue(name=queue_name, connection=conn)


def add_task_to_queue(task: Callable, *args, depends_on=None) -> Job:
    """
    Add a task to the Redis queue with proper error handling.
    
    Args:
        task: The task function to be executed
        *args: Arguments to pass to the task
        depends_on: Optional dependency jobs
        
    Returns:
        Job: The enqueued job
    """
    try:
        # Always use the default queue
        queue = get_queue("default")
        job = queue.enqueue(task, *args, depends_on=depends_on)
        
        logger.info(f"Task {task.__name__} enqueued with job ID: {job.id}")
        return job
    except Exception as e:
        logger.error(f"Failed to enqueue task: {str(e)}")
        raise

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
