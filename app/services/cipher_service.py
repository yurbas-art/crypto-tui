from __future__ import annotations
from dataclasses import dataclass

from app.ciphers import caesar
from app.ciphers import vigenere
from app.ciphers import polybius
from app.analysis import frequency
from app.analysis import kasiski


@dataclass
class KasiskiResult:
    key_length_estimates: dict[int, float]
    probable_key_length: int
    probable_key: str
    decrypted_text: str


@dataclass
class FrequencyResult:
    frequencies: dict[str, float]
    probable_key: int
    decrypted_text: str


class CipherService:
    def encrypt_caesar(self, text: str, key: int) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return caesar.encrypt(text, key)

    def decrypt_caesar(self, text: str, key: int) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return caesar.decrypt(text, key)

    def encrypt_vigenere(self, text: str, key: str) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return vigenere.encrypt(text, key)

    def decrypt_vigenere(self, text: str, key: str) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return vigenere.decrypt(text, key)

    def encrypt_polybius(self, text: str) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return polybius.encrypt(text)

    def decrypt_polybius(self, text: str) -> str:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        return polybius.decrypt(text)

    def frequency_analysis(self, text: str) -> FrequencyResult:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        freqs = frequency.relative_frequencies(text)
        decrypted, key = frequency.auto_decrypt_caesar(text)
        return FrequencyResult(
            frequencies=freqs,
            probable_key=key,
            decrypted_text=decrypted,
        )

    def break_vigenere(self, text: str, max_key_length: int = 15) -> KasiskiResult:
        if not text.strip():
            raise ValueError("Текст не может быть пустым")
        estimates = kasiski.estimate_key_length(text, max_key_length)
        key_length = kasiski.guess_key_length(text, max_key_length)
        decrypted, key = kasiski.auto_decrypt_vigenere(text, max_key_length)
        return KasiskiResult(
            key_length_estimates=estimates,
            probable_key_length=key_length,
            probable_key=key,
            decrypted_text=decrypted,
        )
