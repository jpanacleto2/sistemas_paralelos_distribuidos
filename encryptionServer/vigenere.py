def vigenere_encrypt(plain_text: str, key: str) -> str:
    encrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(plain_text):
        if char.isalpha():
            # Calcula o deslocamento baseado na letra da chave
            shift = ord(key[i % key_length].lower()) - ord('a')
            
            if char.isupper():
                # Processa letras maiúsculas
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Processa letras minúsculas
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_text.append(encrypted_char)
        else:
            # Mantém caracteres não alfabéticos
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)