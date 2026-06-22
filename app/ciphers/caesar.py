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
        text: Исходный текст (верхний или нижний регистр).
        key:  Числовой ключ сдвига.

    Returns:
        Зашифрованный текст.
    """
    raise NotImplementedError


def decrypt(text: str, key: int) -> str:
    """Расшифровать текст шифром Цезаря.

    Args:
        text: Зашифрованный текст.
        key:  Числовой ключ сдвига.

    Returns:
        Расшифрованный текст.
    """
    raise NotImplementedError
