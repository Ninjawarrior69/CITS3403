from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from selenium.common.exceptions import TimeoutException

from tests.selenium_fixtures import SeleniumFixturesMixin
from tests.selenium_setup import SeleniumTestCase


class LoginSeleniumTests(SeleniumFixturesMixin, SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.create_user(
            name="Login User",
            username="loginuser",
            email="loginuser@example.com",
            password="password123",
        )

    def test_login_success_redirects_to_profile(self):
        self.open_path("/login")

        form = self.driver.find_element(By.CSS_SELECTOR, "form[action='/login']")
        form.find_element(By.ID, "login-identifier").send_keys("loginuser")
        form.find_element(By.ID, "login-password").send_keys("password123")
        # submit via the form's submit control (input or button)
        submit = form.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        submit[0].click()

        try:
            WebDriverWait(self.driver, 5).until(lambda d: "/profile" in d.current_url)
        except TimeoutException:
            tmp = Path("tmp")
            tmp.mkdir(exist_ok=True)
            self.driver.save_screenshot(str(tmp / "login_success_after_click.png"))
            with open(tmp / "login_success_after_click.html", "w", encoding="utf-8") as fh:
                fh.write(self.driver.page_source)
            raise

        self.assertIn("/profile", self.driver.current_url)
        # ensure profile name is visible on the page (more robust than #profile-data visibility)
        profile_name_el = self.driver.find_element(By.CSS_SELECTOR, ".profile-name")
        self.assertTrue(profile_name_el.is_displayed())
        self.assertIn("Login User", profile_name_el.text)

    def test_login_failure_shows_error_and_no_redirect(self):
        # ensure a user exists
        self.create_user(
            name="Fail User",
            username="failuser",
            email="failuser@example.com",
            password="correcthorsebatterystaple",
        )

        self.open_path("/login")

        form = self.driver.find_element(By.CSS_SELECTOR, "form[action='/login']")
        form.find_element(By.ID, "login-identifier").send_keys("failuser")
        form.find_element(By.ID, "login-password").send_keys("wrongpassword")
        submit = form.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        submit[0].click()

        # wait for error message to appear on the same page; capture evidence on timeout
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-danger"))
            )
        except TimeoutException:
            tmp = Path("tmp")
            tmp.mkdir(exist_ok=True)
            self.driver.save_screenshot(str(tmp / "login_failure_after_click.png"))
            with open(tmp / "login_failure_after_click.html", "w", encoding="utf-8") as fh:
                fh.write(self.driver.page_source)
            raise

        self.assertIn("/login", self.driver.current_url)
        errors = self.driver.find_elements(By.CSS_SELECTOR, ".text-danger")
        self.assertTrue(any("Invalid username/email or password." in e.text for e in errors))
