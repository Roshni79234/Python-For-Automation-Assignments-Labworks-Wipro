# Selenium Python Framework (Unittest + PyTest + POM)

## Structure
```
config/config.ini      browser, URL, credentials, waits
pages/                 Page Object classes (BasePage, LoginPage, SearchPage)
utils/                 ConfigReader, CsvReader, DriverFactory, screenshot helper
testdata/              login_data.csv, search_data.csv
tests/                 unittest tests (base_test.py) + pytest tests (conftest.py)
reports/  screenshots/ generated output
```

## Setup
```
pip install -r requirements.txt
```
1. Register an account on https://tutorialsninja.com/demo/
2. Put its email/password in `config/config.ini` and in the `success` row of `testdata/login_data.csv`.

## Run
```
pytest                                   # PyTest -> reports/report.html
pytest -m smoke                          # only smoke tests
python run_unittest.py                   # Unittest -> reports/unittest_report.html
python -m unittest discover -s tests -p "test_*_unittest.py"
```
Change browser/headless in `config/config.ini`. Screenshots of failures go to `screenshots/`
(and are embedded in the pytest HTML report).

## Framework concepts
- **POM**: locators + actions live in pages/, tests only hold assertions.
- **Utility classes**: config, CSV, driver, screenshot.
- **Data-driven**: CSV feeds `subTest` (unittest) and `parametrize` (pytest).
- **Failure handling**: `tearDown` (unittest) and `pytest_runtest_makereport` (pytest).
