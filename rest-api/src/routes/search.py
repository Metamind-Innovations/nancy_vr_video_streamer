from fastapi import APIRouter, HTTPException, Request
from helpers.models import SearchRequest

router = APIRouter(tags=["Search"])

@router.post("/search")
async def create_search(request: SearchRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.create_search(request.request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))