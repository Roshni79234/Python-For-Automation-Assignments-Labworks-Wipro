from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    PRICE = (By.CSS_SELECTOR, "#content .list-unstyled h2")

    def get_product_name(self):
        return self.text_of(self.HEADING)

    def get_price(self):
        return self.text_of(self.PRICE)
