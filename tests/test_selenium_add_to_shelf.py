from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.selenium_fixtures import SeleniumFixturesMixin
from tests.selenium_setup import SeleniumTestCase


class AddToShelfSeleniumTests(SeleniumFixturesMixin, SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.create_user(username="shelfuser", email="shelf@example.com", password="password123")
        cls.book = cls.create_book(title="Shelf Selenium Title", author="Shelf Author")

    def login_via_ui(self, username, password):
        self.open_path("/login")
        form = self.driver.find_element(By.CSS_SELECTOR, "form[action='/login']")
        form.find_element(By.ID, "login-identifier").send_keys(username)
        form.find_element(By.ID, "login-password").send_keys(password)
        submit = form.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        submit[0].click()
        WebDriverWait(self.driver, 5).until(lambda d: "/profile" in d.current_url)

    def test_add_book_to_shelf_shows_status(self):
        # login first
        self.login_via_ui("shelfuser", "password123")

        # open book detail
        self.open_path(f"/book/{self.book.id}")

        # open shelf modal
        open_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "openShelfModal"))
        )
        open_btn.click()

        # click the 'To Be Read' option inside the shelf form
        option_selector = "form[action*='/shelf'] button[name='status'][value='To Be Read']"
        option_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector))
        )
        option_btn.click()

        # after redirect, the sidebar button should contain the status
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "openShelfModal"), "To Be Read")
        )

        btn = self.driver.find_element(By.ID, "openShelfModal")
        assert "To Be Read" in btn.text
