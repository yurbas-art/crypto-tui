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
    """Привести ключ к верхнему регистру и проверить что он не пустой.

    Args:
        key: Ключевое слово.

    Returns:
        Ключ в верхнем регистре.

    Raises:
        ValueError: Если ключ пустой или содержит символы вне алфавита.
    """
    key = key.upper().strip()
    if not key:
        raise ValueError("Ключ не может быть пустым")
    for ch in key:
        if ch not in ALPHABET:
            raise ValueError(f"Символ '{ch}' недопустим в ключе")
    return key


def encrypt(text: str, key: str) -> str:
    """Зашифровать текст шифром Виженера.

    Args:
        text: Исходный текст.
        key:  Ключевое слово (только буквы русского алфавита).

    Returns:
        Зашифрованный текст. Символы вне алфавита остаются без изменений,
        индекс ключа при этом не сдвигается.
    """
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
    """Расшифровать текст шифром Виженера.

    Args:
        text: Зашифрованный текст.
        key:  Ключевое слово.

    Returns:
        Расшифрованный текст.
    """
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
