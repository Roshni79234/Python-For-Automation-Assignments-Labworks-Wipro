import unittest

from pages.product_page import ProductPage
from pages.search_page import SearchPage
from tests.base_test import BaseTest
from utils.csv_reader import CsvReader


class SearchUnittest(BaseTest):
    def _check_search(self, row):
        page = SearchPage(self.driver).open_home().search(row["keyword"])
        if row["expected"] == "found":
            self.assertTrue(page.has_results(), f"No results for {row['keyword']}")
            self.assertTrue(any(row["keyword"].lower() in n.lower() for n in page.get_product_names()))
        else:
            self.assertTrue(page.is_no_result_message_displayed())

    def test_search_results_page_title(self):
        page = SearchPage(self.driver).open_home().search("iPhone")
        self.assertEqual(page.title, "Search - iPhone")

    def test_search_using_enter_key(self):
        page = SearchPage(self.driver).open_home().search_with_enter("MacBook")
        self.assertTrue(page.has_results())

    def test_open_product_from_search_results(self):
        search = SearchPage(self.driver).open_home().search("MacBook")
        clicked = search.open_first_result()
        self.assertEqual(ProductPage(self.driver).get_product_name(), clicked)


def _make_test(row):
    def test(self):
        self._check_search(row)
    return test


for _row in CsvReader.read("search_data.csv"):
    setattr(SearchUnittest, f"test_search_{_row['test_id']}", _make_test(_row))


if __name__ == "__main__":
    unittest.main()
