# ML API Backend
## Structure
The project has been reorganized:
```
backend/
├── redisStore/          # Redis connection, queue management and worker
├── server/         # Flask server, routes and API endpoints
├── tasks/          # ML processing, rq tasks, and modules
│   ├── helpers/    # Helper functions for tasks
│   └── models/     # ML models
└── tests/          # Test suite
```
## NOTE: GPU Support
If you have a GPU check out installing the versions of `torch` that work for your machine. https://pytorch.org/get-started/locally/
Will allow the facial recognition model (FER) to run faster. You can see the versions I'm using in the `requirements.txt` or `pyproject.toml` file. Different versions for machines and GPUs afaik.
## Environment Variables (.env)
All you should have to do is set the `AAPI_KEY` and `REDIS_PASSWORD` if building docker locally.
Take a look at the `.env.example` file for a list of all the environment variables that can be set. 
- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_PASSWORD`: Redis password 
    - (Optional for building. can be taken out of `.env` file nd removed from docker-compose)
- `REDIS_URL`: Redis URL  
    - default: redis://redis:6379, this is what the worker will use when the docker container is run. I've put a fallback for a local redis instance in `worker.py` if this env varaible is not set but may not work on your machine if "localhost" or the port number is different.
- `AAPI_KEY`: Assembly AI API key for speech processing
    - Setting this to True will call the model from hugging face and change the `overall_score` in the response. Haven't tested this yet right now the structured score is just a flat value. 
## RECOMMENDED: Running with Docker
Pull the latest images from Docker Hub:
NOTE: Some issue with docker-desktop:4.38.0 and wsl make sure to use docker-desktop:4.39.0 bc they fixed the issue. [link](https://github.com/docker/for-win/issues/14583)
```bash
docker pull testmecs/digitalcoach-mlapi:latest
docker pull testmecs/digitalcoach-worker:latest
docker pull redis:7.0.8-bullseye 
```
Create your own `.env` file in `/mlapi`  and run:
```bash
docker-compose --env-file .env up -d
```
## Development
### Installation
To set up the development environment:
NOTE: Poetry will still work afaik you can use `poetry install` and `poetry shell`
**RECOMMENDED**: use [uv](https://docs.astral.sh/uv/getting-started/installation) package manager
```bash
uv sync # Installs all dependencies and creates .venv
```
Then run: 
```bash
source .venv/bin/activate 
```
Activates the virtual environment, deactivate with `deactivate`
#### Running the Server
```bash
# Run the Flask server
cd backend && python main.py
```
#### Running the Worker in a seperate terminal
```bash
# Run the Redis worker
rq worker high default low
```
#### Running Tests
```bash
# Run all tests
pytest
# Run specific tests
pytest backend/tests/test_processing.py
```
#### Building with Docker
After creating the `.env` file run, use the scripts I've created to rebuild the docker images on your machine. This could be useful maybe if you downloaded different GPU drivers but you still want to use docker or if you have added another dependency and want to use docker. 
```bash
scripts/buildnrun # Builds the docker images and runs the server
```
Go get a coffee or something. This will take a while.
```bash
scripts/cleanup # Cleans up the docker images
```
## TODO
### known issues
- When running with a test video, the data.csv file is not moved to output dir. `move_cv_files()` tries to fix this but doesn't work...
- Frontend videos might not work. 
### Improvements
- Make the `overall_score` more accurate. Requires lots of testing with example videos to see what feels right. If we want to use what we had before, ignore the `text-structure` feedback in the calculation and set it to a flat value of `40` and it will be same as before. 
- Better feedback sentences. Generate with AI?
