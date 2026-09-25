from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class LoginPage(BasePage):
    MY_ACCOUNT_MENU = (By.XPATH, "//a[@title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input[value='Login']")
    FORGOT_LINK = (By.LINK_TEXT, "Forgotten Password")
    RETURNING_HEADING = (By.XPATH, "//h2[normalize-space()='Returning Customer']")
    NEW_CUSTOMER_HEADING = (By.XPATH, "//h2[normalize-space()='New Customer']")
    ACCOUNT_HEADING = (By.XPATH, "//h2[normalize-space()='My Account']")
    LOGOUT_HEADING = (By.XPATH, "//h1[normalize-space()='Account Logout']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")

    def open_login_page(self):
        self.open(ConfigReader.get("app", "base_url"))
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGIN_LINK)
        return self

    def login(self, email, password):
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return self

    def wait_for_login_result(self, timeout=20):
        """Wait ONCE for whichever comes first: My Account page or an error alert."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.ACCOUNT_HEADING),
                    EC.visibility_of_element_located(self.ERROR_ALERT),
                )
            )
        except TimeoutException:
            pass

    def is_login_successful(self):
        self.wait_for_login_result()
        return any(e.is_displayed() for e in self.find_all(self.ACCOUNT_HEADING))

    def get_error_message(self):
        self.wait_for_login_result()
        alerts = self.find_all(self.ERROR_ALERT)
        return alerts[0].text if alerts else ""

    def is_login_form_displayed(self):
        return self.is_visible(self.RETURNING_HEADING) and self.is_visible(self.NEW_CUSTOMER_HEADING)

    def is_password_masked(self):
        return self.attribute_of(self.PASSWORD, "type") == "password"

    def click_forgot_password(self):
        self.click(self.FORGOT_LINK)
        return self

    def logout(self):
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGOUT_LINK)
        return self

    def is_logged_out(self):
        return self.is_visible(self.LOGOUT_HEADING)