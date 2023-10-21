

# FastAPI MongoDB Metrics Service

This is a FastAPI application for managing messages and estimating metrics for those messages. It uses a MongoDB database to store message data and metric estimates.

## Features

- Create, read, update, and delete:
    - messages
    - sessions
    - feedbacks
    - reviews in the database.
- Estimate metrics for the chatbot

## Prerequisites

Before running the application, make sure you have the following installed:

- Python (3.10.13)
- Docker (optional, for containerization)

## Installation


1. Clone this repository to your local machine:

   ```bash
   git clone repo_url
   ```

2. Change into the project directory:

   ```bash
   cd chatlog-metrics-service
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory with the following content:

   ```env

    # For URI string creation

    MONGO_CHATLOG_USERNAME=nonroot
    MONGO_CHATLOG_PASSWORD=secret
    MONGO_CHAT_DB_HOST=172.191.159.98
    MONGO_CHAT_DB_PORT=27017

    # DB NAME
    MONGO_CHATLOG_DB_NAME=chatlog

    # MONGO  COLLECTIONS
    MONGO_CHATLOG_COLLECTION_MESSAGES=messages
    MONGO_CHATLOG_COLLECTION_SESSIONS=sessions
    MONGO_CHATLOG_COLLECTION_FEEDBACK=feedback
    MONGO_CHATLOG_COLLECTION_TICKETS=tickets


    ########### APP ENV ###########
    # Preshared api key for JWT generation
    API_KEY=58lJqzt7qVMe6Nd0LhnIPBzCHaDuYKC6k9g1WoBE2YOvosT56e
    # Algorithm used in the JWT generation
    ALG=HS512
   ```

   Replace `MONGO_VARS...` with the actual values to acces your MongoDB database.

   `API_KEY` and `ALG` are used in the backend to validate the Auth token send from the frontend and chatUI to avoid exposing the endpoints to the public.

## Running the Application

You can run the FastAPI application using Python or Docker.

### Using Python

1. Start the FastAPI application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be accessible at `http://localhost:8000`.

### Using Docker

Alternatively, you can run the application in a Docker container.

1. Build the Docker image:

   ```bash
   docker build -t chatlog-metrics-service .
   ```

2. Run a Docker container based on the image:

   ```bash
   docker run -d -p 8000:8000 --name chatlog-metrics-service chatlog-metrics-service
   ```

   The API will be accessible at `http://localhost:8000`.

## API Documentation

You can access the `Swagger documentation` for the API by navigating to `http://localhost:8000/docs` in your web browser.

## Project Structure

```
.
├── core
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── models.py
│   └── settings.py
├── Dockerfile
├── Documentation.pdf
├── FastAPI - Swagger UI.pdf
├── __init__.py
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── tree.txt
└── v1
    ├── app.py
    ├── __init__.py
    ├── routers
    │   ├── feedback.py
    │   ├── __init__.py
    │   ├── messages.py
    │   ├── metrics.py
    │   ├── sessions.py
    │   └── tickets.py
    └── utils
        ├── __init__.py
        ├── metric_utils.py
        └── utils.py
```

## Usage

You can use the API to perform CRUD operations on messages and estimate metrics for messages. Refer to the API documentation for details on the available endpoints and request payloads.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
