import threading
import unittest

from werkzeug.serving import make_server

from app import create_app
from app.config import TestingConfig

try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except ImportError as exc:  # pragma: no cover - handled by test environment
    webdriver = None
    WebDriverException = Exception
    ChromeOptions = None
    _SELENIUM_IMPORT_ERROR = exc
else:
    _SELENIUM_IMPORT_ERROR = None


class SeleniumTestCase(unittest.TestCase):
    base_url = None
    driver = None
    server = None
    server_thread = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestingConfig)
        cls.server = make_server("127.0.0.1", 0, cls.app)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

        try:
            cls.driver = cls._create_driver()
        except Exception:
            cls.server.shutdown()
            cls.server.server_close()
            cls.server = None
            cls.server_thread = None
            raise

    @classmethod
    def _create_driver(cls):
        if webdriver is None:
            raise unittest.SkipTest(
                f"Selenium is not available: {_SELENIUM_IMPORT_ERROR}"
            )

        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1440,1200")

        try:
            return webdriver.Chrome(options=options)
        except WebDriverException as exc:
            raise unittest.SkipTest(f"Chrome WebDriver is not available: {exc}") from exc

    @classmethod
    def tearDownClass(cls):
        if cls.driver is not None:
            cls.driver.quit()
            cls.driver = None

        if cls.server is not None:
            cls.server.shutdown()
            cls.server.server_close()
            cls.server = None

        cls.server_thread = None

    def open_path(self, path="/"):
        self.driver.get(f"{self.base_url}{path}")
