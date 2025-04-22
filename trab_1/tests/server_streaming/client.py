import grpc
import streaming_pb2
import streaming_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = streaming_pb2_grpc.StreamServiceStub(channel)

    number = int(input('Escolha um numero, no qual o servidor ira imprimir ate ele: '))

    request = streaming_pb2.CountRequest(max=number)

    print("Recebendo stream do servidor:")
    for response in stub.CountTo(request):
        print(f"Número recebido: {response.number}")

if __name__ == '__main__':
    run()
