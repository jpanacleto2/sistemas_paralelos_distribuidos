import requests
import time

URLS = {
    "grpc_encrypt": "http://192.168.100.101:8080/encrypt/",
    "grpc_decrypt": "http://192.168.100.101:8080/decrypt/",
    "rest_encrypt": "http://192.168.100.101:8080/encrypt_rest/",
    "rest_decrypt": "http://192.168.100.101:8080/decrypt_rest/",
}

KEY = "segredo"

PAYLOADS = [
    "Curto.",
    "Texto medio para cifragem com chave secreta.",
    "Texto um pouco maior para avaliar como o desempenho varia com o tamanho da entrada. " * 2,
    "Texto muito grande " * 50,
    "Texto pequeno, apenas para testar o comportamento em tamanhos menores.",
    "A criptografia de Vigenere é um dos métodos mais antigos de cifragem, foi inventada por Blaise de Vigenere.",
    "Este texto é uma tentativa de aumentar ainda mais o tamanho do payload para testar a performance do sistema com entradas grandes, muitas palavras e caracteres repetidos.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "1234567890!@#$%^&*()_+=-`~;:'\",.<>?/|\\{}[]",
    "Teste de carga com um texto ainda maior que está sendo gerado automaticamente para medir como o sistema lida com grandes volumes de dados, esse texto vai ter muito mais conteúdo e por isso irá testar a capacidade de desempenho do sistema em um cenário de alta demanda.",
    "Acelerando o teste com um texto extremamente longo para verificar como o sistema lida com entradas em massa. Vamos aumentar ainda mais a quantidade de caracteres para que possamos observar a diferença no tempo de processamento entre gRPC e REST.",
    "Essa frase tem um número misto de letras, números e caracteres especiais, é um bom exemplo de payload variado que pode ser interessante para testar o comportamento do sistema quando há uma combinação de diferentes tipos de caracteres. Ela também tem um tamanho considerável para ser eficiente na avaliação de performance."
]

def benchmark_encrypt_and_decrypt(text: str, key: str):
    results = {}

    for mode in ["grpc", "rest"]:
        # Encrypt
        encrypt_url = URLS[f"{mode}_encrypt"]
        start_encrypt = time.time()
        enc_response = requests.post(encrypt_url, json={"text": text, "key": key})
        end_encrypt = time.time()

        encrypted_text = enc_response.json()["result"]

        # Decrypt
        decrypt_url = URLS[f"{mode}_decrypt"]
        start_decrypt = time.time()
        dec_response = requests.post(decrypt_url, json={"text": encrypted_text, "key": key})
        end_decrypt = time.time()

        decrypted_text = dec_response.json()["result"]

        results[mode] = {
            "encrypt_time": end_encrypt - start_encrypt,
            "decrypt_time": end_decrypt - start_decrypt,
            "decryption_match": decrypted_text == text
        }

    return results

# Executa os testes
print(f"{'Payload Size':<15} {'Encrypt (gRPC)':<15} {'Encrypt (REST)':<15} {'Decrypt (gRPC)':<15} {'Decrypt (REST)':<15}")
print("-" * 85)

for payload in PAYLOADS:
    res = benchmark_encrypt_and_decrypt(payload, KEY)

    print(f"{len(payload):<15} "
        f"{res['grpc']['encrypt_time']:<17.6f}"
        f"{res['rest']['encrypt_time']:<17.6f}"
        f"{res['grpc']['decrypt_time']:<17.6f}"
        f"{res['rest']['decrypt_time']:<17.6f}")