import sys
sys.path.insert(0, '.')

import pytest
from app.analysis.kasiski import (
    index_of_coincidence, estimate_key_length,
    guess_key_length, guess_key, auto_decrypt_vigenere, RU_IC,
)
from app.ciphers import vigenere


LONG_TEXT = (
    "СЕГОДНЯ ОЧЕНЬ ХОРОШАЯ ПОГОДА ДЛЯ ПРОГУЛКИ ПО УЛИЦАМ НАШЕГО ГОРОДА "
    "СОЛНЦЕ СВЕТИТ ЯРКО И НЕБО ГОЛУБОЕ БЕЗ ЕДИНОГО ОБЛАКА НА ГОРИЗОНТЕ "
    "ДЕТИ ИГРАЮТ ВО ДВОРЕ А ВЗРОСЛЫЕ ОТДЫХАЮТ НА СКАМЕЙКАХ В ПАРКЕ "
    "ДЕРЕВЬЯ ЗЕЛЕНЕЮТ И ПТИЦЫ ПОЮТ СВОИ ВЕСЕЛЫЕ ПЕСНИ НАД ГОЛОВОЙ "
) * 4


def test_ic_of_natural_text_close_to_reference():
    ic = index_of_coincidence(LONG_TEXT)
    assert abs(ic - RU_IC) < 0.02

def test_ic_empty_text_is_zero():
    assert index_of_coincidence("") == 0.0

def test_ic_single_char_is_zero():
    assert index_of_coincidence("А") == 0.0

def test_estimate_key_length_returns_sorted_dict():
    enc = vigenere.encrypt(LONG_TEXT, "КЛЮЧ")
    estimates = estimate_key_length(enc, max_length=10)
    values = list(estimates.values())
    assert values == sorted(values, reverse=True)

def test_guess_key_length_for_key_length_four():
    enc = vigenere.encrypt(LONG_TEXT, "ШИФР")
    assert guess_key_length(enc, max_length=10) == 4

def test_guess_key_for_known_length():
    enc = vigenere.encrypt(LONG_TEXT, "КЛЮЧ")
    assert guess_key(enc, key_length=4) == "КЛЮЧ"

def test_auto_decrypt_vigenere_recovers_text():
    enc = vigenere.encrypt(LONG_TEXT, "ШИФР")
    decrypted, key = auto_decrypt_vigenere(enc, max_length=10)
    assert key == "ШИФР"
    assert decrypted == LONG_TEXT
