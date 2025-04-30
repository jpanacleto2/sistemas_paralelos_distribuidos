import grpc
from concurrent import futures
import time

# Importa os arquivos gerados
import chat_pb2
import chat_pb2_grpc

class UserServiceServicer(chat_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = set() # Usaremos um set para armazenar nomes únicos de usuários

    def RegisterUser(self, request, context):
        username = request.username
        if username in self.users:
            return chat_pb2.RegisterUserResponse(success=False, message="Nome de usuário já existe.")
        else:
            self.users.add(username)
            print(f"Usuário registrado: {username}")
            return chat_pb2.RegisterUserResponse(success=True, message="Usuário registrado com sucesso!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051') # Porta para o servidor de usuários
    server.start()
    print("Servidor de usuários iniciado na porta 50051.")
    try:
        while True:
            time.sleep(86400) # Mantém o servidor rodando
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()