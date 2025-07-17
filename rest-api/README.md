# DLT Gateway REST API

This is a REST API wrapper around the DLT Gateway gRPC service. It provides HTTP endpoints for interacting with the DLT Gateway service.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the `src` directory:
```bash
cd src
cp .env_example .env
```

4. Start the API server:

```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

The gRPC client is configured to connect to `localhost:50051` by default. To change this, modify the `.env` file or set the `GRPC_HOST` and `GRPC_PORT` environment variables.

Available environment variables:
- `GRPC_HOST`: gRPC server host (default: localhost)
- `GRPC_PORT`: gRPC server port (default: 50051)
- `UVICORN_HOST`: FastAPI server host (default: 0.0.0.0)
- `UVICORN_PORT`: FastAPI server port (default: 8000)