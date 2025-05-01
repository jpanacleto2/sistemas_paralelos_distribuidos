import grpc
from concurrent import futures
import time

import crypto_pb2
import crypto_pb2_grpc

class CryptoServicer(crypto_pb2_grpc.CryptoServiceServicer):
    def Decrypt(self, request, context):
        print(f"Received decryption request for: {request.ciphertext}")
        # Lógica de decriptação real aqui
        # Exemplo simplificado: remover "ENCRYPTED(...)"
        import re
        match = re.match(r"ENCRYPTED\((.*),(.*)\)", request.ciphertext)
        if match:
            plaintext = match.group(1)
            key = match.group(2)
            print(f"Decrypted using key: {key}")
            return crypto_pb2.DecryptResponse(plaintext=plaintext)
        else:
            context.set_details("Invalid ciphertext format")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return crypto_pb2.DecryptResponse(plaintext="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crypto_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoServicer(), server)
    server.add_insecure_port('[::]:50052') # Porta para o Server B
    server.start()
    print("Server B started on port 50052")
    try:
        while True:
            time.sleep(86400) # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()