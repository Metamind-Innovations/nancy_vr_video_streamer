#!/usr/bin/env python3
"""
Script to start the mock gRPC server and FastAPI application together
"""

import uvicorn
from mock_grpc_server import MockGrpcServer
from main import app
import os

def main():
    print("Starting mock gRPC server...")
    
    # Start mock gRPC server
    mock_server = MockGrpcServer(port=50051)
    mock_server.start()
    
    print("Mock gRPC server started on port 50051")
    print("Starting FastAPI server...")
    
    uvicorn_host = os.getenv("UVICORN_HOST")
    uvicorn_host = uvicorn_host if uvicorn_host else "0.0.0.0"
    uvicorn_port = os.getenv("UVICORN_PORT")
    uvicorn_port = int(uvicorn_port) if uvicorn_port else 8000
    
    try:
        uvicorn.run(app, host=uvicorn_host, port=uvicorn_port)
    except KeyboardInterrupt:
        print("\nShutting down...")
        mock_server.stop()
        print("Servers stopped")

if __name__ == "__main__":
    main() 