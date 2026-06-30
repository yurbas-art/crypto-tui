from __future__ import annotations

from app.ciphers import caesar

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)

RU_FREQ: dict[str, float] = {
    "О": 0.1097, "Е": 0.0845, "А": 0.0801, "И": 0.0735, "Н": 0.0670,
    "Т": 0.0626, "С": 0.0547, "Р": 0.0473, "В": 0.0454, "Л": 0.0440,
    "К": 0.0349, "М": 0.0321, "Д": 0.0298, "П": 0.0281, "У": 0.0262,
    "Я": 0.0201, "Ы": 0.0190, "Ь": 0.0174, "Г": 0.0170, "З": 0.0165,
    "Б": 0.0159, "Ч": 0.0144, "Й": 0.0121, "Х": 0.0097, "Ж": 0.0094,
    "Ш": 0.0073, "Ю": 0.0064, "Ц": 0.0048, "Щ": 0.0036, "Э": 0.0032,
    "Ф": 0.0026, "Ъ": 0.0004,
}

MOST_FREQUENT_RU = max(RU_FREQ, key=RU_FREQ.__getitem__)


def count_frequencies(text: str) -> dict[str, int]:
    counts: dict[str, int] = {ch: 0 for ch in ALPHABET}
    for char in text.upper():
        if char in counts:
            counts[char] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def relative_frequencies(text: str) -> dict[str, float]:
    counts = count_frequencies(text)
    total = sum(counts.values())
    if total == 0:
        return {ch: 0.0 for ch in ALPHABET}
    return {ch: cnt / total for ch, cnt in counts.items()}


def guess_caesar_key(text: str) -> int:
    counts = count_frequencies(text)
    total = sum(counts.values())
    if total == 0:
        return 0

    most_common = max(counts, key=counts.__getitem__)
    enc_idx = ALPHABET.index(most_common)
    exp_idx = ALPHABET.index(MOST_FREQUENT_RU)
    return (enc_idx - exp_idx) % ALPHABET_SIZE


def auto_decrypt_caesar(text: str) -> tuple[str, int]:
    key = guess_caesar_key(text)
    return caesar.decrypt(text, key), key
