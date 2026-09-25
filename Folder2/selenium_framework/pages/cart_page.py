from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "#content form .table-responsive tbody tr td.text-left a")

    def open_cart(self):
        self.open(ConfigReader.get("app", "base_url") + "index.php?route=checkout/cart")
        return self

    def get_item_names(self):
        self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "#content"))
        return [e.text for e in self.find_all(self.ITEM_NAMES)]
