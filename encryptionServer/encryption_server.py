import grpc
from concurrent import futures

import crypto_pb2
import crypto_pb2_grpc

from vigenere import vigenere_encrypt

class CryptoServicer(crypto_pb2_grpc.CryptoServiceServicer):
    def Encrypt(self, request, context):
        try:
            result = vigenere_encrypt(request.text, request.key)
            return crypto_pb2.CryptoResponse(result=result)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro na codificação: {str(e)}")
            return crypto_pb2.CryptoResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crypto_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoServicer(), server)
    server.add_insecure_port('[::]:50051') 
    server.start()
    print("Servidor de codificação rodando na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()