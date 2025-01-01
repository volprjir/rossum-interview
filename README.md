# Project Overview

This project contains services and tests for interacting with the Rossum API and Postbin service.
For this project I decided to use layer architecture.

## Assignment

For more details on the assignment, please refer to the [interview task](https://you.ashbyhq.com/rossum.ai/assignment/93c83154-d979-4aea-ae5e-3a33a560ffc9).

## Environment Configuration

Before running the project, you need to create a `.env` file in the root directory of the project. This file should contain the following parameters:

- `BASIC_AUTH_USERNAME`: The username for basic authentication.
- `BASIC_AUTH_PASSWORD`: The password for basic authentication.
- `ROSSUM_USERNAME`: The username for accessing the Rossum API.
- `ROSSUM_PASSWORD`: The password for accessing the Rossum API.
- `ROSSUM_API`: The base URL for the Rossum API.
- `POSTBIN_URL`: The URL for the Postbin service.
- `SERVER_PORT`: The port on which the server will run.

You can use the `.env.example` file as a template:

```dotenv
BASIC_AUTH_USERNAME=<username>
BASIC_AUTH_PASSWORD=<password>
ROSSUM_USERNAME=<rossum_username>
ROSSUM_PASSWORD=<rossum_password>
ROSSUM_API=<rossum_api_url_base>
POSTBIN_URL=<postbin_url>
SERVER_PORT=8000
```

## Running the Project

To run the project please follow the steps below:

1. Set up the .env file in the root directory of the project. You can use the .env.example file as a template

2. Build the docker image
```bash
docker build -t myapp .
```
3. Run the docker image
```bash
docker run -p 8000:8000 --env-file .env myapp
```

4. The server will be running on `http://localhost:<SERVER_PORT>`

To test the endpoints, you can use the following curl commands:

```bash
curl -X POST "http://localhost:<SERVER_PORT>/export/" -H "Content-Type: application/json" -d '{"queue_id": "your_queue_id", "annotation_id": "your_annotation_id"}' -u <BASIC_AUTH_USERNAME>:<BASIC_AUTH_PASSWORD>
```

## Testing the Project
To run all the tests use the following commands:
    
```bash
docker run --env-file .env myapp pytest
```
To run the integration test there is the `test_export_endpoint` from the `tests/test_full_flow.py` file, use the following command:
    
```bash
docker run --env-file .env myapp pytest tests/test_full_flow.py::test_export_endpoint
```