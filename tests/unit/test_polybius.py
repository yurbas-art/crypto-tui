import sys
sys.path.insert(0, '.')

import pytest
from app.ciphers.polybius import encrypt, decrypt, CHAR_TO_COORDS, SYMBOLS


ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def test_round_trip():
    assert decrypt(encrypt("ПРИВЕТ")) == "ПРИВЕТ"

def test_all_alphabet_in_table():
    for ch in ALPHABET:
        assert ch in CHAR_TO_COORDS, f"Буква {ch} не найдена в таблице"

def test_punctuation_encoded():
    result = encrypt("ПРИВЕТ.")
    assert result != ""
    decoded = decrypt(result)
    assert decoded == "ПРИВЕТ."

def test_invalid_coords_raise():
    with pytest.raises(ValueError):
        decrypt("99")
