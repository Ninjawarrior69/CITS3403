from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.selenium_fixtures import SeleniumFixturesMixin
from tests.selenium_setup import SeleniumTestCase


class PostReviewSeleniumTests(SeleniumFixturesMixin, SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.create_user(username="reviewuser", email="review@example.com", password="password123")
        cls.book = cls.create_book(title="Review Selenium Title", author="Review Author")

    def login_via_ui(self, username, password):
        self.open_path("/login")
        form = self.driver.find_element(By.CSS_SELECTOR, "form[action='/login']")
        form.find_element(By.ID, "login-identifier").send_keys(username)
        form.find_element(By.ID, "login-password").send_keys(password)
        submit = form.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        submit[0].click()
        WebDriverWait(self.driver, 5).until(lambda d: "/profile" in d.current_url)

    def test_post_review_is_displayed(self):
        self.login_via_ui("reviewuser", "password123")

        self.open_path(f"/book/{self.book.id}")

        # fill review textarea
        review_text = "This is an automated Selenium review."
        textarea = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "review-input"))
        )
        textarea.clear()
        textarea.send_keys(review_text)

        # set stars via hidden input and also set the JS `selectedRating` so the client-side
        # validation allows the review to be submitted
        self.driver.execute_script("document.getElementById('review-stars').value = '5';")
        self.driver.execute_script(
            "selectedRating = 5; document.getElementById('rating-stars').value = 5; updateStars(5, document.querySelectorAll('#rating span'));"
        )
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "form#review-form button[type='submit'], .post-review-btn")
        submit_btn.click()

        # wait until the review text appears in the page
        WebDriverWait(self.driver, 5).until(lambda d: review_text in d.page_source)

        # assert review appears
        body = self.driver.page_source
        assert review_text in body
