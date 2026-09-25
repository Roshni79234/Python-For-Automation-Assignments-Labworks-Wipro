import configparser
import os

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.ini")
_parser = configparser.ConfigParser()
_parser.read(_CONFIG_PATH)


class ConfigReader:
    @staticmethod
    def get(section, key, fallback=None):
        return _parser.get(section, key, fallback=fallback)

    @staticmethod
    def get_bool(section, key, fallback=False):
        return _parser.getboolean(section, key, fallback=fallback)

    @staticmethod
    def get_int(section, key, fallback=None):
        return _parser.getint(section, key, fallback=fallback)

    @staticmethod
    def valid_email():
        return ConfigReader.get("app", "valid_email")

    @staticmethod
    def valid_password():
        return ConfigReader.get("app", "valid_password")
