import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = calculator_pb2_grpc.CalculatorStub(channel)

    num1 = input('Entre com o 1º valor: ')

    num2 = input('Entre com o 2º valor: ')

    request = calculator_pb2.SumRequest(a=int(num1), b=int(num2))
    response = stub.Sum(request)

    print(f"Resultado da soma: {response.result}")

if __name__ == '__main__':
    run()
