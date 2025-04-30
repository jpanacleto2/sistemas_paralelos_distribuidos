import grpc
from concurrent import futures
import time
import threading
from datetime import datetime

# Importa os arquivos gerados
import chat_pb2
import chat_pb2_grpc

class MessageServiceServicer(chat_pb2_grpc.MessageServiceServicer):
    def __init__(self):
        self.messages = [] # Lista para armazenar as mensagens
        self._lock = threading.Lock() # Para garantir acesso seguro à lista de mensagens
        self._subscribers = [] # Lista de contextos de clientes que chamaram ListMessages

    def SendMessage(self, request, context):
        # Basicamente, apenas adicionamos a mensagem com um timestamp
        message_with_timestamp = chat_pb2.Message(
            sender=request.sender,
            content=request.content,
            timestamp=int(datetime.now().timestamp())
        )
        with self._lock:
            self.messages.append(message_with_timestamp)
            # Poderíamos ordenar aqui, mas adicionar ao final e retornar na ordem de adição
            # para ListMessages já serve para o básico. Para ordenação rigorosa por tempo,
            # precisaríamos de uma estrutura de dados diferente ou ordenar na leitura.
            print(f"Mensagem recebida de {request.sender}: {request.content}")

            # Notificar assinantes (clientes que chamaram ListMessages)
            for subscriber_context in self._subscribers:
                try:
                    subscriber_context.write(message_with_timestamp)
                except grpc.RpcError as e:
                    # Lidar com clientes desconectados
                    print(f"Cliente desconectado: {e}")
                    self._subscribers.remove(subscriber_context)


        return chat_pb2.SendMessageResponse(success=True, message="Mensagem enviada com sucesso!")

    def ListMessages(self, request, context):
        # Este método envia mensagens existentes e depois continua enviando novas mensagens
        with self._lock:
            # Envia mensagens existentes primeiro
            for msg in self.messages:
                yield msg

            # Adiciona o contexto do cliente à lista de assinantes para receber futuras mensagens
            self._subscribers.append(context)

            # Mantém a conexão aberta para enviar novas mensagens via streaming
            # O loop abaixo garante que o servidor continue respondendo ao cliente
            # até que a conexão seja cancelada pelo cliente ou ocorra um erro.
            try:
                while context.is_active():
                    time.sleep(1) # Pequena pausa para não consumir 100% da CPU
            except grpc.RpcError:
                print("Cliente de streaming desconectado.")
            finally:
                # Remove o cliente da lista de assinantes quando a conexão é encerrada
                if context in self._subscribers:
                    self._subscribers.remove(context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_MessageServiceServicer_to_server(MessageServiceServicer(), server)
    server.add_insecure_port('[::]:50052') # Porta para o servidor de mensagens
    server.start()
    print("Servidor de mensagens iniciado na porta 50052.")
    try:
        while True:
            time.sleep(86400) # Mantém o servidor rodando
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()