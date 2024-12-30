# My FastAPI App with PostgreSQL

This project demonstrates how to set up and run a FastAPI application with a PostgreSQL database using Docker and Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```
my_fastapi_app/
├── app/
│   ├── api/
│   │   └── endpoints.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── session.py
│   │   └── functions.py
│   ├── main.py
│   └── __init__.py
├── docker/
│   ├── docker-compose.yml
│   └── postgres/
│       └── Dockerfile
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

## Environment Variables

Ensure you have a `.env` file in the root of your project directory with the following content:

```
DATABASE_URL=postgresql+psycopg2://postgres:post123@db:5432/mydatabase
```

## Building and Running the Containers

### Step 1: Build the Docker Images

Navigate to the directory containing the `docker-compose.yml` file and build the Docker images:

```sh
cd docker
docker-compose build
```

### Step 2: Run the Docker Containers

Start the Docker containers using the following command:

```sh
docker-compose up
```

To run the containers in detached mode, add the `-d` flag:

```sh
docker-compose up -d
```

### Step 3: Verify the Setup

After running the containers, open your web browser and navigate to `http://localhost:8000` to access the FastAPI application.

### Step 4: Stopping the Docker Containers

To stop the Docker containers, use the following command:

```sh
docker-compose down
```

## Configuration Files

### `Dockerfile`

This file defines the Docker image for the FastAPI application.

```dockerfile
# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client and development packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the environment file into the container
COPY .env .env

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`

This file defines the services (FastAPI app and PostgreSQL) and how they interact.

```yaml
version: '3.9'

services:
  db:
    build:
      context: ./postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: post123
      POSTGRES_DB: mydatabase
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  web:
    build: ..
    container_name: fastapi_app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - app-network

networks:
  app-network:

volumes:
  postgres_data:
```

## Troubleshooting

If you encounter any issues, ensure that:
- Docker and Docker Compose are correctly installed.
- The `.env` file is correctly set up in the root of the project directory.
- The PostgreSQL server is running and accessible from the FastAPI container.

For further assistance, feel free to contact the project maintainer.

