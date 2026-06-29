"""
Шифр Цезаря.

E(x) = (x + k) mod n
D(x) = (x - k) mod n
"""

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)


def encrypt(text: str, key: int) -> str:
    """Зашифровать текст шифром Цезаря.

    Args:
        text: Исходный текст. Поддерживается верхний и нижний регистр.
        key:  Числовой ключ сдвига. Допускаются отрицательные значения.

    Returns:
        Зашифрованный текст. Символы вне алфавита остаются без изменений.
    """
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
    """Расшифровать текст шифром Цезаря.

    Args:
        text: Зашифрованный текст.
        key:  Числовой ключ сдвига.

    Returns:
        Расшифрованный текст.
    """
    return encrypt(text, -key)
