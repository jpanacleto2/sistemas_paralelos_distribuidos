import grpc
from concurrent import futures
import time

import crypto_pb2
import crypto_pb2_grpc

class CryptoServicer(crypto_pb2_grpc.CryptoServiceServicer):
    def Encrypt(self, request, context):
        print(f"Received encryption request for: {request.plaintext}")
        # Lógica de encriptação real aqui
        encrypted_text = f"ENCRYPTED({request.plaintext},{request.key})"
        return crypto_pb2.EncryptResponse(ciphertext=encrypted_text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crypto_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoServicer(), server)
    server.add_insecure_port('[::]:50051') # Porta para o Server A
    server.start()
    print("Server A started on port 50051")
    try:
        while True:
            time.sleep(86400) # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()