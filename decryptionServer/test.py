import grpc
import crypto_pb2
import crypto_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = crypto_pb2_grpc.CryptoServiceStub(channel)
    
    # Teste apenas de encriptação
    response = stub.Decrypt(crypto_pb2.CryptoRequest(
        text="tevrxt tevrxt",
        key="SECRET"
    ))
    print("Decrypted:", response.result)

if __name__ == '__main__':
    run()