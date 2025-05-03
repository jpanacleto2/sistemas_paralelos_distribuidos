import grpc
import time
from concurrent import futures

import bidi_streaming_pb2
import bidi_streaming_pb2_grpc

class ChatSericeServicer(bidi_streaming_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        for message in request_iterator:
            print(f"[{message.user}] -> {message.text}")
            response_text = f"Olá {message.user}, você disse: '{message.text}'"
            yield bidi_streaming_pb2.ChatMessage(user="Servidor", text=response_text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidi_streaming_pb2_grpc.add_ChatServiceServicer_to_server(ChatSericeServicer(),server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Servidor de chat rodando na porta 50054...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
