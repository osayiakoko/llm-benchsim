# Simulation Service

## Overview

This service simulates LLM performance metrics and stores the results in a database. It runs periodically, an hour by default or configured simulation interval.

## Project Description
This service simulates the following performance metrics for different LLM models:
- TTFT: time to first token
- TPS: tokens per second
- e2e_latency: end-to-end latency
- RPS: requests per second

The simulation results are stored in a PostgreSQL database, allowing for historical analysis and comparison of model performance over time. In addition, each simulation is sent to the benchmarking service via a RabbitMQ queue.

### **Message Structure**

Sample simulation results

```json
[
  {
    "llm_name": "GPT-4o",
    "metric": "TTFT",
    "values": [
      1.314910917069979,
      0.14752043492306718,
      0.6225557049013265,
      0.5241004024827632,
      1.4992953069116235,
    ],
    "timestamp": "2024-09-27T11:29:13.291565Z"
  }
{
    "llm_name": "GPT-4o",
    "metric": "TPS",
    "values": [
      11.033291974853768,
      71.35393321239172,
      58.32732973679156,
      34.014267095728854,
      20.03969562362888,
    ],
    "timestamp": "2024-09-27T11:29:13.291565Z"
  }
 {
    "llm_name": "GPT-4o",
    "metric": "e2e_latency",
    "values": [
      4.86048315778138,
      1.248399997717613,
      2.685385064528233,
      2.3046813164725366,
      0.7638592998748052,
    ],
    "timestamp": "2024-09-27T11:29:13.291565Z"
  }
]
```

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
- `LLM_MODELS_STR`: Comma-separated string of LLM models to simulate
- `NUM_DATA_POINTS`: Number of data points to generate per simulation
- `RANDOM_SEED`: Seed for random number generation
- `SIMULATION_INTERVAL`: Interval between simulations in seconds

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
| id | INTEGER | Primary key |
| llm_name | VARCHAR(50) | Name of the LLM model |
| metric | VARCHAR(20) | Name of the metric |
| values | ARRAY(FLOAT) | Simulated values |
| timestamp | TIMESTAMP WITH TIME ZONE | Time of the simulation |

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
   docker run -d --env-file .env simulation-service:latest
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