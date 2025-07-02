import grpc
from concurrent import futures
import threading
import time
import json
import dlt_gateway_pb2
import dlt_gateway_pb2_grpc

class MockDltGatewayService(dlt_gateway_pb2_grpc.DltGatewayServiceServicer):
    
    def GetNonce(self, request, context):
        """Mock GetNonce - returns a nonce for the given DID"""
        request_data = json.loads(request.value)
        did = request_data.get("data", {}).get("did", "unknown")
        
        # Generate a mock nonce
        mock_nonce = f"nonce_{hash(did) % 1000000:06d}"
        
        response_data = mock_nonce
        
        return dlt_gateway_pb2.Response(value=json.dumps(response_data))

    def CreatePresentation(self, request, context):
        """Mock CreatePresentation - returns a verifiable presentation containing the credential"""
        try:
            credential = json.loads(request.credential)
            
            mock_presentation = {
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiablePresentation"],
                "verifiableCredential": [credential],  # Include the parsed credential
                "proof": {
                    "type": "Ed25519Signature2018",
                    "created": "2023-01-01T00:00:00Z",
                    "nonce": request.nonce,  # Include the nonce from request
                    "proofValue": f"mock_proof_{hash(str(credential)) % 1000000:06d}"
                }
            }
            
            # Return presentation as JSON string in value field, with empty error
            return dlt_gateway_pb2.Response(
                value=json.dumps(mock_presentation),
                error=""
            )
        except Exception as e:
            # Return error if something goes wrong
            return dlt_gateway_pb2.Response(
                value="",
                error=f"Failed to create presentation: {str(e)}"
            )

    def VerifyCredential(self, request, context):
        """Mock VerifyCredential - returns verification result"""
        try:
            request_data = json.loads(request.value)
            credential = request_data.get("credential", {})

            if not credential:
                return dlt_gateway_pb2.VerificationResult(
                    result=False,
                    error="No credential provided"
                )
            
            if credential.get("type") == ["RevokedCredential"]:
                return dlt_gateway_pb2.VerificationResult(
                    result=False,
                    error="Credential has been revoked"
                )
            
            return dlt_gateway_pb2.VerificationResult(
                result=True,
                error=""
            )
            
        except Exception as e:
            return dlt_gateway_pb2.VerificationResult(
                result=False,
                error=f"Verification failed: {str(e)}"
            )

    def CreateSearch(self, request, context):
        """Mock CreateSearch - returns mock search results with services list and status"""
        try:
            request_data = json.loads(request.value)
            
            # Mock search response with list of services and status
            mock_search_response = {
                "searchId": f"search_{hash(str(request_data)) % 1000000:06d}",
                "status": "completed",
                "query": request_data,
                "services": [
                    {
                        "serviceId": "service_001",
                        "name": "Data Analytics Service",
                        "providerId": "provider_123",
                        "description": "Advanced data analytics and machine learning",
                        "category": "analytics",
                        "score": 0.95,
                        "pricing": {
                            "model": "per_hour",
                            "amount": 50.0,
                            "currency": "USD"
                        }
                    },
                    {
                        "serviceId": "service_002", 
                        "name": "Cloud Storage Service",
                        "providerId": "provider_456",
                        "description": "Secure cloud storage with encryption",
                        "category": "storage",
                        "score": 0.88,
                        "pricing": {
                            "model": "per_gb",
                            "amount": 0.023,
                            "currency": "USD"
                        }
                    },
                    {
                        "serviceId": "service_003",
                        "name": "API Gateway Service", 
                        "providerId": "provider_789",
                        "description": "High-performance API gateway with monitoring",
                        "category": "infrastructure",
                        "score": 0.92,
                        "pricing": {
                            "model": "per_request",
                            "amount": 0.001,
                            "currency": "USD"
                        }
                    }
                ],
                "totalResults": 3,
                "timestamp": int(time.time())
            }
            
            return dlt_gateway_pb2.Response(
                value=json.dumps(mock_search_response),
                error=""
            )
            
        except Exception as e:
            return dlt_gateway_pb2.Response(
                value="",
                error=f"Search creation failed: {str(e)}"
            )

    def SlaSign(self, request, context):
        """Mock SlaSign - handles SLA signing requests"""
        try:
            request_data = json.loads(request.value)
            
            # Validate required fields
            if not request_data.get("slaId"):
                return dlt_gateway_pb2.Response(
                    value="",
                    error="Missing required field: slaId"
                )
            if not request_data.get("uid"):
                return dlt_gateway_pb2.Response(
                    value="",
                    error="Missing required field: uid"
                )
            
            # Mock successful signing
            return dlt_gateway_pb2.Response(
                value="",
                error=""
            )
            
        except json.JSONDecodeError:
            return dlt_gateway_pb2.Response(
                value="",
                error="Invalid JSON in request"
            )
        except Exception as e:
            return dlt_gateway_pb2.Response(
                value="",
                error=f"SLA signing failed: {str(e)}"
            )
    
    def SubscribeToSLAInit(self, request, context):
        """Mock SubscribeToSLAInit - streams SLA initialization events"""
        # Mock events for SLA initialization
        events = [
            {
                "name": "SLA_INIT",
                "payload": json.dumps({
                    "id": "sla-init-001",
                    "value": "sla value in json format",
                    "provider_id": "provider-123",
                    "consumer_id": "consumer-456",
                    "provider_sig": "mock_provider_sig_xyz",
                    "consumer_sig": "mock_consumer_sig_xyz"
                })
            }
        ]
        
        for event in events:
            yield dlt_gateway_pb2.DltRecordEvent(
                name=event["name"],
                payload=event["payload"]
            )

    def SubscribeToSLASigning(self, request, context):
        """Mock SubscribeToSLASigning - streams SLA signing events"""
        # Mock events for SLA signing
        events = [
            {
                "name": "SLA_SIGNING",
                "payload": json.dumps({
                    "id": "sla-sign-001",
                    "value": "sla value in json format",
                    "provider_id": "provider-123",
                    "consumer_id": "consumer-456",
                    "provider_sig": "mock_provider_sig_xyz",
                    "consumer_sig": "mock_consumer_sig_xyz"
                })
            }
        ]
        
        for event in events:
            yield dlt_gateway_pb2.DltRecordEvent(
                name=event["name"],
                payload=event["payload"]
            )

class MockGrpcServer:
    def __init__(self, port=50051):
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the mock gRPC server"""
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        dlt_gateway_pb2_grpc.add_DltGatewayServiceServicer_to_server(
            MockDltGatewayService(), self.server
        )
        
        listen_addr = f'[::]:{self.port}'
        self.server.add_insecure_port(listen_addr)
        
        def run_server():
            self.server.start()
            print(f"Mock gRPC server started on port {self.port}")
            try:
                self.server.wait_for_termination()
            except KeyboardInterrupt:
                print("Mock gRPC server stopped")
        
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        time.sleep(1)  # Give server time to start
    
    def stop(self):
        """Stop the mock gRPC server"""
        if self.server:
            self.server.stop(0)

if __name__ == "__main__":
    # Start the mock server
    mock_server = MockGrpcServer()
    mock_server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mock_server.stop()
        print("Mock server stopped") 