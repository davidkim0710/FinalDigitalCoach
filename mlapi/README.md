# ML API Backend
## Project Structure
The project has been reorganized into logical packages:
```
backend/
├── redisStore/          # Redis connection, queue management and worker
├── server/         # Flask server, routes and API endpoints
├── tasks/          # ML processing tasks and modules
│   ├── helpers/    # Helper functions for tasks
│   └── models/     # ML models
└── tests/          # Test suite
```
## Development
### Installation
To set up the development environment:
```bash
# Clone the repository
`git clone <repository-url> && cd mlapi`
# Install dependencies
`cd backend && pip install -r requirements.txt`
```
or using [uv](https://docs.astral.sh/uv/getting-started/installation)
```bash
uv sync
```
or poetry or by running `python setup.py` which just does `pip install -r requirements.txt` 
### Running the Server
```bash
# Run the Flask server
cd backend && python main.py
```
### Running the Worker
```bash
# Run the Redis worker
rq worker high default low
```
### Running Tests
```bash
# Run all tests
pytest
# Run specific tests
pytest backend/tests/test_processing.py
```
## Docker
To run the full stack download docker-desktop then run:
```bash
docker-compose up -d
```
## Environment Variables
- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_PASSWORD`: Redis password
- `REDIS_URL`: Redis URL (alternative to host/port/password)
- `AAPI_KEY`: Assembly AI API key for speech processing
## Temporary Files
Temporary files are managed in standardized locations(not atm):
- `/backend/tmp/data`: General temporary data files
- `/backend/tmp/audio`: Audio files (.mp3)
- `/backend/tmp/video`: Video files (.mp4)
- `/backend/tmp/output`: Processed output files
## Feedback Systems

### Competency-Based Feedback
The system now implements a competency-based feedback approach that provides:
- Practical, actionable feedback on interview skills
- Analysis of communication clarity, confidence, and engagement
- Specific recommendations for improvement
- Numerical scores for each competency area

This approach replaces the previous Big 5 personality trait scoring with more directly applicable feedback for interview preparation.

## TODO
- Recreate the structured score NLP model. The results show a 62% validation ON THE TEST SET. That is barely better than a coinflip...
- Enhance competency feedback with more specialized metrics for different interview types
- Add benchmark comparison to successful interviews in similar roles