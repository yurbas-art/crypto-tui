"""
Шифр Полибия (квадрат Полибия).

Каждый символ кодируется парой координат (строка, столбец)
в таблице 6×6. Координаты нумеруются с 1.

Таблица:
     1  2  3  4  5  6
  1  А  Б  В  Г  Д  Е
  2  Ж  З  И  Й  К  Л
  3  М  Н  О  П  Р  С
  4  Т  У  Ф  Х  Ц  Ч
  5  Ш  Щ  Ъ  Ы  Ь  Э
  6  Ю  Я  .  ,  !  ?
"""

TABLE_SIZE = 6
SYMBOLS = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ.,!?"

TABLE: list[list[str]] = []
CHAR_TO_COORDS: dict[str, tuple[int, int]] = {}
COORDS_TO_CHAR: dict[tuple[int, int], str] = {}


def build_table() -> None:
    global TABLE, CHAR_TO_COORDS, COORDS_TO_CHAR
    TABLE = []
    CHAR_TO_COORDS = {}
    COORDS_TO_CHAR = {}

    idx = 0
    for row in range(TABLE_SIZE):
        table_row = []
        for col in range(TABLE_SIZE):
            char = SYMBOLS[idx] if idx < len(SYMBOLS) else ""
            table_row.append(char)
            if char:
                coords = (row + 1, col + 1)
                CHAR_TO_COORDS[char] = coords
                COORDS_TO_CHAR[coords] = char
            idx += 1
        TABLE.append(table_row)


def encrypt(text: str) -> str:
    parts = []
    for char in text.upper():
        if char in CHAR_TO_COORDS:
            row, col = CHAR_TO_COORDS[char]
            parts.append(f"{row}{col}")
    return " ".join(parts)


def decrypt(text: str) -> str:
    result = []
    for pair in text.strip().split():
        if len(pair) != 2 or not pair.isdigit():
            raise ValueError(f"Некорректная пара координат: '{pair}'")
        row, col = int(pair[0]), int(pair[1])
        coords = (row, col)
        if coords not in COORDS_TO_CHAR:
            raise ValueError(f"Координаты {coords} не найдены в таблице")
        result.append(COORDS_TO_CHAR[coords])
    return "".join(result)


build_table()
