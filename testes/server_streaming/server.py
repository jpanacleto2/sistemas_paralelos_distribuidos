import grpc
from concurrent import futures
import time

import streaming_pb2
import streaming_pb2_grpc

class StreamServiceServicer(streaming_pb2_grpc.StreamServiceServicer):
    def CountTo(self, request, context):
        for i in range(1, request.max + 1):
            yield streaming_pb2.CountResponse(number=i)
            time.sleep(0.5)  # Simula delay para visualização

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamServiceServicer_to_server(StreamServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor de streaming rodando na porta 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
