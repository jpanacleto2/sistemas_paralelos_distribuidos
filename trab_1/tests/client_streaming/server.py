import grpc
from concurrent import futures

import client_streaming_pb2
import client_streaming_pb2_grpc

class StreamServiceServicer(client_streaming_pb2_grpc.StreamServiceServicer):
    def SumStream(self, request_iterator, context):
        total = 0
        for number in request_iterator:
            print(f"Recebido: {number.value}")
            total += number.value
        return client_streaming_pb2.SumResponse(total=total)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_streaming_pb2_grpc.add_StreamServiceServicer_to_server(StreamServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Servidor de client streaming na porta 50053...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
