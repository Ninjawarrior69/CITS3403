from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        self.driver.find_element(By.ID, "login-identifier").send_keys("loginuser")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        self.assertIn("/profile", self.driver.current_url)
        self.assertTrue(self.driver.find_element(By.ID, "profile-data").is_displayed())

    def test_login_failure_shows_error_and_no_redirect(self):
        # ensure a user exists
        self.create_user(
            name="Fail User",
            username="failuser",
            email="failuser@example.com",
            password="correcthorsebatterystaple",
        )

        self.open_path("/login")

        self.driver.find_element(By.ID, "login-identifier").send_keys("failuser")
        self.driver.find_element(By.ID, "login-password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # wait for error message to appear on the same page
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".text-danger"))
        )

        self.assertIn("/login", self.driver.current_url)
        errors = self.driver.find_elements(By.CSS_SELECTOR, ".text-danger")
        self.assertTrue(any("Invalid username/email or password." in e.text for e in errors))
