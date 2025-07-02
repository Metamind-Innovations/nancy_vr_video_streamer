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

## Testing with Mock gRPC Server

For development and testing without access to the actual gRPC server, use the mock server:

```bash
cd src
python start_with_mock.py
```

This will:
- Start a mock gRPC server on port 50051
- Start the FastAPI server on port 8000
- Provide realistic mock responses for all endpoints

## API Endpoints

### Nonce
- **POST** `/nonce`
  - Get a nonce from the verifier wallet
  - Request body: 
    ```json
    {
      "did": "string"
    }
    ```

### Presentation
- **POST** `/presentation`
  - Create a verifiable presentation
  - Request body:
    ```json
    {
      "credential": {}, // Dictionary containing credential data
      "nonce": "string"
    }
    ```

### Verification
- **POST** `/verify`
  - Verify a credential
  - Request body:
    ```json
    {
      "credential": {} // Dictionary containing credential data
    }
    ```

### Search
- **POST** `/search`
  - Create a search request
  - Request body:
    ```json
    {
      "request": {} // Dictionary containing search parameters
    }
    ```

### SLA
- **POST** `/sla/sign`
  - Sign an SLA
  - Request body:
    ```json
    {
      "data": {} // Dictionary containing SLA data
    }
    ```

- **GET** `/sla/events/init`
  - Subscribe to SLA initialization events
  - Returns a stream of events with the following structure:
    ```json
    {
      "name": "string",
      "payload": {
        "id": "unique-sla-id",
        "value": "sla value in json format",
        "provider_id": "provider-id",
        "consumer_id": "consumer-id",
        "provider_sig": "provider signature",
        "consumer_sig": "consumer signature"
      }
    }
    ```

- **GET** `/sla/events/signing`
  - Subscribe to SLA signing events
  - Returns a stream of events with the same structure as `/sla/events/init`

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
