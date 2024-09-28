# Benchmarking Service

## Overview

This service calculates and stores rankings for LLM performance metrics. It consumes messages from a RabbitMQ queue to trigger the benchmarking process.

## Project Description

The Benchmarking Service processes performance metrics for different LLM models, including:
- TTFT: time to first token
- TPS: tokens per second
- e2e_latency: end-to-end latency
- RPS: requests per second

The service calculates rankings based on these metrics and stores the results in a PostgreSQL database.

## Prerequisites

- Python 3.11+
- PostgreSQL
- RabbitMQ
- Docker 
- Kubernetes

## Setup

1. Clone the repository
2. Copy `.env.sample` to `.env` and update the variables as needed
3. Install dependencies: `make install`
4. Run database migrations: `make migrate`

## Environment Variables

Key variables include:

- `POSTGRES_*`: Database connection details
- `RABBITMQ_*`: RabbitMQ connection details
- `LOG_FILE`: File path for logging
- `CONSOLE_LOGGING`: Enable/disable console logging

Refer to `.env.sample` for a complete list of required environment variables.

## Running the Service

### Locally

To run the service locally:

```bash
make run
```

### Using Docker

To build and run the service using Docker:

1. Build the Docker image:
   ```bash
   make docker-build
   ```
2. Run the container:
   ```bash
   docker run -d --env-file .env benchmarking-service:latest
   ```

### On Kubernetes using kubectl

1. Ensure your Kubernetes cluster is set up and `kubectl` is configured
2. Install the K8s manifests:
   ```bash
   make k8-apply
   ```

## Testing

Run tests with:
```bash
make test
```

## Logging

Logs are written to the file specified by the `LOG_FILE` environment variable. Console logging can be enabled/disabled using the `CONSOLE_LOGGING` environment variable.

## Configuration

All configuration is done through environment variables. See `src/config.py` for available options.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.