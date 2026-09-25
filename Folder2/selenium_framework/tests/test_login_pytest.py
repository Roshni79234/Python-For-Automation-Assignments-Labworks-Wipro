import time

import pytest

from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.csv_reader import CsvReader

LOGIN_ROWS = CsvReader.read("login_data.csv")


@pytest.mark.regression
@pytest.mark.parametrize("row", LOGIN_ROWS, ids=[r["test_id"] for r in LOGIN_ROWS])
def test_login_data_driven(driver, row):
    page = LoginPage(driver).open_login_page()
    page.login(row["email"], row["password"])
    if row["expected"] == "success":
        assert page.is_login_successful(), "Expected to land on My Account page"
    else:
        assert not page.is_login_successful()
        assert page.get_error_message().strip() != "", "Expected a warning message"


@pytest.mark.smoke
def test_login_page_loads(driver):
    page = LoginPage(driver).open_login_page()
    assert page.title == "Account Login"
    assert page.is_login_form_displayed()
    assert "account/login" in page.current_url


@pytest.mark.regression
def test_password_field_is_masked(driver):
    page = LoginPage(driver).open_login_page()
    assert page.is_password_masked()


@pytest.mark.regression
def test_forgot_password_link_navigates(driver):
    page = LoginPage(driver).open_login_page().click_forgot_password()
    assert "account/forgotten" in page.current_url


@pytest.mark.regression
def test_invalid_login_shows_no_match_message(driver):
    # unique email each run so the site's login-attempt lockout never affects the real account
    page = LoginPage(driver).open_login_page()
    page.login(f"nobody_{int(time.time())}@example.com", "SomePass123")
    assert "No match for E-Mail Address" in page.get_error_message()


@pytest.mark.smoke
def test_logout_after_login(driver):
    page = LoginPage(driver).open_login_page()
    page.login(ConfigReader.valid_email(), ConfigReader.valid_password())
    assert page.is_login_successful()
    page.logout()
    assert page.is_logged_out()
