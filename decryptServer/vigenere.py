def vigenere_decrypt(cipher_text: str, key: str) -> str:
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(cipher_text):
        if char.isalpha():
            # Calcula o deslocamento (inverso para decriptação)
            shift = ord(key[i % key_length].lower()) - ord('a')
            
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)