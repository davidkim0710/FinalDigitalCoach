from rq import Worker
import backend.redisStore.myConnection as myConnection

listen = ["high", "default", "low"]
conn = myConnection.get_redis_con()

if __name__ == "__main__":
    worker = Worker(listen, connection=conn)
    worker.work()
