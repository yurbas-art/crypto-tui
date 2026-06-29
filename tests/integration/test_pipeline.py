import sys
sys.path.insert(0, '.')

import pytest
from app.services.cipher_service import CipherService
from app.services.file_service import FileService


@pytest.fixture
def cipher_svc():
    return CipherService()


@pytest.fixture
def long_text():
    return (
        "СЕГОДНЯ ОЧЕНЬ ХОРОШАЯ ПОГОДА ДЛЯ ПРОГУЛКИ ПО УЛИЦАМ НАШЕГО ГОРОДА "
        "СОЛНЦЕ СВЕТИТ ЯРКО И НЕБО ГОЛУБОЕ БЕЗ ЕДИНОГО ОБЛАКА "
        "ДЕТИ ИГРАЮТ ВО ДВОРЕ А ВЗРОСЛЫЕ ОТДЫХАЮТ НА СКАМЕЙКАХ "
    ) * 3


def test_vigenere_pipeline(cipher_svc, long_text):
    encrypted = cipher_svc.encrypt_vigenere(long_text, "КЛЮЧ")
    decrypted = cipher_svc.decrypt_vigenere(encrypted, "КЛЮЧ")
    assert decrypted == long_text


def test_frequency_auto_decrypt_pipeline(cipher_svc, long_text):
    encrypted = cipher_svc.encrypt_caesar(long_text, 9)
    result = cipher_svc.frequency_analysis(encrypted)
    assert result.probable_key == 9
    assert result.decrypted_text == long_text
