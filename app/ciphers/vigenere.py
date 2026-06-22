"""
Шифр Виженера.

Полиалфавитный шифр. Каждый символ открытого текста сдвигается
на значение соответствующей буквы ключевого слова.

E(xᵢ) = (xᵢ + kᵢ) mod n
D(xᵢ) = (xᵢ - kᵢ) mod n
"""


ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)


def encrypt(text: str, key: str) -> str:
    """Зашифровать текст шифром Виженера.

    Args:
        text: Исходный текст.
        key:  Ключевое слово (только буквы алфавита).

    Returns:
        Зашифрованный текст.
    """
    raise NotImplementedError


def decrypt(text: str, key: str) -> str:
    """Расшифровать текст шифром Виженера.

    Args:
        text: Зашифрованный текст.
        key:  Ключевое слово.

    Returns:
        Расшифрованный текст.
    """
    raise NotImplementedError
