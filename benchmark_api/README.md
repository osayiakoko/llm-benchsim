# Benchmark API

## Overview

Benchmark API is a FastAPI-based service designed to provide performance benchmarks for various LLM (Language Model) metrics. It offers a RESTful API to retrieve benchmark results, utilizing PostgreSQL for data storage and Redis for caching.

## Features

- Retrieve benchmark results for different LLM metrics
- API Key authentication
- Caching with Redis for improved performance
- Logging with rotation
- Containerized with Docker
- Kubernetes manifest
- Prometheus and Grafana integration for monitoring


## API Endpoints

The following endpoints are available:
- `GET /`: Alternate endpoint to get loggedin user details.
- `GET /docs`: Alternate endpoint to get loggedin user details.
- `GET /metrics`: Alternate endpoint to get loggedin user details.
- `GET /api/v1/benchmark/{metric}`: Retrieve a list of all users in the system.

### **Message Structure**

Sample data from the API 

```json
// GET /api/v1/benchmark/{metric}
{
  "success": true,
  "data": [
    {
      "id": "fe860508-ecf7-4f57-941d-a0dbbe63cfa4",
      "metric": "TTFT",
      "llm_name": " Llama 3.1 405",
      "mean_value": 1.0281117694509072,
      "rank": 1,
      "timestamp": "2024-09-27T08:57:17.739976Z"
    },
    {
      "id": "9b17e1e9-592a-45ee-bce9-a265f333ea55",
      "metric": "TTFT",
      "llm_name": " Claude 3.5 Sonnet",
      "mean_value": 1.064995727486063,
      "rank": 2,
      "timestamp": "2024-09-27T08:57:17.739976Z"
    },
    {
      "id": "8c50767f-4a7e-47e7-8efa-13ce637a65c7",
      "metric": "TTFT",
      "llm_name": "GPT-4o",
      "mean_value": 1.0738677434628694,
      "rank": 3,
      "timestamp": "2024-09-27T08:57:17.739976Z"
    }
  ],
  "message": null
}
// GET /api/v1/benchmark/{metric} (No/Invalid X-API-KEY provided)
{
    "success": false,
    "data": null,
    "message": "Could not validate API key"
}
```

## Project Structure

```
benchmark_api/
│
├── alembic/                 # Database migrations
├── grafana/                 # Grafana configuration
├── helm/                    # Helm chart for Kubernetes deployment
├── k8s/                     # Kubernetes manifests
├── prometheus/              # Prometheus configuration
├── src/
│   ├── api/
│   │   ├── routers/         # API routes and endpoints
│   │   ├── dependencies.py  # Dependency injection
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── response.py      # Custom response formats
│   ├── core/                # Core functionality (security, logging, etc.)
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # Data access layer
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic layer
│   ├── config.py            # Configuration settings
│   ├── create_app.py        # FastAPI application setup point
│   ├── database.py          # Database connection setup
│   └── main.py              # FastAPI application entry point
│
├── tests/                   # Unit and integration tests
├── .env.sample              # environment variables
├── alembic.ini              # migration configuration
├── Dockerfile               # Docker build instructions
├── Makefile                 # Make file commands
├── README.md                # this file
├── docker-compose.yml       # Docker Compose configuration
└── requirements.txt         # Python dependencies
```

## Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Docker (for containerization)
- Kubernetes and Helm

## Setup

1. Clone the repository
2. Create and activate a virtual environment `python -m venv venv`
3. Copy `.env.sample` to `.env` and update the variables as needed
4. Install dependencies: `make install`
5. Run database migrations: `make migrate`

## Environment Variables

Key variables include:

- `POSTGRES_*`: Database connection details
- `REDIS_*`: Redis connection details
- `CACHE_EXPIRATION`: Expiration time for the Redis cache in seconds
- `API_KEY`: API key for authentication

Refer to `.env.sample` for a complete list of required environment variables.

## Running the Service

### Locally

#### Database Migrations

- Create a new migration: `make migrations msg="Your migration message"`
- Apply migrations: `make migrate`

#### Database Schema

The database schema includes the following table:

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| id | UUID | Primary key, generated on insertion |
| metric | VARCHAR(20) | Name of the metric |
| llm_name | VARCHAR(50) | Name of the LLM model |
| mean_value | FLOAT | Mean value of the simulated metric |
| rank | INTEGER | Rank of the LLM model for the given metric |
| timestamp | TIMESTAMP WITH TIME ZONE | Time of the simulation |

To run the service locally:

```bash
make run
# or
make dev
```

### Using Docker

To build and run the service using Docker:


1. Build the Docker image:
   ```bash
   make docker-build
   ```
2. Run the container:
   ```bash
   docker run -d --env-file .env benchmark-api-service:latest

The API will be available at `http://localhost:8000`.

### On Kubernetes using kubectl

1. Ensure your Kubernetes cluster is set up and `kubectl` is configured
2. Install the K8s manifests:
   ```bash
   # Add the Prometheus community Helm repository:
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   # 	Install the Prometheus Operator:
   helm install prometheus-operator prometheus-community/kube-prometheus-stack
   # Apply k8s manifest
   make k8-apply
   ```

## Testing

Run tests with:
```bash
make test
```

## Logging

Logs are written to the file specified by the `LOG_FILE` environment variable. Console logging can be enabled/disabled using the `CONSOLE_LOGGING` environment variable.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

The API uses API Key authentication. Include the `X-API-Key` header in your requests with the appropriate key.

## Monitoring

- Prometheus is configured to scrape metrics from the application.
- Grafana dashboards can be set up to visualize these metrics.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.