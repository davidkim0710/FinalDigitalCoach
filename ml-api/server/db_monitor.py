import time
import os
import ast
import requests

# Set to keep track of all jobs
ALL_JOBS = set()
# Encoded strings for result and finished status
RESULT_ENCODING = "result".encode("utf-8")
FINISHED_ENCODING = "finished".encode("utf-8")


def _update_all_jobs(redis_conn):
    # Get all keys from the Redis database
    keys = redis_conn.keys("*")
    for key in keys:
        key_str = key.decode("utf-8")
        # Check if the key represents a job
        if "rq:job" in key_str:
            # Get the job's status
            status = redis_conn.hgetall(key)
            status = {key.decode("utf-8"): value for key,
                      value in status.items()}
            # If the job is finished, add it to the set of all jobs
            if status["status"] == FINISHED_ENCODING:
                ALL_JOBS.add(key)


def _send_job_results(redis_conn):
    # Iterate over all finished jobs
    for job in ALL_JOBS:
        # Get the result of the job
        result = redis_conn.hget(job, RESULT_ENCODING)
        # Convert the result from byte array to string
        b_arr = bytearray(result)
        str_res = "".join(chr(a) for a in b_arr)
        str_res = str_res[16:]
        str_res = str_res[:-2]
        # Parse the string result to a Python object
        parsed_res = ast.literal_eval(str_res)
        # Get the Firebase endpoint from environment variables
        firebase_endpnt = os.getenv("FIREBASE_FUNCTIONS_ENDPOINT")
        # Send the result to the Firebase endpoint
        # requests.post(firebase_endpnt, data=parsed_res)
    # Clear the set of all jobs after sending results
    ALL_JOBS.clear()


def poll_connection(redis_connection):
    # Run indefinitely
    while True:
        # Update the list of all jobs
        _update_all_jobs(redis_connection)
        # If there are finished jobs, send their results
        if len(ALL_JOBS) > 0:
            _send_job_results(redis_connection)
        # Wait for 5 seconds before the next iteration
        time.sleep(5)
