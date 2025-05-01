from fastapi import FastAPI, HTTPException
import grpc
import crypto_pb2
import crypto_pb2_grpc
import os

app = FastAPI()

# Endereços dos servidores gRPC (ajuste conforme necessário)
GRPC_SERVER_A_ADDRESS = os.environ.get("GRPC_SERVER_A_ADDRESS", "localhost:50051")
GRPC_SERVER_B_ADDRESS = os.environ.get("GRPC_SERVER_B_ADDRESS", "localhost:50052")

@app.post("/encrypt/")
async def encrypt_message(message: str, key: str):
    try:
        # Conecta ao gRPC Server A (Encriptação)
        with grpc.insecure_channel(GRPC_SERVER_A_ADDRESS) as channel:
            stub = crypto_pb2_grpc.CryptoServiceStub(channel)
            request = crypto_pb2.EncryptRequest(plaintext=message, key=key)
            response = stub.Encrypt(request)
            return {"ciphertext": response.ciphertext}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error during encryption: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during encryption: {e}")

@app.post("/decrypt/")
async def decrypt_message(message: str, key: str):
    try:
        # Conecta ao gRPC Server B (Decriptação)
        with grpc.insecure_channel(GRPC_SERVER_B_ADDRESS) as channel:
            stub = crypto_pb2_grpc.CryptoServiceStub(channel)
            request = crypto_pb2.DecryptRequest(ciphertext=message, key=key)
            response = stub.Decrypt(request)
            return {"plaintext": response.plaintext}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error during decryption: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during decryption: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # Porta para o FastAPI