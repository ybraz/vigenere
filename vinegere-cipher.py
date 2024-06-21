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

import sys  # Importa o módulo sys para acessar os argumentos da linha de comando

# Função para criptografar uma mensagem usando a cifra de Vigenère
def encrypt_vigenere(plaintext, keyword):
    plaintext = plaintext.upper()  # Converte o texto para maiúsculas
    keyword = keyword.upper().replace(" ", "")  # Converte a palavra-chave para maiúsculas e remove espaços
    # Repete a palavra-chave para cobrir o comprimento do texto
    keyword_repeated = (keyword * ((len(plaintext.replace(" ", "")) // len(keyword)) + 1))[:len(plaintext.replace(" ", ""))]
    
    ciphertext = ""  # Inicializa o texto cifrado
    keyword_index = 0  # Índice da palavra-chave
    for p in plaintext:  # Itera sobre cada letra do texto
        if p == " ":
            ciphertext += " "  # Mantém os espaços no texto cifrado
        else:
            p_val = ord(p) - ord('A')  # Converte a letra do texto para um valor numérico
            k_val = ord(keyword_repeated[keyword_index]) - ord('A')  # Converte a letra da palavra-chave para um valor numérico
            c_val = (p_val + k_val) % 26  # Calcula o valor da letra cifrada
            ciphertext += chr(c_val + ord('A'))  # Converte o valor numérico de volta para uma letra
            keyword_index += 1
    
    return ciphertext  # Retorna o texto cifrado

# Função para descriptografar uma mensagem usando a cifra de Vigenère
def decrypt_vigenere(ciphertext, keyword):
    ciphertext = ciphertext.upper()  # Converte o texto cifrado para maiúsculas
    keyword = keyword.upper().replace(" ", "")  # Converte a palavra-chave para maiúsculas e remove espaços
    # Repete a palavra-chave para cobrir o comprimento do texto cifrado
    keyword_repeated = (keyword * ((len(ciphertext.replace(" ", "")) // len(keyword)) + 1))[:len(ciphertext)]
    
    plaintext = ""  # Inicializa o texto decifrado
    keyword_index = 0  # Índice da palavra-chave
    for c in ciphertext:  # Itera sobre cada letra do texto cifrado
        if c == " ":
            plaintext += " "  # Mantém os espaços no texto decifrado
        else:
            c_val = ord(c) - ord('A')  # Converte a letra cifrada para um valor numérico
            k_val = ord(keyword_repeated[keyword_index]) - ord('A')  # Converte a letra da palavra-chave para um valor numérico
            p_val = (c_val - k_val + 26) % 26  # Calcula o valor da letra decifrada
            plaintext += chr(p_val + ord('A'))  # Converte o valor numérico de volta para uma letra
            keyword_index += 1
    
    return plaintext  # Retorna o texto decifrado

# Função principal que é chamada quando o script é executado
def main():
    if len(sys.argv) != 4:  # Verifica se o número correto de argumentos foi fornecido
        print("Uso: python script.py <modo> <texto> <chave>")
        print("Modo: 1 para criptografar, 2 para descriptografar")
        return
    
    mode = int(sys.argv[1])  # Modo de operação (1 para criptografar, 2 para descriptografar)
    text = sys.argv[2]  # Texto a ser cifrado ou decifrado
    keyword = sys.argv[3]  # Palavra-chave
    
    if mode == 1:
        result = encrypt_vigenere(text, keyword)  # Chama a função de criptografia
        print(f"Texto cifrado: {result}")
    elif mode == 2:
        result = decrypt_vigenere(text, keyword)  # Chama a função de descriptografia
        print(f"Texto decifrado: {result}")
    else:
        print("Modo inválido. Use 1 para criptografar e 2 para descriptografar.")
        print("Uso: python script.py <modo> <texto> <chave>")

if __name__ == "__main__":
    main()  # Chama a função principal se o script for executado diretamente
