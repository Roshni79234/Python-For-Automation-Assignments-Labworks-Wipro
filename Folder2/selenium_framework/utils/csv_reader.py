import csv
import os

from utils.config_reader import ConfigReader

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "testdata")

# Placeholders usable inside CSV files, replaced with values from config.ini
# so credentials live in ONE place only.
_TOKENS = {
    "{valid_email}": ConfigReader.valid_email,
    "{valid_password}": ConfigReader.valid_password,
}


def _resolve(value):
    for token, getter in _TOKENS.items():
        if token in value:
            value = value.replace(token, getter() or "")
    return value


class CsvReader:
    @staticmethod
    def read(filename):
        """Return CSV rows as a list of dicts (header row = keys)."""
        path = os.path.join(DATA_DIR, filename)
        with open(path, newline="", encoding="utf-8") as f:
            return [{k: _resolve(v or "") for k, v in row.items()} for row in csv.DictReader(f)]
