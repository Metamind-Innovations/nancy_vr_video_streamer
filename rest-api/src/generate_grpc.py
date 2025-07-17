import subprocess

def generate_grpc_code():
    # Generate gRPC code
    subprocess.run([
        "python", "-m", "grpc_tools.protoc",
        "-I.",
        "--python_out=.",
        "--grpc_python_out=.",
        "dlt_gateway.proto"
    ])
