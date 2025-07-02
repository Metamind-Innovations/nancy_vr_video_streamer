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

    def get_nonce(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get a nonce from the verifier wallet."""
        request = dlt_gateway_pb2.Request(value=json.dumps(request_data))
        response = self.stub.GetNonce(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def create_presentation(self, credential: Dict[str, Any], nonce: str) -> Dict[str, Any]:
        """Create a verifiable presentation."""
        request = dlt_gateway_pb2.PresentationParam(
            credential=json.dumps(credential),
            nonce=nonce
        )
        response = self.stub.CreatePresentation(request)
        return {
            "value": response.value,
            "error": response.error
        }

    def verify_credential(self, credential: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a credential."""
        request = dlt_gateway_pb2.Request(value=json.dumps(credential))
        response = self.stub.VerifyCredential(request)
        return {
            "result": response.result,
            "error": response.error
        }

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