# Automated Testing with Selenium
To develop automated test scripts using Selenium for testing web application functionalities, execute these scripts, and generate comprehensive test reports.
## Table of contents
- Prereqisites
- Environment setup

## Prereqisites
- **Python**: Version 3.6 or higher
- **pip**: Package manager for Python

## Environment setup
- Programming Language: Install Python at https://www.python.org/downloads/
- IDE: Install PyCharm at https://www.jetbrains.com/pycharm/download/?section=windows
- Browser: Chrome
- WebDriver: Install ChromeDriver at https://developer.chrome.com/docs/chromedriver/download/
- To install Selenium and pytest, open your terminal and run:
```bash
 pip install selenium pytest
```

## Running with Pytest
- Write the test scripts, then run the script by opening the terminal and run:
```bash
pytest test_file.py
```
- With opencart_automatic_testing.py is a name of test file

-To get even more detailed output, use the -v flag:
```bash
pytest -v test_file.py
```
-For a more visual representation of the test results, you can generate HTML reports using the pytest-html plugin.
### 1. Install pytest-html
```bash
pip install pytest-html
```
### 2. Run tests with HTML report generation
```bash
pytest --html=report-test_file.html
```
- The report.html file will be saved in the same directory as the test file.
