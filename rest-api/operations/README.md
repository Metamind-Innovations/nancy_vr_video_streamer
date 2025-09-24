# Docker Deployment for Nancy-gRPC

This directory contains Docker configuration files for building and deploying the Nancy-gRPC application.

## Files

- `Dockerfile`: Defines the container image for the application
- `docker-compose.yml`: Orchestrates the deployment of the application

## Environment Variables

The application uses the following environment variables:

- `GRPC_HOST`: Host address for the gRPC server (default: 195.37.154.23)
- `GRPC_PORT`: Port for the gRPC server (default: 8881)
- `UVICORN_HOST`: Host address for the FastAPI server (default: 0.0.0.0)
- `UVICORN_PORT`: Port for the FastAPI server (default: 8000)

You can set these variables in a `.env` file in the `src` directory. The docker-compose configuration will load this file automatically.

### Example .env file

```
GRPC_HOST=195.37.154.23
GRPC_PORT=8881
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

## Building and Running

### Build the Docker image

```bash
# From the project root directory
docker build -t nancy-grpc -f operations/Dockerfile .

# To build without using cache
docker build --no-cache -t nancy-grpc -f operations/Dockerfile .
```

### Run with Docker Compose

```bash
# From the operations directory
docker-compose up -d
```

This will start the Nancy-gRPC service on port 8000.

### Stop the service

```bash
# From the operations directory
docker-compose down
```

## Development with Docker

The docker-compose configuration mounts the `src` directory as a volume, allowing you to make changes to the code without rebuilding the image. However, you may need to restart the container for changes to take effect:

```bash
docker-compose restart nancy-grpc
``` 
