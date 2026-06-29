import sys
sys.path.insert(0, '.')

import pytest
from app.analysis.frequency import (
    count_frequencies, relative_frequencies,
    guess_caesar_key, auto_decrypt_caesar,
)
from app.ciphers.caesar import encrypt


def test_count_frequencies_sum():
    text = "ААББВ"
    counts = count_frequencies(text)
    assert counts["А"] == 2
    assert counts["Б"] == 2
    assert counts["В"] == 1

def test_relative_frequencies_sum():
    text = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" * 3
    freqs = relative_frequencies(text)
    assert abs(sum(freqs.values()) - 1.0) < 0.001

def test_empty_text_returns_zero_key():
    assert guess_caesar_key("") == 0

def test_guess_caesar_key():
    long_text = "СОЛНЕЧНЫЙ ДЕНЬ ОЧЕНЬ ХОРОШО ДЛЯ ПРОГУЛКИ ПО УЛИЦАМ НАШЕГО ГОРОДА" * 5
    enc = encrypt(long_text, 5)
    assert guess_caesar_key(enc) == 5

def test_auto_decrypt_caesar():
    long_text = "СЕГОДНЯ ОЧЕНЬ ХОРОШАЯ ПОГОДА ДЛЯ ПРОГУЛКИ ПО ГОРОДУ" * 5
    enc = encrypt(long_text, 11)
    decrypted, key = auto_decrypt_caesar(enc)
    assert key == 11
    assert decrypted == long_text
