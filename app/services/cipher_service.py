"""
Сервис шифрования — паттерн Facade.

Предоставляет единый интерфейс к модулям алгоритмического слоя.
UI работает только с этим классом и не импортирует шифры напрямую.
"""

from __future__ import annotations
from dataclasses import dataclass

from app.ciphers import caesar
from app.ciphers import vigenere
from app.ciphers import polybius
from app.analysis import frequency


@dataclass
class FrequencyResult:
    """Результат частотного анализа."""
    frequencies: dict[str, float]
    probable_key: int
    decrypted_text: str


class CipherService:
    """Фасад над модулями шифрования и анализа."""

    def encrypt_caesar(self, text: str, key: int) -> str:
        """Зашифровать текст шифром Цезаря.

        Args:
            text: Исходный текст.
            key:  Числовой ключ.

        Returns:
            Зашифрованный текст.

        Raises:
            ValueError: Если текст пуст.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return caesar.encrypt(text, key)

    def decrypt_caesar(self, text: str, key: int) -> str:
        """Расшифровать текст шифром Цезаря.

        Args:
            text: Зашифрованный текст.
            key:  Числовой ключ.

        Returns:
            Расшифрованный текст.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return caesar.decrypt(text, key)

    def encrypt_vigenere(self, text: str, key: str) -> str:
        """Зашифровать текст шифром Виженера.

        Args:
            text: Исходный текст.
            key:  Ключевое слово.

        Returns:
            Зашифрованный текст.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return vigenere.encrypt(text, key)

    def decrypt_vigenere(self, text: str, key: str) -> str:
        """Расшифровать текст шифром Виженера.

        Args:
            text: Зашифрованный текст.
            key:  Ключевое слово.

        Returns:
            Расшифрованный текст.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return vigenere.decrypt(text, key)

    def encrypt_polybius(self, text: str) -> str:
        """Зашифровать текст шифром Полибия.

        Args:
            text: Исходный текст.

        Returns:
            Строка пар координат.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return polybius.encrypt(text)

    def decrypt_polybius(self, text: str) -> str:
        """Расшифровать текст шифром Полибия.

        Args:
            text: Строка пар координат («11 32 21 ...»).

        Returns:
            Восстановленный текст.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return polybius.decrypt(text)

    def frequency_analysis(self, text: str) -> FrequencyResult:
        """Выполнить частотный анализ и автодешифрование шифра Цезаря.

        Args:
            text: Зашифрованный текст.

        Returns:
            FrequencyResult с частотами, вероятным ключом и расшифровкой.
        """
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        freqs = frequency.relative_frequencies(text)
        decrypted, key = frequency.auto_decrypt_caesar(text)
        return FrequencyResult(
            frequencies=freqs,
            probable_key=key,
            decrypted_text=decrypted,
        )
