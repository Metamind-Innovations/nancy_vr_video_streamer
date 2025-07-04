from pydantic import BaseModel
from typing import Dict, Any

class SearchRequest(BaseModel):
    request: Dict[str, Any]

class SLASignRequest(BaseModel):
    data: Dict[str, Any]

class CredentialParam(BaseModel):
    claims: str
    holderDID: str
    signature: str
    vmId: str

class CredentialRequest(BaseModel):
    credParam: CredentialParam
    issuerAddress: str 

class AuthorizationParam(BaseModel):
    holderDID: str
    vcId: str

class AuthorizationRequest(BaseModel):
    authParam: AuthorizationParam
    verifierAddress: str

class SignMessageRequest(BaseModel):
    did: str
    payload: str
    vmId: str

class VerifyMessageRequest(BaseModel):
    did: str
    payload: str
    signature: str
    vmId: str