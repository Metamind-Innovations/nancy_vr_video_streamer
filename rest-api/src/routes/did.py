from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/did", tags=["DID"])

@router.get("/list")
async def list_dids(req: Request):
    """List all DIDs saved in the wallet."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.list_dids()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 