import grpc
import client_streaming_pb2
import client_streaming_pb2_grpc
import time 

def generate_numbers():
    for i in [40, 20, 30]:
        yield client_streaming_pb2.Number(value=i)
        time.sleep(1)

def run():
    channel = grpc.insecure_channel('localhost:50053')
    stub = client_streaming_pb2_grpc.StreamServiceStub(channel)

    response = stub.SumStream(generate_numbers())
    print(f"Soma total recebida: {response.total}")

if __name__ == '__main__':
    run()
