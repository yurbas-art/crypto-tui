from __future__ import annotations

import os
from pathlib import Path


ALLOWED_EXTENSIONS = {".txt"}
DEFAULT_ENCODING = "utf-8"


class FileService:
    def validate_file_path(self, file_path: str) -> bool:
        path = Path(file_path)
        return (
            path.exists()
            and path.is_file()
            and path.suffix.lower() in ALLOWED_EXTENSIONS
        )

    def read_file(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        if path.is_dir():
            raise IsADirectoryError(f"Указан путь к директории: {file_path}")
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Недопустимое расширение: '{path.suffix}'. "
                f"Поддерживаются: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        content = path.read_text(encoding=DEFAULT_ENCODING)
        if not content.strip():
            raise ValueError("Файл пуст")
        return content

    def write_file(self, file_path: str, content: str) -> bool:
        if not content:
            raise ValueError("Нечего записывать: контент пуст")

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=DEFAULT_ENCODING)
        return True

    def get_file_info(self, file_path: str) -> dict:
        path = Path(file_path)
        if not path.exists():
            return {}
        return {
            "name": path.name,
            "size_bytes": path.stat().st_size,
            "extension": path.suffix,
        }
