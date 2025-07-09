from pydantic import BaseModel
from typing import Dict, Any

class SearchRequest(BaseModel):
    consumer_id: str
    service_query: Dict[str, Any]
    provider_query: Dict[str, Any]

class SLASignRequest(BaseModel):
    slaId: str
    uid: str

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

class CreateProviderRequest(BaseModel):
    id: str
    name: str
    type: str
    available_resources: int

class CreateServiceRequest(BaseModel):
    provider_id: str
    cpu: int
    ram: int
    location: str
    storage: int
    maximumULthroughput: int
    maximumDLthroughput: int
    minPrice: float
    maxPrice: float
