from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class SearchPage(BasePage):
    SEARCH_BOX = (By.NAME, "search")
    SEARCH_BTN = (By.CSS_SELECTOR, "#search button")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-thumb h4 a")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".product-thumb .button-group button:first-child")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    NO_RESULT_MSG = (By.XPATH, "//p[contains(text(),'no product that matches')]")

    def open_home(self):
        self.open(ConfigReader.get("app", "base_url"))
        return self

    def search(self, keyword):
        self.type(self.SEARCH_BOX, keyword)
        self.click(self.SEARCH_BTN)
        return self

    def search_with_enter(self, keyword):
        self.type(self.SEARCH_BOX, keyword)
        self.find(self.SEARCH_BOX).send_keys(Keys.ENTER)
        return self

    def get_search_placeholder(self):
        return self.attribute_of(self.SEARCH_BOX, "placeholder")

    def get_product_names(self):
        return [e.text for e in self.find_all(self.PRODUCT_TITLES)]

    def has_results(self):
        return len(self.get_product_names()) > 0

    def is_no_result_message_displayed(self):
        return self.is_visible(self.NO_RESULT_MSG)

    def open_first_result(self):
        """Click the first product; returns the product name that was clicked."""
        first = self.wait.until(lambda d: d.find_elements(*self.PRODUCT_TITLES))[0]
        name = first.text
        first.click()
        return name

    def add_first_result_to_cart(self):
        """Adds first result to cart; returns its name."""
        name = self.get_product_names()[0]
        self.click(self.ADD_TO_CART_BTN)
        return name

    def get_success_alert(self):
        return self.text_of(self.SUCCESS_ALERT) if self.is_visible(self.SUCCESS_ALERT) else ""
