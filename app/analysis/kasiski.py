"""
Оценка длины ключа шифра Виженера методом индекса совпадений.

Индекс совпадений (Index of Coincidence, IC) — вероятность того,
что два случайно выбранных символа текста совпадают:

    IC = Σ nᵢ(nᵢ - 1) / [N(N - 1)]

где nᵢ — частота i-й буквы, N — длина текста.

Для текста на естественном русском языке IC ≈ 0.0553.
Для случайного (равномерного) текста IC ≈ 1/32 ≈ 0.0313.

Идея метода:
1. Перебираем предполагаемую длину ключа m = 1, 2, 3, ...
2. Разбиваем шифртекст на m подпотоков (каждый m-й символ начиная
   со смещения i), считаем IC каждого подпотока.
3. Если шифртекст разбит на подпотоки правильной длиной ключа —
   каждый подпоток зашифрован одним и тем же сдвигом Цезаря,
   и его IC близок к IC естественного языка (≈0.0553).
4. Длина ключа с наибольшим средним IC — наиболее вероятная.

После определения длины ключа каждая буква ключа находится
частотным анализом соответствующего подпотока (как для Цезаря).

Практическое ограничение метода: для надёжного определения каждой
буквы ключа частотным анализом требуется от ~150-200 символов
на подпоток. Например, при длине ключа 4 это означает зашифрованный
текст не короче ~800-1000 букв. На более коротких текстах длина
ключа обычно определяется верно, но отдельные буквы ключа могут
быть угаданы с ошибкой из-за статистических колебаний на малой
выборке — это не ошибка реализации, а фундаментальное ограничение
частотного анализа на малых объёмах данных.
"""

from __future__ import annotations

from app.analysis import frequency
from app.ciphers.caesar import decrypt as caesar_decrypt

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(ALPHABET)

# Эталонный индекс совпадений для русского языка
RU_IC = 0.0553

MAX_KEY_LENGTH = 15


def index_of_coincidence(text: str) -> float:
    """Вычислить индекс совпадений для текста.

    Символы не из алфавита игнорируются.

    Args:
        text: Анализируемый текст.

    Returns:
        Значение IC. Для пустого текста или текста короче 2 букв
        возвращается 0.0.
    """
    counts = frequency.count_frequencies(text)
    n = sum(counts.values())
    if n < 2:
        return 0.0

    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def _split_into_streams(text: str, key_length: int) -> list[str]:
    """Разбить текст (только буквы алфавита) на key_length подпотоков.

    Args:
        text:       Шифртекст.
        key_length: Предполагаемая длина ключа.

    Returns:
        Список подпотоков, i-й подпоток содержит символы
        с индексами i, i + key_length, i + 2*key_length, ...
    """
    letters = [ch for ch in text.upper() if ch in ALPHABET]
    streams = ["" for _ in range(key_length)]
    for idx, ch in enumerate(letters):
        streams[idx % key_length] += ch
    return streams


def estimate_key_length(text: str, max_length: int = MAX_KEY_LENGTH) -> dict[int, float]:
    """Оценить длину ключа Виженера методом индекса совпадений.

    Для каждой длины ключа от 1 до max_length вычисляется средний IC
    по всем подпотокам. Длина с IC, наиболее близким к эталону
    русского языка (RU_IC), является наиболее вероятной.

    Args:
        text:       Зашифрованный текст (шифр Виженера).
        max_length: Максимальная проверяемая длина ключа.

    Returns:
        Словарь {длина_ключа: средний_IC}, отсортированный по
        убыванию среднего IC (первый ключ — наиболее вероятный).
    """
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
    """Вернуть наиболее вероятную длину ключа Виженера.

    IC-метод нередко даёт высокий IC и для длин, кратных истинной
    длине ключа (например, 8 при реальной длине 4) — это ожидаемо,
    так как подпотоки для длины 2m являются объединением подпотоков
    для длины m. Поэтому среди длин с IC близким к лучшему результату
    выбирается наименьшая (минимальный делитель).

    Args:
        text:       Зашифрованный текст.
        max_length: Максимальная проверяемая длина ключа.
        tolerance:  Допустимое отклонение IC от наилучшего значения,
                    при котором длины считаются равнозначными.

    Returns:
        Длина ключа, чей средний IC ближе всего к эталону русского
        языка. Если текст пуст — возвращает 1.
    """
    estimates = estimate_key_length(text, max_length)
    if not estimates:
        return 1

    # Сортируем по близости IC к эталону
    by_closeness = sorted(estimates, key=lambda length: abs(estimates[length] - RU_IC))
    best_score = abs(estimates[by_closeness[0]] - RU_IC)

    # Среди длин с похожим результатом берём наименьшую
    candidates = [
        length for length in by_closeness
        if abs(estimates[length] - RU_IC) <= best_score + tolerance
    ]
    return min(candidates)


def guess_key(text: str, key_length: int) -> str:
    """Подобрать сами буквы ключа известной длины частотным анализом.

    Каждый подпоток (зашифрован одним сдвигом Цезаря) анализируется
    отдельно методом частотного анализа.

    Args:
        text:       Зашифрованный текст.
        key_length: Известная или предполагаемая длина ключа.

    Returns:
        Предполагаемое ключевое слово длиной key_length.
    """
    streams = _split_into_streams(text, key_length)
    key_chars = []
    for stream in streams:
        shift = frequency.guess_caesar_key(stream)
        key_chars.append(ALPHABET[shift])
    return "".join(key_chars)


def auto_decrypt_vigenere(text: str, max_length: int = MAX_KEY_LENGTH) -> tuple[str, str]:
    """Автоматически оценить ключ и расшифровать текст Виженера.

    Args:
        text:       Зашифрованный текст.
        max_length: Максимальная проверяемая длина ключа.

    Returns:
        Кортеж (расшифрованный_текст, предполагаемый_ключ).
    """
    from app.ciphers import vigenere

    key_length = guess_key_length(text, max_length)
    key = guess_key(text, key_length)
    decrypted = vigenere.decrypt(text, key)
    return decrypted, key
