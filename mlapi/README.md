# ML API

Machine Learning API for video analysis, providing audio sentiment analysis, facial emotion detection, and more.

## Features

- Audio sentiment analysis using AssemblyAI
- Facial emotion detection using DeepFace
- STAR feedback evaluation
- Big Five personality traits analysis
- Task queuing with Redis RQ
- Multiple worker queues for parallel processing

## Getting Started with Docker

The easiest way to run the application is using Docker Compose.

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the application

1. Clone the repository
2. Navigate to the project directory
3. Start the services using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- The main API server on port 8000
- Redis database for job queuing
- Multiple workers for processing different priority tasks
- A monitoring service for job status

### Accessing the API

Once running, you can access:
- API documentation: http://localhost:8000/docs
- API base endpoint: http://localhost:8000/

## Service Architecture

The application is composed of several services:

- **API Server**: FastAPI application exposing the REST endpoints
- **Redis**: Queue manager and job storage
- **High-Priority Workers**: Process video analysis tasks (2 replicas)
- **Default Workers**: Handle standard priority tasks (3 replicas)
- **Low-Priority Workers**: Handle background and non-urgent tasks
- **Monitor**: Tracks job progress and status

## Development Environment

If you prefer to run the application locally without Docker:

1. Install Python 3.12 or higher
2. Install Redis locally
3. Install dependencies: `pip install -e .`
4. Start the API server: `python main.py`
5. Start workers in separate terminals: `python -m redisStore.worker high default low`

## Testing

Run tests using pytest:

```bash
pytest
```

## Environment Variables

Configure the application using environment variables:

- `REDIS_HOST`: Redis host (default: "localhost")
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_PASSWORD`: Redis password (optional)
- `REDIS_URL`: Complete Redis URL (optional, overrides other Redis settings)
- `WORKERS_COUNT`: Number of worker processes (used in Docker setup)
EOF < /dev/null