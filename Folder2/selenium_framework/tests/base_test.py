import unittest

from utils.driver_factory import DriverFactory
from utils.screenshot import should_capture, take_screenshot


class BaseTest(unittest.TestCase):
    """Base for unittest-style tests: browser setup/teardown + screenshot for each test."""

    _test_failed = False

    def setUp(self):
        self._test_failed = False
        self.driver = DriverFactory.get_driver()

    def _callTestMethod(self, method):
        try:
            super()._callTestMethod(method)
        except unittest.SkipTest:
            raise
        except BaseException:
            self._test_failed = True
            raise

    def tearDown(self):
        status = "failed" if self._test_failed else "passed"
        try:
            if should_capture(status):
                path = take_screenshot(self.driver, self.id(), status)
                print(f"\n[Screenshot saved] {path}")
        except Exception as e:
            print(f"\n[Screenshot skipped] {type(e).__name__}")
        finally:
            try:
                self.driver.quit()
            except Exception:
                pass