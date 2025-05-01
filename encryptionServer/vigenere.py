def vigenere_encrypt(plain_text: str, key: str) -> str:
    # Filtra apenas caracteres alfabéticos da chave
    clean_key = [k.lower() for k in key if k.isalpha()]
    if not clean_key:
        return plain_text  # Retorna original se chave não tem letras
    
    encrypted_text = []
    key_len = len(clean_key)
    key_idx = 0
    
    for char in plain_text:
        if char.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - ord('a')
            if char.isupper():
                encrypted_text.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                encrypted_text.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_idx += 1
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)