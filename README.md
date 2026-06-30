# crypto-tui

TUI-приложение для шифрования, дешифрования и криптоанализа текстовых файлов на основе классических шифров.

## Возможности

- **Шифр Цезаря** — шифрование и дешифрование с числовым ключом
- **Шифр Виженера** — шифрование и дешифрование с ключевым словом
- **Шифр Полибия** — шифрование и дешифрование по таблице
- **Частотный анализ** — определение вероятного ключа и автодешифрование
- **Работа с файлами** — чтение `.txt`, сохранение результата
- **TUI-интерфейс** — на базе библиотеки [Textual](https://github.com/Textualize/textual)

## Стек

| Технология | Назначение |
|---|---|
| Python 3.12 | Основной язык |
| Textual | TUI-интерфейс |
| Pytest | Тестирование |
| Docker | Контейнеризация |

## Структура проекта

```
.
├── app
│   ├── analysis
│   │   ├── frequency.py
│   │   ├── __init__.py
│   │   └── kasiski.py
│   ├── ciphers
│   │   ├── caesar.py
│   │   ├── __init__.py
│   │   ├── polybius.py
│   │   └── vigenere.py
│   ├── __init__.py
│   ├── services
│   │   ├── cipher_service.py
│   │   ├── file_service.py
│   │   └── __init__.py
│   └── ui
│       ├── __init__.py
│       └── textual_app.py
├── docker-compose.yml
├── Dockerfile
├── docs
│   ├── architecture.md
│   ├── project.md
│   └── user_guide.md
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── test_data
│   ├── encrypted_caesar.txt
│   ├── encrypted_polybius.txt
│   ├── encrypted_vigenere.txt
│   ├── invalid.txt
│   ├── plain_long.txt
│   └── plain_short.txt
└── tests
    ├── integration
    │   ├── test_file_cipher.py
    │   └── test_pipeline.py
    └── unit
        ├── test_caesar.py
        ├── test_frequency.py
        ├── test_kasiski.py
        ├── test_polybius.py
        └── test_vigenere.py
```

## Запуск

### Локально

```bash
git clone https://github.com/yurbas-art/crypto-tui.git
cd crypto-tui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Docker

```bash
docker build -t crypto-tui .
docker run -it crypto-tui
```

## Тестирование

```bash
pytest tests/ -v
```

## Алгоритмы

**Цезарь**

```
E(x) = (x + k) mod n
D(x) = (x − k) mod n
```

**Виженер** — полиалфавитный шифр, ключ — слово. Каждый символ сдвигается на значение соответствующей буквы ключа.

**Полибий** — символы кодируются координатами в таблице 6×6 (русский алфавит).

**Частотный анализ** — вычисляет относительные частоты символов `p = nᵢ / N` и сопоставляет с эталонным распределением русского языка для определения ключа Цезаря.

## Документация

- [`docs/user_guide.md`](docs/user_guide.md) — руководство пользователя
- [`docs/architecture.md`](docs/architecture.md) — описание архитектуры

---

Учебно-ознакомительная практика, ВВГУ, кафедра ИТС, 2026.
