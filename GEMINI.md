# Project Overview

This project is a FastAPI-based API service designed to provide information about room availability at the University of the West Indies, Cavehill Campus. It uses MongoDB as its database and Pydantic for data modeling and validation.

The API exposes several endpoints to query for room schedules, find free rooms, and retrieve lists of available rooms and course prefixes.

# Building and Running

## Prerequisites

- Python 3.10+
- A running MongoDB instance

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project with the following content:
    ```
    MONGO_URL=<your-mongodb-connection-string>
    DB_NAME=<your-database-name>
    ```

## Running the application

To run the application, use the following command:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Testing

There are no tests in this project yet.

# Development Conventions

- **Code Style:** The project follows the standard PEP 8 style guide for Python code.
- **API Versioning:** The API is versioned, with the current version being `v1`.
- **Modularity:** The application is structured into modules for different concerns (e.g., `routers`, `models`, `schemas`, `services`).
- **Dependency Injection:** FastAPI's dependency injection system is used to manage dependencies, such as query parameters and database connections.
- **Data Validation:** Pydantic models are used to define the data schemas and validate incoming request data and outgoing responses.
