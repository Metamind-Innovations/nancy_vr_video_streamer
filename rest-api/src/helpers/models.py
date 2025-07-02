from pydantic import BaseModel
from typing import Dict, Any

class NonceRequest(BaseModel):
    did: str

class PresentationRequest(BaseModel):
    credential: str
    nonce: str

class VerificationRequest(BaseModel):
    value: str

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