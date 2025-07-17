from fastapi import APIRouter, HTTPException, Request, Query

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
    
@router.get("/lookupdid")
async def lookup_did(req: Request, value: str = Query(..., description="DID to look up")):
    """Look up a DID document in the registry."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.lookup_did(value)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
