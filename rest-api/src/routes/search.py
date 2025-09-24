from fastapi import APIRouter, HTTPException, Request
from helpers.models import SearchRequest, CreateProviderRequest, CreateServiceRequest

router = APIRouter(tags=["Search"])

@router.post("/search")
async def create_search(request: SearchRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client
        
        # Build the search request data from the new model structure
        request_data = {
            "consumer_id": request.consumer_id,
            "service_query": request.service_query,
            "provider_query": request.provider_query
        }
        
        result = grpc_client.create_search(request_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create-provider")
async def create_provider(request: CreateProviderRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client

        request_data = {
            "id": request.id,
            "name": request.name,
            "type": request.type,
            "available_resources": request.available_resources
        }

        result = grpc_client.create_provider(request_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create-service")
async def create_service(request: CreateServiceRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client

        request_data = {
            "provider_id": request.provider_id,
            "cpu": request.cpu,
            "ram": request.ram,
            "location": request.location,
            "storage": request.storage,
            "maximumULthroughput": request.maximumULthroughput,
            "maximumDLthroughput": request.maximumDLthroughput,
            "minPrice": request.minPrice,
            "maxPrice": request.maxPrice
        }
        result = grpc_client.create_service(request_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))