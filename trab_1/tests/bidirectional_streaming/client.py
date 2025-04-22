import grpc
import bidi_streaming_pb2
import bidi_streaming_pb2_grpc
import time

def message_generator():
    mensagens = ["Oi", "Como você está?", "Esse é um teste!", "Tchau"]
    for msg in mensagens:
        yield bidi_streaming_pb2.ChatMessage(user="Aluno", text=msg)
        time.sleep(3)  # Simula atraso entre mensagens

def run():
    channel = grpc.insecure_channel('localhost:50054')
    stub = bidi_streaming_pb2_grpc.ChatServiceStub(channel)

    responses = stub.Chat(message_generator())

    for response in responses:
        print(f"[{response.user}] -> {response.text}")

if __name__ == '__main__':
    run()
