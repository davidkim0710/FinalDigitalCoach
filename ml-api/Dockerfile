# Use Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
# Copy Pipfile and Pipfile.lock first for dependency caching
COPY Pipfile Pipfile.lock ./

# Install Pipenv
RUN pip install pipenv

# Install project dependencies
RUN pipenv install --deploy --system

# Copy the rest of the application files
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to start the Flask API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

