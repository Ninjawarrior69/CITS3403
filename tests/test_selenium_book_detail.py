from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.selenium_fixtures import SeleniumFixturesMixin
from tests.selenium_setup import SeleniumTestCase


class BookDetailSeleniumTests(SeleniumFixturesMixin, SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a book without a cover so the placeholder is shown
        cls.book = cls.create_book(title="Detail Selenium Title", author="Detail Author", cover_url=None)

    def test_view_book_detail_shows_title_author_and_cover(self):
        self.open_path(f"/book/{self.book.id}")

        # wait for book title to be present
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )

        title = self.driver.find_element(By.CSS_SELECTOR, "h1").text
        author_text = self.driver.find_element(By.CSS_SELECTOR, ".book-info p").text

        assert "Detail Selenium Title" in title
        assert "Detail Author" in author_text

        # ensure either an image or placeholder exists
        covers = self.driver.find_elements(By.CSS_SELECTOR, ".book-cover, .book-cover-placeholder")
        assert len(covers) > 0
