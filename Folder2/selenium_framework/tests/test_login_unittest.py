import unittest

from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.csv_reader import CsvReader


class LoginUnittest(BaseTest):
    def _check_login(self, row):
        page = LoginPage(self.driver).open_login_page()
        page.login(row["email"], row["password"])
        if row["expected"] == "success":
            self.assertTrue(page.is_login_successful(), "Login should succeed")
        else:
            self.assertFalse(page.is_login_successful(), "Login should fail")
            self.assertNotEqual(page.get_error_message().strip(), "", "Expected a warning message")

    def test_login_page_loads(self):
        page = LoginPage(self.driver).open_login_page()
        self.assertEqual(page.title, "Account Login")
        self.assertTrue(page.is_login_form_displayed())

    def test_password_field_is_masked(self):
        page = LoginPage(self.driver).open_login_page()
        self.assertTrue(page.is_password_masked())

    def test_forgot_password_link_navigates(self):
        page = LoginPage(self.driver).open_login_page().click_forgot_password()
        self.assertIn("account/forgotten", page.current_url)


def _make_test(row):
    def test(self):
        self._check_login(row)
    return test


# One real test per CSV row -> separate result and screenshot for each row
for _row in CsvReader.read("login_data.csv"):
    setattr(LoginUnittest, f"test_login_{_row['test_id']}", _make_test(_row))


if __name__ == "__main__":
    unittest.main()
