import os
from generate_grpc import generate_grpc_code
from fastapi import FastAPI

generate_grpc_code()

from contextlib import asynccontextmanager
from grpc_client import DltGatewayClient
from routes import sla_router, verification_router, search_router, did_router
from dotenv import load_dotenv
import uvicorn


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Initialize gRPC client
grpc_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global grpc_client
    grpc_client = DltGatewayClient()
    app.state.grpc_client = grpc_client
    yield

    if grpc_client:
        grpc_client.channel.close()

app = FastAPI(title="DLT Gateway REST API", lifespan=lifespan)

# Include routers
app.include_router(sla_router)
app.include_router(verification_router)
app.include_router(search_router)
app.include_router(did_router)

if __name__ == "__main__":
    uvicorn_host = os.getenv("UVICORN_HOST")
    uvicorn_host = uvicorn_host if uvicorn_host else "0.0.0.0"
    uvicorn_port = os.getenv("UVICORN_PORT")
    uvicorn_port = int(uvicorn_port) if uvicorn_port else 8000
    uvicorn.run(app, host=uvicorn_host, port=uvicorn_port) 
