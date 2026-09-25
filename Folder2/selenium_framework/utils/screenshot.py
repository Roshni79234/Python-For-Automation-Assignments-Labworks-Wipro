import os
from datetime import datetime

from utils.config_reader import ConfigReader

SHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")


def should_capture(status):
    """status is 'passed' or 'failed'. Controlled by [screenshots] in config.ini."""
    key = "on_fail" if status == "failed" else "on_pass"
    return ConfigReader.get_bool("screenshots", key, fallback=True)


def take_screenshot(driver, test_name, status="failed"):
    folder = os.path.abspath(os.path.join(SHOT_DIR, status))
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)[-90:]
    path = os.path.join(folder, f"{safe}_{stamp}.png")
    driver.save_screenshot(path)
    return path
