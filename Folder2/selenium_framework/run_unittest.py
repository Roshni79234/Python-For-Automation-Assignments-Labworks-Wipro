"""Run unittest tests and produce an HTML report in reports/."""
import unittest

import HtmlTestRunner

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests", pattern="test_*_unittest.py")
    HtmlTestRunner.HTMLTestRunner(
        output="reports", report_name="unittest_report", combine_reports=True,
        report_title="Unittest Automation Report",
    ).run(suite)
