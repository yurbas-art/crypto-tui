import sys
sys.path.insert(0, '.')

import pytest
import tempfile
import os
from app.services.cipher_service import CipherService
from app.services.file_service import FileService


@pytest.fixture
def services():
    return CipherService(), FileService()


@pytest.fixture
def plain_file(tmp_path):
    f = tmp_path / "plain.txt"
    f.write_text("ПРИВЕТ МИР ЭТО ТЕСТОВЫЙ ТЕКСТ", encoding="utf-8")
    return str(f)


def test_read_encrypt_write_read(services, plain_file, tmp_path):
    cipher_svc, file_svc = services
    text = file_svc.read_file(plain_file)
    encrypted = cipher_svc.encrypt_caesar(text, 7)
    out = str(tmp_path / "encrypted.txt")
    file_svc.write_file(out, encrypted)
    assert file_svc.read_file(out) == encrypted


def test_encrypt_then_decrypt_equals_original(services, plain_file):
    cipher_svc, file_svc = services
    original = file_svc.read_file(plain_file)
    encrypted = cipher_svc.encrypt_caesar(original, 7)
    decrypted = cipher_svc.decrypt_caesar(encrypted, 7)
    assert decrypted == original
