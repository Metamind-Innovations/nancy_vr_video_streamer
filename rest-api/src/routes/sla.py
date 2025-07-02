from fastapi import APIRouter, HTTPException, Request
from helpers.models import SLASignRequest

router = APIRouter(prefix="/sla", tags=["SLA"])

@router.post("/sign")
async def sla_sign(request: SLASignRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.sla_sign(request.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/init")
def subscribe_to_sla_init(req: Request):
    grpc_client = req.app.state.grpc_client
    result = grpc_client.subscribe_to_sla_init()
    return result

@router.get("/events/signing")
def subscribe_to_sla_signing(req: Request):
    grpc_client = req.app.state.grpc_client
    result = grpc_client.subscribe_to_sla_signing()
    return result