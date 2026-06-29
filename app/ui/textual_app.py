"""
TUI-приложение на базе Textual.
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input, TextArea, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center

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
        width: 40;
        height: auto;
        padding: 2 4;
        border: round white;
    }
    #title {
        text-align: center;
        margin-bottom: 1;
    }
    #subtitle {
        text-align: center;
        margin-bottom: 2;
        color: gray;
    }
    Button {
        width: 100%;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu"):
            yield Static("crypto-tui", id="title")
            yield Static("классические шифры", id="subtitle")
            yield Button("Шифр Цезаря",      id="caesar")
            yield Button("Шифр Виженера",    id="vigenere")
            yield Button("Шифр Полибия",     id="polybius")
            yield Button("Частотный анализ", id="frequency")
            yield Button("Выход",            id="exit", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        routes = {
            "caesar":    CaesarScreen,
            "vigenere":  VigenereScreen,
            "polybius":  PolybiusScreen,
            "frequency": FrequencyScreen,
        }
        if event.button.id == "exit":
            self.app.exit()
        elif event.button.id in routes:
            self.app.push_screen(routes[event.button.id]())


# ---------------------------------------------------------------------------
# Шифр Цезаря
# ---------------------------------------------------------------------------

class CaesarScreen(Screen):

    CSS = """
    CaesarScreen {
        align: center middle;
    }
    #box {
        width: 70;
        height: auto;
        padding: 1 3;
        border: round white;
    }
    #title { text-align: center; margin-bottom: 1; }
    TextArea { height: 6; margin-bottom: 1; }
    Input    { margin-bottom: 1; }
    #status  { margin-bottom: 1; color: gray; }
    #btn-row { height: auto; }
    #btn-row Button { width: 1fr; margin-right: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="box"):
            yield Static("--- Шифр Цезаря ---", id="title")
            yield Label("Текст:")
            yield TextArea(id="text-in")
            yield Label("Ключ (число):")
            yield Input(placeholder="например: 3", id="key")
            yield Static("", id="status")
            with Horizontal(id="btn-row"):
                yield Button("Зашифровать", id="enc", variant="primary")
                yield Button("Расшифровать", id="dec", variant="success")
                yield Button("← Назад", id="back")
            yield Label("Результат:")
            yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return

        text = self.query_one("#text-in", TextArea).text.strip()
        key_raw = self.query_one("#key", Input).value.strip()
        status = self.query_one("#status", Static)

        if not text:
            status.update("[!] Введите текст")
            return
        if not key_raw:
            status.update("[!] Введите ключ")
            return
        try:
            key = int(key_raw)
        except ValueError:
            status.update("[!] Ключ должен быть целым числом")
            return

        svc: CipherService = self.app.cipher_service
        try:
            if event.button.id == "enc":
                result = svc.encrypt_caesar(text, key)
                status.update(f"[OK] Зашифровано, ключ = {key}")
            else:
                result = svc.decrypt_caesar(text, key)
                status.update(f"[OK] Расшифровано, ключ = {key}")
            self.query_one("#text-out", TextArea).load_text(result)
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Шифр Виженера
# ---------------------------------------------------------------------------

class VigenereScreen(Screen):

    CSS = """
    VigenereScreen {
        align: center middle;
    }
    #box {
        width: 70;
        height: auto;
        padding: 1 3;
        border: round white;
    }
    #title { text-align: center; margin-bottom: 1; }
    TextArea { height: 6; margin-bottom: 1; }
    Input    { margin-bottom: 1; }
    #status  { margin-bottom: 1; color: gray; }
    #btn-row Button { width: 1fr; margin-right: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="box"):
            yield Static("--- Шифр Виженера ---", id="title")
            yield Label("Текст:")
            yield TextArea(id="text-in")
            yield Label("Ключевое слово:")
            yield Input(placeholder="например: КЛЮЧ", id="key")
            yield Static("", id="status")
            with Horizontal(id="btn-row"):
                yield Button("Зашифровать", id="enc", variant="primary")
                yield Button("Расшифровать", id="dec", variant="success")
                yield Button("← Назад", id="back")
            yield Label("Результат:")
            yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return

        text = self.query_one("#text-in", TextArea).text.strip()
        key = self.query_one("#key", Input).value.strip()
        status = self.query_one("#status", Static)

        if not text:
            status.update("[!] Введите текст")
            return
        if not key:
            status.update("[!] Введите ключевое слово")
            return

        svc: CipherService = self.app.cipher_service
        try:
            if event.button.id == "enc":
                result = svc.encrypt_vigenere(text, key)
                status.update(f"[OK] Зашифровано, ключ = {key.upper()}")
            else:
                result = svc.decrypt_vigenere(text, key)
                status.update(f"[OK] Расшифровано, ключ = {key.upper()}")
            self.query_one("#text-out", TextArea).load_text(result)
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Шифр Полибия
# ---------------------------------------------------------------------------

class PolybiusScreen(Screen):

    TABLE = (
        "Таблица Полибия:\n"
        "    1  2  3  4  5  6\n"
        "1   А  Б  В  Г  Д  Е\n"
        "2   Ж  З  И  Й  К  Л\n"
        "3   М  Н  О  П  Р  С\n"
        "4   Т  У  Ф  Х  Ц  Ч\n"
        "5   Ш  Щ  Ъ  Ы  Ь  Э\n"
        "6   Ю  Я  .  ,  !  ?"
    )

    CSS = """
    PolybiusScreen {
        align: center middle;
    }
    #box {
        width: 70;
        height: 100%;
        padding: 1 3;
        border: round white;
        overflow-y: auto;
    }
    #title  { text-align: center; margin-bottom: 1; }
    #table  { margin-bottom: 1; color: gray; }
    TextArea { height: 4; margin-bottom: 1; }
    #status  { margin-bottom: 1; color: gray; }
    #btn-row Button { width: 1fr; margin-right: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="box"):
            yield Static("--- Шифр Полибия ---", id="title")
            yield Static(self.TABLE, id="table")
            yield Label("Текст / Пары цифр:")
            yield TextArea(id="text-in")
            yield Static("", id="status")
            with Horizontal(id="btn-row"):
                yield Button("Зашифровать", id="enc", variant="primary")
                yield Button("Расшифровать", id="dec", variant="success")
                yield Button("← Назад", id="back")
            yield Label("Результат:")
            yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return

        text = self.query_one("#text-in", TextArea).text.strip()
        status = self.query_one("#status", Static)

        if not text:
            status.update("[!] Введите текст")
            return

        svc: CipherService = self.app.cipher_service
        try:
            if event.button.id == "enc":
                result = svc.encrypt_polybius(text)
                status.update("[OK] Зашифровано")
            else:
                result = svc.decrypt_polybius(text)
                status.update("[OK] Расшифровано")
            self.query_one("#text-out", TextArea).load_text(result)
        except Exception as e:
            status.update(f"[!] {e}")


# ---------------------------------------------------------------------------
# Частотный анализ
# ---------------------------------------------------------------------------

class FrequencyScreen(Screen):

    CSS = """
    FrequencyScreen {
        align: center middle;
    }
    #box {
        width: 70;
        height: auto;
        padding: 1 3;
        border: round white;
    }
    #title   { text-align: center; margin-bottom: 1; }
    TextArea { height: 6; margin-bottom: 1; }
    #status  { margin-bottom: 1; color: gray; }
    #btn-row Button { width: 1fr; margin-right: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="box"):
            yield Static("--- Частотный анализ ---", id="title")
            yield Label("Зашифрованный текст (шифр Цезаря):")
            yield TextArea(id="text-in")
            yield Static("", id="status")
            with Horizontal(id="btn-row"):
                yield Button("Анализировать", id="analyze", variant="primary")
                yield Button("← Назад", id="back")
            yield Label("Результат:")
            yield TextArea(id="text-out", read_only=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return

        text = self.query_one("#text-in", TextArea).text.strip()
        status = self.query_one("#status", Static)

        if not text:
            status.update("[!] Введите текст")
            return

        svc: CipherService = self.app.cipher_service
        try:
            r = svc.frequency_analysis(text)

            lines = [
                f"Вероятный ключ: {r.probable_key}",
                "",
                "Топ-10 частых букв:",
            ]
            top10 = sorted(r.frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
            for ch, freq in top10:
                bar = "#" * int(freq * 100)
                lines.append(f"  {ch}  {bar}  {freq:.4f}")
            lines += ["", "Авторасшифровка:", r.decrypted_text]

            self.query_one("#text-out", TextArea).load_text("\n".join(lines))
            status.update(f"[OK] Вероятный ключ: {r.probable_key}")
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
