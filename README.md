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
classical-crypto/
├── app/
│   ├── ciphers/
│   │   ├── caesar.py
│   │   ├── vigenere.py
│   │   └── polybius.py
│   ├── analysis/
│   │   └── frequency.py
│   ├── services/
│   │   ├── cipher_service.py
│   │   └── file_service.py
│   └── ui/
│       └── textual_app.py
├── tests/
│   ├── unit/
│   └── integration/
├── test_data/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── main.py
```

## Запуск

### Локально

```bash
git clone https://github.com/yurbas-art/crypto-tui.git
cd crypto-tui
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
