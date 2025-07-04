import os
import grpc
import dlt_gateway_pb2
import dlt_gateway_pb2_grpc
from typing import Generator, Dict, Any
import json

class DltGatewayClient:
    def __init__(self, host: str = None, port: int = None):
        host = os.getenv("GRPC_HOST")
        host = host if host else "localhost"
        port = os.getenv("GRPC_PORT")
        port = int(port) if port else 50051
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = dlt_gateway_pb2_grpc.DltGatewayServiceStub(self.channel)

    def create_search(self, search_request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a search request."""
        request = dlt_gateway_pb2.Request(value=json.dumps(search_request))
        response = self.stub.CreateSearch(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def sla_sign(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sign an SLA."""
        request = dlt_gateway_pb2.Request(value=json.dumps(request_data))
        response = self.stub.SlaSign(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def subscribe_to_sla_init(self) -> Generator[Dict[str, Any], None, None]:
        """Subscribe to SLA initialization events."""
        request = dlt_gateway_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        for event in self.stub.SubscribeToSLAInit(request):
            yield {
                "name": event.name,
                "payload": event.payload
            }

    def subscribe_to_sla_signing(self) -> Generator[Dict[str, Any], None, None]:
        """Subscribe to SLA signing events."""
        request = dlt_gateway_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        for event in self.stub.SubscribeToSLASigning(request):
            yield {
                "name": event.name,
                "payload": event.payload
            }

    def list_dids(self) -> Dict[str, Any]:
        """List all DIDs saved in the wallet."""
        request = dlt_gateway_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self.stub.ListDIDs(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def request_credential(self, issuer_address: str, cred_param: Dict[str, Any]) -> Dict[str, Any]:
        """Request a credential from an issuer."""
        request = dlt_gateway_pb2.CredentialRequest(
            issuerAddress=issuer_address,
            credParam=dlt_gateway_pb2.CredentialParam(
                holderDID=cred_param.get("holderDID", ""),
                claims=cred_param.get("claims", ""),
                vmId=cred_param.get("vmId", ""),
                signature=cred_param.get("signature", "")
            )
        )
        response = self.stub.RequestCredential(request)
        return {
            "credential": response.credential,
            "error": response.error
        }

    def lookup_did(self, did_value: str) -> Dict[str, Any]:
        """Look up a DID document in the registry."""
        request = dlt_gateway_pb2.Request(value=did_value)
        response = self.stub.LookupDID(request)
        return {
            "value": response.value,
            "error": response.error
        } 
    
    def show_credential(self, credential_value: str) -> Dict[str, Any]: 
        """Get a verifiable credential from the wallet."""
        request = dlt_gateway_pb2.Request(value=credential_value)
        response = self.stub.ShowCredential(request)
        return {
            "value": response.value,
            "error": response.error
        }
    
    def list_credentials(self) -> Dict[str, Any]:
        """Get a credential from the wallet."""
        request = dlt_gateway_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self.stub.ListCredentials(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def request_authorization(self, verifier_address: str, auth_param: Dict[str, Any]) -> Dict[str, Any]:
        """Request authorization from a verifier."""
        request = dlt_gateway_pb2.AuthorizationRequest(
            verifierAddress=verifier_address,
            authParam=dlt_gateway_pb2.AuthorizationParam(
                holderDID=auth_param.get("holderDID", ""),
                vcId=auth_param.get("vcId", "")
            )
        )
        response = self.stub.RequestAuthorization(request)
        return {
            "result": response.result,
            "error": response.error
        }
    
    def sign_message(self, did: str, payload: str, vmId: str) -> Dict[str, Any]:
        """Sign a message."""
        request = dlt_gateway_pb2.SignMessageReq(
            did=did,
            payload=payload,
            vmId=vmId
        )
        response = self.stub.SignMessage(request)
        return {
            "signature": response.signature,
            "vmId": response.vmId,
            "error": response.error
        }
    
    def verify_message(self, did: str, payload: str, signature: str, vmId: str) -> Dict[str, Any]:
        """Verify a message."""
        request = dlt_gateway_pb2.VerifyMessageReq(
            did=did,
            payload=payload,
            signature=signature,
            vmId=vmId
        )
        response = self.stub.VerifyMessage(request)
        return {
            "result": response.result,
            "error": response.error
        }