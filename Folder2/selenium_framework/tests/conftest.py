import pytest

from utils.driver_factory import DriverFactory
from utils.screenshot import should_capture, take_screenshot


@pytest.fixture
def driver():
    drv = DriverFactory.get_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot every pytest-style test (pass or fail) and embed it in the HTML report.
    unittest-style tests are handled by BaseTest.tearDown instead."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    drv = getattr(item, "funcargs", {}).get("driver")
    if drv is None:
        return

    status = "failed" if report.failed else "passed" if report.passed else None
    if status is None or not should_capture(status):
        return

    path = take_screenshot(drv, item.name, status)
    print(f"\n[Screenshot saved] {path}")
    try:
        from pytest_html import extras
        report.extras = list(getattr(report, "extras", [])) + [
            extras.image(drv.get_screenshot_as_base64(), mime_type="image/png")
        ]
    except Exception:
        pass
