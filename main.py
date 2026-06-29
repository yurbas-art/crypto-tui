"""
Точка входа приложения classical-crypto.

Запуск:
    python main.py

Docker:
    docker build -t classical-crypto .
    docker run -it classical-crypto
"""

import sys
from pathlib import Path

# Гарантируем что корень проекта в sys.path,
# чтобы пакет app был импортируемым при запуске
# через `python main.py` из любой директории.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.textual_app import CryptoApp


def main() -> None:
    """Запустить TUI-приложение."""
    app = CryptoApp()
    app.run()


if __name__ == "__main__":
    main()
