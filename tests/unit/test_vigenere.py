import sys
sys.path.insert(0, '.')

import pytest
from app.ciphers.vigenere import encrypt, decrypt


def test_round_trip():
    assert decrypt(encrypt("ПРИВЕТ", "КЛЮЧ"), "КЛЮЧ") == "ПРИВЕТ"

def test_key_shorter_than_text():
    text = "АБВГДЕЖЗИЙКЛМН"
    assert decrypt(encrypt(text, "АБ"), "АБ") == text

def test_spaces_do_not_shift_key_index():
    enc1 = encrypt("АБВГД", "КЛ")
    enc2 = encrypt("АБ ВГД", "КЛ")
    assert enc2.replace(" ", "") == enc1

def test_empty_key_raises():
    with pytest.raises(ValueError):
        encrypt("ТЕКСТ", "")
