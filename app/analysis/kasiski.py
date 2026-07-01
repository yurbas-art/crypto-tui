from __future__ import annotations

from app.analysis import frequency
from app.ciphers.caesar import decrypt as caesar_decrypt

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)

RU_IC = 0.0553

MAX_KEY_LENGTH = 15


def index_of_coincidence(text: str) -> float:
    counts = frequency.count_frequencies(text)
    n = sum(counts.values())
    if n < 2:
        return 0.0

    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def _split_into_streams(text: str, key_length: int) -> list[str]:
    letters = [ch for ch in text.upper() if ch in ALPHABET]
    streams = ["" for _ in range(key_length)]
    for idx, ch in enumerate(letters):
        streams[idx % key_length] += ch
    return streams


def estimate_key_length(text: str, max_length: int = MAX_KEY_LENGTH) -> dict[int, float]:
    results: dict[int, float] = {}
    for length in range(1, max_length + 1):
        streams = _split_into_streams(text, length)
        ics = [index_of_coincidence(s) for s in streams if len(s) >= 2]
        if not ics:
            results[length] = 0.0
            continue
        results[length] = sum(ics) / len(ics)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def guess_key_length(text: str, max_length: int = MAX_KEY_LENGTH, tolerance: float = 0.006) -> int:
    estimates = estimate_key_length(text, max_length)
    if not estimates:
        return 1

    by_closeness = sorted(estimates, key=lambda length: abs(estimates[length] - RU_IC))
    best_score = abs(estimates[by_closeness[0]] - RU_IC)

    candidates = [
        length for length in by_closeness
        if abs(estimates[length] - RU_IC) <= best_score + tolerance
    ]
    return min(candidates)


def guess_key(text: str, key_length: int) -> str:
    streams = _split_into_streams(text, key_length)
    key_chars = []
    for stream in streams:
        shift = frequency.guess_caesar_key(stream)
        key_chars.append(ALPHABET[shift])
    return "".join(key_chars)


def auto_decrypt_vigenere(text: str, max_length: int = MAX_KEY_LENGTH) -> tuple[str, str]:
    from app.ciphers import vigenere

    key_length = guess_key_length(text, max_length)
    key = guess_key(text, key_length)
    decrypted = vigenere.decrypt(text, key)
    return decrypted, key
