import pytest

from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from utils.csv_reader import CsvReader

SEARCH_ROWS = CsvReader.read("search_data.csv")


@pytest.mark.smoke
@pytest.mark.parametrize("row", SEARCH_ROWS, ids=[r["test_id"] for r in SEARCH_ROWS])
def test_product_search_data_driven(driver, row):
    page = SearchPage(driver).open_home().search(row["keyword"])
    if row["expected"] == "found":
        assert page.has_results(), f"Expected results for '{row['keyword']}'"
        assert any(row["keyword"].lower() in n.lower() for n in page.get_product_names())
    else:
        assert page.is_no_result_message_displayed()


@pytest.mark.regression
def test_search_box_placeholder(driver):
    page = SearchPage(driver).open_home()
    assert page.get_search_placeholder() == "Search"


@pytest.mark.regression
def test_search_results_page_title(driver):
    page = SearchPage(driver).open_home().search("iPhone")
    assert page.title == "Search - iPhone"


@pytest.mark.regression
def test_search_using_enter_key(driver):
    page = SearchPage(driver).open_home().search_with_enter("MacBook")
    assert page.has_results()


@pytest.mark.regression
def test_search_again_from_results_page(driver):
    page = SearchPage(driver).open_home().search("iPhone")
    assert page.has_results()
    page.search("Canon")
    assert any("canon" in n.lower() for n in page.get_product_names())


@pytest.mark.regression
def test_open_product_from_search_results(driver):
    search = SearchPage(driver).open_home().search("MacBook")
    clicked = search.open_first_result()
    assert ProductPage(driver).get_product_name() == clicked


@pytest.mark.regression
def test_add_searched_product_to_cart(driver):
    search = SearchPage(driver).open_home().search("iPhone")
    name = search.add_first_result_to_cart()
    assert "Success" in search.get_success_alert()
    assert name in CartPage(driver).open_cart().get_item_names()
