##
## Cifra de Vigenère
##

## Por: Yuri Braz (ybraz@proton.me)
## Versão: 0.1
## Data: 21/06/2024

'''
A cifra de Vigenère é um método de criptografia que usa uma palavra-chave para cifrar e decifrar mensagens. 
Em vez de substituir cada letra da mensagem por uma letra fixa (como na cifra de César), 
a cifra de Vigenère usa uma série de diferentes substituições baseadas em uma palavra-chave.

Criptografia:
- Suponha que a soma das posições das letras "V" (22ª letra) e "M" (13ª letra) ultrapasse 26.
- Some as posições: 22 + 13 = 35.
- Use o módulo 26 para ajustar: 35 % 26 = 9.
- A 9ª letra do alfabeto é "I".

Descriptografia:
- Suponha que subtrair as posições das letras "I" (9ª letra) e "M" (13ª letra) resulte em um valor negativo.
- Subtraia as posições: 9 - 13 = -4.
- Para obter um valor positivo dentro do intervalo do alfabeto, podemos adicionar 26 e então aplicar o módulo 26: (-4 + 26) % 26 = 22.
- A 22ª letra do alfabeto é "V".
'''

import sys

def encrypt_vigenere(plaintext, keyword):
    plaintext = plaintext.upper()
    keyword = keyword.upper().replace(" ", "")
    keyword_repeated = (keyword * ((len(plaintext.replace(" ", "")) // len(keyword)) + 1))[:len(plaintext.replace(" ", ""))]
    
    ciphertext = ""
    keyword_index = 0
    for p in plaintext:
        if p == " ":
            ciphertext += " "
        else:
            p_val = ord(p) - ord('A')
            k_val = ord(keyword_repeated[keyword_index]) - ord('A')
            c_val = (p_val + k_val) % 26
            ciphertext += chr(c_val + ord('A'))
            keyword_index += 1
    
    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    ciphertext = ciphertext.upper()
    keyword = keyword.upper().replace(" ", "")
    keyword_repeated = (keyword * ((len(ciphertext.replace(" ", "")) // len(keyword)) + 1))[:len(ciphertext.replace(" ", ""))]
    
    plaintext = ""
    keyword_index = 0
    for c in ciphertext:
        if c == " ":
            plaintext += " "
        else:
            c_val = ord(c) - ord('A')
            k_val = ord(keyword_repeated[keyword_index]) - ord('A')
            p_val = (c_val - k_val + 26) % 26
            plaintext += chr(p_val + ord('A'))
            keyword_index += 1
    
    return plaintext

def main():
    if len(sys.argv) != 4:
        print("Uso: python script.py <modo> <texto> <chave>")
        print("Modo: 1 para criptografar, 2 para descriptografar")
        return
    
    mode = int(sys.argv[1])
    text = sys.argv[2]
    keyword = sys.argv[3]
    
    if mode == 1:
        result = encrypt_vigenere(text, keyword)
        print(f"Texto cifrado: {result}")
    elif mode == 2:
        result = decrypt_vigenere(text, keyword)
        print(f"Texto decifrado: {result}")
    else:
        print("Modo inválido. Use 1 para criptografar e 2 para descriptografar.")
        print("Uso: python script.py <modo> <texto> <chave>")

if __name__ == "__main__":
    main()
