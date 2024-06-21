from collections import Counter
import re

def find_repeated_sequences_spacings(ciphertext):
    spacings = {}
    for seq_len in range(3, 6):
        for i in range(len(ciphertext) - seq_len):
            seq = ciphertext[i:i + seq_len]
            for j in range(i + seq_len, len(ciphertext) - seq_len):
                if ciphertext[j:j + seq_len] == seq:
                    if seq not in spacings:
                        spacings[seq] = []
                    spacings[seq].append(j - i)
    return spacings

def kasiski_examination(ciphertext):
    spacings = find_repeated_sequences_spacings(ciphertext)
    spacing_freqs = Counter()
    for seq in spacings:
        for space in spacings[seq]:
            spacing_freqs[space] += 1
    likely_key_lengths = [spacing for spacing, freq in spacing_freqs.most_common()]
    return likely_key_lengths

def calculate_index_of_coincidence(text):
    N = len(text)
    frequency_sum = sum([freq * (freq - 1) for freq in Counter(text).values()])
    return frequency_sum / (N * (N - 1)) if N > 1 else 0

def find_key_length_by_ic(ciphertext):
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    avg_ic = 0.068
    key_length_candidates = []

    for key_length in range(1, 21):  # Assume key length is between 1 and 20
        ic_sum = 0
        for i in range(key_length):
            nth_subtext = ciphertext[i::key_length]
            ic_sum += calculate_index_of_coincidence(nth_subtext)
        avg_ic_for_length = ic_sum / key_length
        if abs(avg_ic_for_length - avg_ic) < 0.01:  # Tolerance level for IC comparison
            key_length_candidates.append(key_length)

    return key_length_candidates

def frequency_analysis(ciphertext, key_length):
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    key = ''
    for i in range(key_length):
        nth_letters = ciphertext[i::key_length]
        freq_counter = Counter(nth_letters)
        most_common_letter, _ = freq_counter.most_common(1)[0]
        key += chr(((ord(most_common_letter) - ord('E') + 26) % 26) + ord('A'))
    return key

def decrypt_vigenere(ciphertext, keyword):
    ciphertext = ciphertext.upper()
    keyword = keyword.upper().replace(" ", "")
    keyword_repeated = (keyword * ((len(ciphertext) // len(keyword)) + 1))[:len(ciphertext)]
    
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

def break_vigenere(ciphertext):
    likely_key_lengths = kasiski_examination(ciphertext)
    if not likely_key_lengths:
        print("Método de Kasiski falhou, tentando índice de coincidência...")
        likely_key_lengths = find_key_length_by_ic(ciphertext)

    if not likely_key_lengths:
        print("Não foi possível determinar o comprimento da chave.")
        return

    for key_length in likely_key_lengths:
        key = frequency_analysis(ciphertext, key_length)
        plaintext = decrypt_vigenere(ciphertext, key)
        print(f"Possível chave: {key}")
        print(f"Texto decifrado: {plaintext[:100]}...")  # Mostra os primeiros 100 caracteres do texto decifrado
        print()

ciphertext = "GQSNWU PZOQ DLOJ MZQT"  # Substitua isso pelo seu texto cifrado
break_vigenere(ciphertext)
