import json
from fastapi import APIRouter, HTTPException, Request, Query
from helpers.models import PresentationRequest, VerificationRequest, CredentialRequest

router = APIRouter(tags=["Verification"])

@router.get("/nonce")
async def get_nonce(req: Request, did: str = Query(..., description="The DID to get nonce for")):
    try:
        grpc_client = req.app.state.grpc_client
        payload = {"data": {"did": did}}
        result = grpc_client.get_nonce(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/presentation")
async def create_presentation(request: PresentationRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client
        
        # Parse the credential JSON string into a dictionary
        try:
            credential_dict = json.loads(request.credential)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in credential field")
        
        result = grpc_client.create_presentation(
            credential=credential_dict,
            nonce=request.nonce
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify")
async def verify_credential(request: VerificationRequest, req: Request):
    try:
        grpc_client = req.app.state.grpc_client
        credential = json.loads(request.value)
        result = grpc_client.verify_credential(credential)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/request")
async def request_credential(request: CredentialRequest, req: Request):
    """Request a credential from an issuer."""
    try:
        grpc_client = req.app.state.grpc_client
        
        # Build the credential parameter from the nested structure
        cred_param = {
            "holderDID": request.credParam.holderDID,
            "claims": request.credParam.claims,
            "vmId": request.credParam.vmId,
            "signature": request.credParam.signature
        }
        
        result = grpc_client.request_credential(request.issuerAddress, cred_param)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 