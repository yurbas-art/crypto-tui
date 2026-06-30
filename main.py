import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.textual_app import CryptoApp


def main() -> None:
    app = CryptoApp()
    app.run()


if __name__ == "__main__":
    main()
