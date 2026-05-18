from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = PROJECT_ROOT / "reports" / "screenshots"


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="URL base del sitio SauceDemo.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Ejecuta Chrome sin abrir ventana visible.",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    """Crea y cierra una instancia independiente de Chrome por cada test."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1366,768")

    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless=new")

    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.implicitly_wait(0)

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura automatica cuando falla un test con Selenium."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver_instance = item.funcargs.get("driver")
    if driver_instance is None:
        return

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOTS_DIR / f"{item.name}_{timestamp}.png"
    driver_instance.save_screenshot(str(screenshot_path))
