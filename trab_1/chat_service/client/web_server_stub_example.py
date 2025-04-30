import grpc
import time
import threading

# Importa os arquivos gerados
import chat_pb2
import chat_pb2_grpc

def run():
    # Conecta ao servidor de usuários
    user_channel = grpc.insecure_channel('localhost:50051')
    user_stub = chat_pb2_grpc.UserServiceStub(user_channel)

    # Conecta ao servidor de mensagens
    message_channel = grpc.insecure_channel('localhost:50052')
    message_stub = chat_pb2_grpc.MessageServiceStub(message_channel)

    # Exemplo: Registrar um usuário
    print("Digite seu nome de usuario:\n")
    nome = input()
    register_response = user_stub.RegisterUser(chat_pb2.RegisterUserRequest(username=nome))
    print(f"Resposta de registro: {register_response.message}")

    # Exemplo: Enviar mensagens
    print("Digite sua mensagem: ")
    mensagem = input()
    send_response = message_stub.SendMessage(chat_pb2.Message(sender=nome , content=mensagem))
    print(f"Resposta de envio: {send_response.message}")


    # Exemplo: Receber mensagens via streaming
    print("\nRecebendo mensagens (streaming)...")
    try:
        # Iniciamos um thread para ouvir as mensagens para não bloquear o programa principal
        def message_listener():
            try:
                for message in message_stub.ListMessages(chat_pb2.ListMessagesRequest()):
                    print(f"Nova mensagem de {message.sender} (timestamp: {message.timestamp}): {message.content}")
            except grpc.RpcError as e:
                print(f"Erro no streaming de mensagens: {e}")

        listener_thread = threading.Thread(target=message_listener)
        listener_thread.start()

        # Mantenha o cliente rodando por um tempo para receber mensagens
        time.sleep(20) # Aguarda 20 segundos para receber mensagens

    except KeyboardInterrupt:
        print("Cliente encerrado.")

    finally:
        # Fecha os canais gRPC
        user_channel.close()
        message_channel.close()

if __name__ == '__main__':
    run()