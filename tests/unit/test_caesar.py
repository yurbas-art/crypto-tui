import sys
sys.path.insert(0, '.')

import pytest
from app.ciphers.caesar import encrypt, decrypt, ALPHABET_SIZE


def test_round_trip():
    assert decrypt(encrypt("ПРИВЕТ", 3), 3) == "ПРИВЕТ"

def test_key_zero():
    assert encrypt("ПРИВЕТ", 0) == "ПРИВЕТ"

def test_key_mod_alphabet():
    assert encrypt("ПРИВЕТ", ALPHABET_SIZE) == encrypt("ПРИВЕТ", 0)

def test_negative_key():
    assert decrypt(encrypt("МИР", -5), -5) == "МИР"

def test_non_alphabet_chars_unchanged():
    result = encrypt("ПРИВЕТ, МИР! 123", 3)
    assert ", " in result
    assert "! 123" in result
