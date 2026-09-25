import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.config_reader import ConfigReader


@pytest.mark.e2e
def test_login_search_add_to_cart_logout(driver):
    login = LoginPage(driver).open_login_page()
    login.login(ConfigReader.valid_email(), ConfigReader.valid_password())
    assert login.is_login_successful()

    search = SearchPage(driver).open_home().search("MacBook")
    assert search.has_results()
    name = search.add_first_result_to_cart()
    assert "Success" in search.get_success_alert()
    assert name in CartPage(driver).open_cart().get_item_names()

    login.logout()
    assert login.is_logged_out()
