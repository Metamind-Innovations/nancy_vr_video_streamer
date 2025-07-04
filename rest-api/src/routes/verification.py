import json
from fastapi import APIRouter, HTTPException, Request, Query
from helpers.models import CredentialRequest, AuthorizationRequest, SignMessageRequest, VerifyMessageRequest

router = APIRouter(tags=["Verification"])

@router.post("/request_credential")
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
    
@router.get("/show_credential")
async def show_credential(req: Request, value: str = Query(..., description="Credential to get")):
    """Get a credential from the wallet."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.show_credential(value)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/list_credentials")
async def list_credentials(req: Request):
    """Get a credential from the wallet."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.list_credentials()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/request_authorization")
async def request_authorization(request: AuthorizationRequest, req: Request):
    """Request an authorization from an issuer."""
    try:
        grpc_client = req.app.state.grpc_client
        
        # Build the authorization parameter from the nested structure
        auth_param = {
            "holderDID": request.authParam.holderDID,
            "vcId": request.authParam.vcId
        }
        
        result = grpc_client.request_authorization(request.verifierAddress, auth_param)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/sign_message")
async def sign_message(request: SignMessageRequest, req: Request):
    """Sign a message."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.sign_message(request.did, request.payload, request.vmId)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/verify_message")
async def verify_message(request: VerifyMessageRequest, req: Request):
    """Verify a message."""
    try:
        grpc_client = req.app.state.grpc_client
        result = grpc_client.verify_message(request.did, request.payload, request.signature, request.vmId)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/use_case_request")
async def redirect_to_verify(request: VerifyMessageRequest, req: Request):
    """Redirects to verify_message endpoint."""
    verifiableMessage = await verify_message(request, req)
    if verifiableMessage["result"] == True:
        #execute ote service provider endpoint for ListAuthorizationResults
        #get the authorization result and execute Desicion to grant service
        #res = fetch(ote(ListAuthorizationResults))
        res = True

        return res
    else:
        return False
