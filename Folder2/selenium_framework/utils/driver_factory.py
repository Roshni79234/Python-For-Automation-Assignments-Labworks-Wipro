from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.config_reader import ConfigReader


class DriverFactory:
    @staticmethod
    def get_driver():
        name = ConfigReader.get("browser", "name").lower()
        headless = ConfigReader.get_bool("browser", "headless")

        if name == "chrome":
            opts = ChromeOptions()
            opts.page_load_strategy = "eager"  # don't wait for every image/ad to load
            if headless:
                opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(options=opts)
        elif name == "firefox":
            opts = FirefoxOptions()
            if headless:
                opts.add_argument("-headless")
            driver = webdriver.Firefox(options=opts)
        elif name == "edge":
            opts = EdgeOptions()
            if headless:
                opts.add_argument("--headless=new")
            driver = webdriver.Edge(options=opts)
        else:
            raise ValueError(f"Unsupported browser: {name}")

        driver.maximize_window()
        driver.implicitly_wait(ConfigReader.get_int("browser", "implicit_wait"))
        return driver