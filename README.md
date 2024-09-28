[![Simulation CI pipeline](https://github.com/osayiakoko/llm-benchsim/actions/workflows/simulation-ci-pipeline.yaml/badge.svg?branch=dev)](https://github.com/osayiakoko/llm-benchsim/actions/workflows/simulation-ci-pipeline.yaml)
[![Benchmarking CI pipeline](https://github.com/osayiakoko/llm-benchsim/actions/workflows/benchmarking-ci-pipeline.yaml/badge.svg?branch=dev)](https://github.com/osayiakoko/llm-benchsim/actions/workflows/benchmarking-ci-pipeline.yaml)
[![Benchmark API CI pipeline](https://github.com/osayiakoko/llm-benchsim/actions/workflows/benchmark_api-ci-pipeline.yaml/badge.svg?branch=dev)](https://github.com/osayiakoko/llm-benchsim/actions/workflows/benchmark_api-ci-pipeline.yaml)
[![AWS deployment pipeline](https://github.com/osayiakoko/llm-benchsim/actions/workflows/aws-deployment-pipeline.yaml/badge.svg?branch=dev)](https://github.com/osayiakoko/llm-benchsim/actions/workflows/aws-deployment-pipeline.yaml)

# LLM Benchmark Simulation

This README provides instructions for deploying the LLM Benchmark Simulation Application to Amazon EKS (Elastic Kubernetes Service) using Helm and GitHub Actions.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Repository Structure](#repository-structure)
4. [Helm Chart](#helm-chart)
5. [GitHub Actions Workflow](#github-actions-workflow)
6. [Deployment Steps](#deployment-steps)
7. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
8. [Cleaning Up](#cleaning-up)
8. [License](#license)

## Overview

The LLM Benchmark Simulation Application consists of three main components:

1. [Simulation Service](./simulation/)
2. [Benchmarking Service](./benchmarking/)
3. [Benchmark API](./benchmark_api/)

These services work together to simulate LLM usage, perform benchmarks, and provide an API for accessing benchmark results.

## Prerequisites

Before deploying the application, ensure you have the following:

- An AWS account with permissions to create and manage EKS clusters
- AWS CLI installed and configured
- kubectl installed
- Helm 3 installed
- An Amazon EKS cluster set up and running
- Amazon ECR repositories created for each service
- GitHub repository with your application code

## Repository Structure

Your repository should have the following structure:

```
.
├── .github
│   └── workflows
│       └── deploy-to-aws.yml
├── benchmark-api
│   └── Dockerfile
├── benchmarking
│   └── Dockerfile
├── simulation
│   └── Dockerfile
├── llm-benchsim-chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates
│       ├── benchmark-api
│       ├── benchmarking
│       ├── monitoring
│       ├── simulation
│       └── shared
└── README.md
```

## Helm Chart

The Helm chart (`llm-benchsim-chart`) defines the Kubernetes resources for deploying the application. Key files include:

- `Chart.yaml`: Metadata about the chart
- `values.yaml`: Default configuration values
- `templates/`: Kubernetes resource templates

Customize the `values.yaml` file to match your specific requirements.

## GitHub Actions Workflow

The workflow file (`.github/workflows/aws-deployment-pipeline.yml`) automates the deployment process to aws. It performs the following steps:

1. Builds Docker images for each service
2. Pushes images to Amazon ECR
3. Deploys the application to EKS using Helm

## Deployment Steps

1. **Set up GitHub Secrets**

   Add the following secrets to your GitHub repository:

   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `BENCHMARKING_DB_PASSWORD`
   - `SIMULATION_DB_PASSWORD`
   - `RABBITMQ_PASSWORD`

2. **Configure GitHub Actions Workflow**

   Update the `deploy-to-aws.yml` file with your specific AWS region and EKS cluster name:

   ```yaml
   env:
     AWS_REGION: us-west-2  # Change this to your AWS region
     EKS_CLUSTER_NAME: your-eks-cluster-name  # Change this to your EKS cluster name
   ```

3. **Trigger Deployment**

   The deployment will be triggered automatically on pushes to the `main` branch. You can also manually trigger the workflow from the GitHub Actions tab.

4. **Monitor Deployment**

   Watch the GitHub Actions workflow execution for any errors or successes.

## Monitoring and Troubleshooting

- Use `kubectl` to check the status of your pods:
  ```
  kubectl get pods
  ```

- View logs for a specific pod:
  ```
  kubectl logs <pod-name>
  ```

- Use AWS CloudWatch for monitoring if configured

## Cleaning Up

To remove the deployment:

1. Delete the Helm release:
   ```
   helm uninstall llm-benchsim-chart
   ```

2. Optionally, delete the EKS cluster if no longer needed:
   ```
   eksctl delete cluster --name=<your-cluster-name>
   ```

Remember to delete any associated AWS resources (e.g., load balancers, ECR repositories) to avoid unnecessary costs.

For any issues or questions, please open an issue in the GitHub repository.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.