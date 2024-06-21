# Cifra de Vigenère

- Por: Yuri Braz (ybraz@proton.me)
- Versão: 0.1
- Data: 21/06/2024

A cifra de Vigenère é um método de criptografia que usa uma palavra-chave para cifrar e decifrar mensagens. 
Em vez de substituir cada letra da mensagem por uma letra fixa (como na cifra de César), 
a cifra de Vigenère usa uma série de diferentes substituições baseadas em uma palavra-chave.

**Criptografia:
- Suponha que a soma das posições das letras "V" (22ª letra) e "M" (13ª letra) ultrapasse 26.
- Some as posições: 22 + 13 = 35.
- Use o módulo 26 para ajustar: 35 % 26 = 9.
- A 9ª letra do alfabeto é "I".

**Descriptografia:
- Suponha que subtrair as posições das letras "I" (9ª letra) e "M" (13ª letra) resulte em um valor negativo.
- Subtraia as posições: 9 - 13 = -4.
- Para obter um valor positivo dentro do intervalo do alfabeto, podemos adicionar 26 e então aplicar o módulo 26: (-4 + 26) % 26 = 22.
- A 22ª letra do alfabeto é "V".

Uso: > python.exe .\vinegere-cipher.py 1 "Texto para criptografar" "CHAOS" 
Texto cifrado: VLXHG RHRO UTPPHGIYATST
> python.exe .\vinegere-cipher.py 2 "VLXHG RHRO UTPPHGIYATST" "CHAOS"
Texto decifrado: TEXTO PARA CRIPTOGRAFAR
