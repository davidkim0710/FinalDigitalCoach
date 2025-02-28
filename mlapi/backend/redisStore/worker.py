from rq import Worker
from .myConnection import get_redis_con

# List of queues to listen for jobs on
listen = ["default"]


def create_worker():
    """Create and return a worker instance"""
    conn = get_redis_con()
    return Worker(listen, connection=conn)


if __name__ == "__main__":
    worker = create_worker()
    worker.work()

