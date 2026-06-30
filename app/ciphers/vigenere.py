"""
Шифр Виженера.

Полиалфавитный шифр. Каждый символ текста сдвигается на значение
соответствующей буквы ключевого слова.

E(xᵢ) = (xᵢ + kᵢ) mod n
D(xᵢ) = (xᵢ - kᵢ) mod n
"""

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)


def _validate_key(key: str) -> str:
    key = key.upper().strip()
    if not key:
        raise ValueError("Ключ не может быть пустым")
    for ch in key:
        if ch not in ALPHABET:
            raise ValueError(f"Символ '{ch}' недопустим в ключе")
    return key


def encrypt(text: str, key: str) -> str:
    key = _validate_key(key)
    result = []
    key_idx = 0
    for char in text:
        upper = char.upper()
        if upper in ALPHABET:
            shift = ALPHABET.index(key[key_idx % len(key)])
            idx = ALPHABET.index(upper)
            new_idx = (idx + shift) % ALPHABET_SIZE
            encrypted = ALPHABET[new_idx]
            result.append(encrypted if char.isupper() else encrypted.lower())
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


def decrypt(text: str, key: str) -> str:
    key = _validate_key(key)
    result = []
    key_idx = 0
    for char in text:
        upper = char.upper()
        if upper in ALPHABET:
            shift = ALPHABET.index(key[key_idx % len(key)])
            idx = ALPHABET.index(upper)
            new_idx = (idx - shift) % ALPHABET_SIZE
            decrypted = ALPHABET[new_idx]
            result.append(decrypted if char.isupper() else decrypted.lower())
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)
