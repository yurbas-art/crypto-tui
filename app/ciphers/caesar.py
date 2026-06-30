"""
Шифр Цезаря.

E(x) = (x + k) mod n
D(x) = (x - k) mod n
"""

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)


def encrypt(text: str, key: int) -> str:
    result = []
    for char in text:
        upper = char.upper()
        if upper in ALPHABET:
            idx = ALPHABET.index(upper)
            new_idx = (idx + key) % ALPHABET_SIZE
            encrypted = ALPHABET[new_idx]
            result.append(encrypted if char.isupper() else encrypted.lower())
        else:
            result.append(char)
    return "".join(result)


def decrypt(text: str, key: int) -> str:
    return encrypt(text, -key)
