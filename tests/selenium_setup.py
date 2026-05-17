import threading
import unittest
import tempfile
from pathlib import Path

from werkzeug.serving import make_server

from app import create_app
from app.config import TestingConfig
from app.extensions import db
import os

try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
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
    app_ctx = None
    _db_file = None

    class SeleniumTestingConfig(TestingConfig):
        pass

    @classmethod
    def setUpClass(cls):
        db_file = tempfile.NamedTemporaryFile(prefix="selenium-test-", suffix=".sqlite", delete=False)
        db_file.close()
        cls._db_file = Path(db_file.name)
        cls.SeleniumTestingConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{cls._db_file.as_posix()}"

        cls.app = create_app(cls.SeleniumTestingConfig)
        cls.app_ctx = cls.app.app_context()
        cls.app_ctx.push()
        db.create_all()

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
        # Allow running with visible browser when SHOW_BROWSER env var is set
        if not os.environ.get("SHOW_BROWSER"):
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1440,1200")

        try:
                # Use webdriver-manager to fetch a matching chromedriver in CI
                service = Service(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
        except WebDriverException as exc:
            raise unittest.SkipTest(f"Chrome WebDriver is not available: {exc}") from exc

    @classmethod
    def tearDownClass(cls):
        if cls.driver is not None:
            cls.driver.quit()
            cls.driver = None

        if cls.app_ctx is not None:
            db.session.remove()
            db.drop_all()
            cls.app_ctx.pop()
            cls.app_ctx = None

        if cls.server is not None:
            cls.server.shutdown()
            cls.server.server_close()
            cls.server = None

        if cls._db_file is not None and cls._db_file.exists():
            try:
                cls._db_file.unlink()
            except PermissionError:
                # On Windows the DB file may still be held by a subprocess; ignore cleanup error
                pass
            cls._db_file = None

        cls.server_thread = None

    def open_path(self, path="/"):
        self.driver.get(f"{self.base_url}{path}")
