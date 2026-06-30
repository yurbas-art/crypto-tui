"""
TUI-приложение на базе Textual.
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input, TextArea, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal

from app.services.cipher_service import CipherService
from app.services.file_service import FileService


# ---------------------------------------------------------------------------
# Главное меню
# ---------------------------------------------------------------------------

class MainScreen(Screen):

    CSS = """
    MainScreen {
        align: center middle;
    }
    #menu {
        width: auto;
        height: auto;
    }
    #menu Static {
        text-align: center;
    }
    #menu Button {
        width: 32;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu"):
            yield Static("crypto-tui / классические шифры\n")
            yield Button("1. Шифр Цезаря",         id="caesar")
            yield Button("2. Шифр Виженера",       id="vigenere")
            yield Button("3. Шифр Полибия",        id="polybius")
            yield Button("4. Частотный анализ",    id="frequency")
            yield Button("5. Взлом Виженера (IC)", id="kasiski")
            yield Button("6. Выход",               id="exit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        routes = {
            "caesar":    CaesarScreen,
            "vigenere":  VigenereScreen,
            "polybius":  PolybiusScreen,
            "frequency": FrequencyScreen,
            "kasiski":   KasiskiScreen,
        }
        if event.button.id == "exit":
            self.app.exit()
        elif event.button.id in routes:
            self.app.push_screen(routes[event.button.id]())


# ---------------------------------------------------------------------------
# Вспомогательная функция: открыть / сохранить файл
# ---------------------------------------------------------------------------

def handle_file(event_id: str, path: str, text_in, text_out, status, file_svc) -> bool:
    """Обработать кнопки open/save. Возвращает True если действие выполнено."""
    if event_id == "open":
        if not path:
            status.update("[!] Укажите путь к файлу")
            return True
        try:
            text_in.load_text(file_svc.read_file(path))
            status.update(f"[OK] Загружено: {path}")
        except Exception as e:
            status.update(f"[!] {e}")
        return True

    if event_id == "save":
        if not path:
            status.update("[!] Укажите путь для сохранения")
            return True
        if not text_out.text.strip():
            status.update("[!] Нет результата для сохранения")
            return True
        try:
            file_svc.write_file(path, text_out.text)
            status.update(f"[OK] Сохранено: {path}")
        except Exception as e:
            status.update(f"[!] {e}")
        return True

    return False


# ---------------------------------------------------------------------------
# Шифр Цезаря
# ---------------------------------------------------------------------------

class CaesarScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("=== Шифр Цезаря ===\n")
        yield Label("Файл:")
        yield Horizontal(
            Input(placeholder="путь к файлу", id="file-path"),
            Button("Открыть", id="open"),
            Button("Сохранить", id="save"),
        )
        yield Label("Текст:")
        yield TextArea(id="text-in")
        yield Label("Ключ (число):")
        yield Input(placeholder="3", id="key")
        yield Static("", id="status")
        yield Horizontal(
            Button("Зашифровать", id="enc"),
            Button("Расшифровать", id="dec"),
            Button("← Назад", id="back"),
        )
        yield Label("Результат:")
        yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status   = self.query_one("#status", Static)
        text_in  = self.query_one("#text-in", TextArea)
        text_out = self.query_one("#text-out", TextArea)
        path     = self.query_one("#file-path", Input).value.strip()

        if event.button.id == "back":
            self.app.pop_screen(); return

        if handle_file(event.button.id, path, text_in, text_out, status, self.app.file_service):
            return

        text = text_in.text.strip()
        key_raw = self.query_one("#key", Input).value.strip()
        if not text:
            status.update("[!] Введите текст"); return
        if not key_raw:
            status.update("[!] Введите ключ"); return
        try:
            key = int(key_raw)
        except ValueError:
            status.update("[!] Ключ — целое число"); return

        svc = self.app.cipher_service
        try:
            if event.button.id == "enc":
                text_out.load_text(svc.encrypt_caesar(text, key))
                status.update(f"[OK] Зашифровано, ключ = {key}")
            elif event.button.id == "dec":
                text_out.load_text(svc.decrypt_caesar(text, key))
                status.update(f"[OK] Расшифровано, ключ = {key}")
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Шифр Виженера
# ---------------------------------------------------------------------------

class VigenereScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("=== Шифр Виженера ===\n")
        yield Label("Файл:")
        yield Horizontal(
            Input(placeholder="путь к файлу", id="file-path"),
            Button("Открыть", id="open"),
            Button("Сохранить", id="save"),
        )
        yield Label("Текст:")
        yield TextArea(id="text-in")
        yield Label("Ключевое слово:")
        yield Input(placeholder="КЛЮЧ", id="key")
        yield Static("", id="status")
        yield Horizontal(
            Button("Зашифровать", id="enc"),
            Button("Расшифровать", id="dec"),
            Button("← Назад", id="back"),
        )
        yield Label("Результат:")
        yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status   = self.query_one("#status", Static)
        text_in  = self.query_one("#text-in", TextArea)
        text_out = self.query_one("#text-out", TextArea)
        path     = self.query_one("#file-path", Input).value.strip()

        if event.button.id == "back":
            self.app.pop_screen(); return

        if handle_file(event.button.id, path, text_in, text_out, status, self.app.file_service):
            return

        text = text_in.text.strip()
        key  = self.query_one("#key", Input).value.strip()
        if not text: status.update("[!] Введите текст"); return
        if not key:  status.update("[!] Введите ключевое слово"); return

        svc = self.app.cipher_service
        try:
            if event.button.id == "enc":
                text_out.load_text(svc.encrypt_vigenere(text, key))
                status.update(f"[OK] Зашифровано, ключ = {key.upper()}")
            elif event.button.id == "dec":
                text_out.load_text(svc.decrypt_vigenere(text, key))
                status.update(f"[OK] Расшифровано, ключ = {key.upper()}")
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Шифр Полибия
# ---------------------------------------------------------------------------

class PolybiusScreen(Screen):

    TABLE = (
        "Таблица:\n"
        "    1  2  3  4  5  6\n"
        "1   А  Б  В  Г  Д  Е\n"
        "2   Ж  З  И  Й  К  Л\n"
        "3   М  Н  О  П  Р  С\n"
        "4   Т  У  Ф  Х  Ц  Ч\n"
        "5   Ш  Щ  Ъ  Ы  Ь  Э\n"
        "6   Ю  Я  .  ,  !  ?\n"
    )

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("=== Шифр Полибия ===\n")
        yield Static(self.TABLE)
        yield Label("Файл:")
        yield Horizontal(
            Input(placeholder="путь к файлу", id="file-path"),
            Button("Открыть", id="open"),
            Button("Сохранить", id="save"),
        )
        yield Label("Текст / Пары цифр:")
        yield TextArea(id="text-in")
        yield Static("", id="status")
        yield Horizontal(
            Button("Зашифровать", id="enc"),
            Button("Расшифровать", id="dec"),
            Button("← Назад", id="back"),
        )
        yield Label("Результат:")
        yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status   = self.query_one("#status", Static)
        text_in  = self.query_one("#text-in", TextArea)
        text_out = self.query_one("#text-out", TextArea)
        path     = self.query_one("#file-path", Input).value.strip()

        if event.button.id == "back":
            self.app.pop_screen(); return

        if handle_file(event.button.id, path, text_in, text_out, status, self.app.file_service):
            return

        text = text_in.text.strip()
        if not text: status.update("[!] Введите текст"); return

        svc = self.app.cipher_service
        try:
            if event.button.id == "enc":
                text_out.load_text(svc.encrypt_polybius(text))
                status.update("[OK] Зашифровано")
            elif event.button.id == "dec":
                text_out.load_text(svc.decrypt_polybius(text))
                status.update("[OK] Расшифровано")
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Частотный анализ
# ---------------------------------------------------------------------------

class FrequencyScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("=== Частотный анализ ===\n")
        yield Label("Файл:")
        yield Horizontal(
            Input(placeholder="путь к файлу", id="file-path"),
            Button("Открыть", id="open"),
            Button("Сохранить", id="save"),
        )
        yield Label("Зашифрованный текст (шифр Цезаря):")
        yield TextArea(id="text-in")
        yield Static("", id="status")
        yield Horizontal(
            Button("Анализировать", id="analyze"),
            Button("← Назад", id="back"),
        )
        yield Label("Результат:")
        yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status   = self.query_one("#status", Static)
        text_in  = self.query_one("#text-in", TextArea)
        text_out = self.query_one("#text-out", TextArea)
        path     = self.query_one("#file-path", Input).value.strip()

        if event.button.id == "back":
            self.app.pop_screen(); return

        if handle_file(event.button.id, path, text_in, text_out, status, self.app.file_service):
            return

        text = text_in.text.strip()
        if not text: status.update("[!] Введите текст"); return

        svc = self.app.cipher_service
        try:
            r = svc.frequency_analysis(text)
            lines = [f"Вероятный ключ: {r.probable_key}", "", "Топ-10 букв:"]
            top10 = sorted(r.frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
            for ch, freq in top10:
                lines.append(f"  {ch}  {'#' * int(freq * 100)}  {freq:.4f}")
            lines += ["", "Авторасшифровка:", r.decrypted_text]
            text_out.load_text("\n".join(lines))
            status.update(f"[OK] Вероятный ключ: {r.probable_key}")
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Взлом Виженера (индекс совпадений)
# ---------------------------------------------------------------------------

class KasiskiScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("=== Взлом шифра Виженера (индекс совпадений) ===\n")
        yield Label("Файл:")
        yield Horizontal(
            Input(placeholder="путь к файлу", id="file-path"),
            Button("Открыть", id="open"),
            Button("Сохранить", id="save"),
        )
        yield Label("Зашифрованный текст (шифр Виженера):")
        yield TextArea(id="text-in")
        yield Static("", id="status")
        yield Horizontal(
            Button("Взломать", id="break"),
            Button("← Назад", id="back"),
        )
        yield Label("Результат:")
        yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status   = self.query_one("#status", Static)
        text_in  = self.query_one("#text-in", TextArea)
        text_out = self.query_one("#text-out", TextArea)
        path     = self.query_one("#file-path", Input).value.strip()

        if event.button.id == "back":
            self.app.pop_screen(); return

        if handle_file(event.button.id, path, text_in, text_out, status, self.app.file_service):
            return

        text = text_in.text.strip()
        if not text:
            status.update("[!] Введите текст")
            return

        svc = self.app.cipher_service
        try:
            r = svc.break_vigenere(text)

            lines = [
                f"Вероятная длина ключа: {r.probable_key_length}",
                f"Вероятный ключ: {r.probable_key}",
                "",
                "Оценка длины ключа (длина -> средний IC):",
            ]
            for length, ic in list(r.key_length_estimates.items())[:5]:
                lines.append(f"  длина {length:2d}  IC = {ic:.4f}")
            lines += ["", "Расшифровка:", r.decrypted_text]

            text_out.load_text("\n".join(lines))
            status.update(f"[OK] Ключ: {r.probable_key} (длина {r.probable_key_length})")
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Приложение
# ---------------------------------------------------------------------------

class CryptoApp(App):

    TITLE = "crypto-tui"
    BINDINGS = [("q", "quit", "Выход")]

    def __init__(self) -> None:
        super().__init__()
        self.cipher_service = CipherService()
        self.file_service = FileService()

    def on_mount(self) -> None:
        self.push_screen(MainScreen())
