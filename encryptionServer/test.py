import grpc
import crypto_pb2
import crypto_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = crypto_pb2_grpc.CryptoServiceStub(channel)
    
    # Teste apenas de encriptação
    response = stub.Encrypt(crypto_pb2.CryptoRequest(
        text="batata batata",
        key="SECRET"
    ))
    print("Encrypted:", response.result)

if __name__ == '__main__':
    run()