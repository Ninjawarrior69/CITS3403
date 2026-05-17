from selenium.webdriver.common.by import By

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
