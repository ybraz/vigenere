##
## Método Kasiski para quebrar a cifra Vinegere
##

'''
Quebrar a cifra de Vigenère é um problema clássico em criptografia e pode ser realizado utilizando técnicas como análise de frequência e o método de Kasiski. 
O método de Kasiski ajuda a encontrar o comprimento da palavra-chave, e a análise de frequência é usada para determinar as letras da palavra-chave. 

Passos para Quebrar a Cifra de Vigenère

1. Encontrar o Comprimento da Palavra-Chave:
- Usar o método de Kasiski para identificar repetições no texto cifrado e estimar o comprimento da palavra-chave.

2. Determinar as Letras da Palavra-Chave:
- Para cada posição na palavra-chave, realizar uma análise de frequência das letras no texto cifrado correspondente a essa posição.
- Assumir que a letra mais frequente corresponde à letra 'E' (a letra mais comum em inglês) e calcular o deslocamento.
'''

from collections import Counter  # Importa Counter para contagem de frequências
import re  # Importa re para manipulação de expressões regulares

# Função para encontrar espaçamentos entre sequências repetidas no texto cifrado
def find_repeated_sequences_spacings(ciphertext):
    spacings = {}  # Dicionário para armazenar os espaçamentos das sequências
    for seq_len in range(3, 6):  # Examina sequências de comprimento 3 a 5
        for i in range(len(ciphertext) - seq_len):
            seq = ciphertext[i:i + seq_len]  # Obtém uma sequência de comprimento seq_len
            for j in range(i + seq_len, len(ciphertext) - seq_len):
                if ciphertext[j:j + seq_len] == seq:  # Verifica se a sequência se repete
                    if seq not in spacings:
                        spacings[seq] = []  # Adiciona a sequência ao dicionário se não estiver presente
                    spacings[seq].append(j - i)  # Adiciona o espaçamento ao dicionário
    return spacings

# Função para realizar o exame de Kasiski
def kasiski_examination(ciphertext):
    spacings = find_repeated_sequences_spacings(ciphertext)  # Obtém os espaçamentos das sequências repetidas
    spacing_freqs = Counter()  # Contador para as frequências dos espaçamentos
    for seq in spacings:
        for space in spacings[seq]:
            spacing_freqs[space] += 1  # Conta as frequências dos espaçamentos
    likely_key_lengths = [spacing for spacing, freq in spacing_freqs.most_common()]  # Comprimentos de chave prováveis
    return likely_key_lengths

# Função para calcular o índice de coincidência de um texto
def calculate_index_of_coincidence(text):
    N = len(text)  # Comprimento do texto
    frequency_sum = sum([freq * (freq - 1) for freq in Counter(text).values()])  # Soma das frequências
    return frequency_sum / (N * (N - 1)) if N > 1 else 0  # Calcula o índice de coincidência

# Função para encontrar o comprimento da chave usando o índice de coincidência
def find_key_length_by_ic(ciphertext):
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())  # Remove caracteres não alfabéticos e converte para maiúsculas
    avg_ic = 0.068  # Índice de coincidência médio esperado para o inglês
    key_length_candidates = []  # Lista de candidatos a comprimento da chave

    for key_length in range(1, 21):  # Assume que o comprimento da chave está entre 1 e 20
        ic_sum = 0
        for i in range(key_length):
            nth_subtext = ciphertext[i::key_length]  # Pega a i-ésima subsequência de comprimento key_length
            ic_sum += calculate_index_of_coincidence(nth_subtext)  # Calcula o índice de coincidência da subsequência
        avg_ic_for_length = ic_sum / key_length  # Média do índice de coincidência para o comprimento da chave
        if abs(avg_ic_for_length - avg_ic) < 0.01:  # Verifica se a média está próxima do esperado
            key_length_candidates.append(key_length)  # Adiciona o comprimento da chave candidato

    return key_length_candidates

# Função para realizar a análise de frequência e determinar a chave
def frequency_analysis(ciphertext, key_length):
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())  # Remove caracteres não alfabéticos e converte para maiúsculas
    key = ''
    for i in range(key_length):
        nth_letters = ciphertext[i::key_length]  # Pega a i-ésima subsequência de comprimento key_length
        freq_counter = Counter(nth_letters)  # Conta as frequências das letras na subsequência
        most_common_letter, _ = freq_counter.most_common(1)[0]  # Encontra a letra mais comum na subsequência
        key += chr(((ord(most_common_letter) - ord('E') + 26) % 26) + ord('A'))  # Calcula a letra correspondente na chave
    return key

# Função para decifrar o texto cifrado usando a cifra de Vigenère
def decrypt_vigenere(ciphertext, keyword):
    ciphertext = ciphertext.upper()  # Converte o texto cifrado para maiúsculas
    keyword = keyword.upper().replace(" ", "")  # Converte a palavra-chave para maiúsculas e remove espaços
    keyword_repeated = (keyword * ((len(ciphertext) // len(keyword)) + 1))[:len(ciphertext)]  # Repete a palavra-chave para cobrir todo o texto

    plaintext = ""
    keyword_index = 0
    for c in ciphertext:
        if c == " ":
            plaintext += " "  # Mantém os espaços no texto decifrado
        else:
            c_val = ord(c) - ord('A')  # Converte a letra cifrada para um valor numérico
            k_val = ord(keyword_repeated[keyword_index]) - ord('A')  # Converte a letra da palavra-chave para um valor numérico
            p_val = (c_val - k_val + 26) % 26  # Calcula o valor da letra decifrada
            plaintext += chr(p_val + ord('A'))  # Converte o valor numérico de volta para uma letra
            keyword_index += 1

    return plaintext

# Função principal para quebrar a cifra de Vigenère
def break_vigenere(ciphertext):
    likely_key_lengths = kasiski_examination(ciphertext)  # Tenta determinar os comprimentos de chave prováveis usando o método de Kasiski
    if not likely_key_lengths:
        print("Método de Kasiski falhou, tentando índice de coincidência...")
        likely_key_lengths = find_key_length_by_ic(ciphertext)  # Se o método de Kasiski falhar, tenta usar o índice de coincidência

    if not likely_key_lengths:
        print("Não foi possível determinar o comprimento da chave.")
        return

    for key_length in likely_key_lengths:
        key = frequency_analysis(ciphertext, key_length)  # Realiza a análise de frequência para encontrar a chave
        plaintext = decrypt_vigenere(ciphertext, key)  # Decifra o texto cifrado usando a chave encontrada
        print(f"Possível chave: {key}")
        print(f"Texto decifrado: {plaintext[:100]}...")  # Mostra os primeiros 100 caracteres do texto decifrado
        print()

# Exemplo de uso
ciphertext = "GQSNWU PZOQ DLOJ MZQT"  # Substitua isso pelo seu texto cifrado
break_vigenere(ciphertext)
