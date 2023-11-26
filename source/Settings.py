from json import dump
from json import load
from pathlib import Path

__all__ = ['Settings']


class Settings:
    file = Path(__file__).resolve().parent.parent.joinpath("./settings.json")
    default = {
        "path": "",
        "folder": "Download",
        "cookie": "",
        "proxies": None,
        "timeout": 10,
        "chunk": 1024 * 1024,
    }

    def run(self):
        return self.read() if self.file.is_file() else self.create()

    def read(self) -> dict:
        with self.file.open("r", encoding="utf-8") as f:
            return load(f)

    def create(self) -> dict:
        with self.file.open("w", encoding="utf-8") as f:
            dump(self.default, f, indent=4)
            return self.default

    def update(self, data: dict):
        with self.file.open("w", encoding="utf-8") as f:
            dump(data, f, indent=4, ensure_ascii=False)
