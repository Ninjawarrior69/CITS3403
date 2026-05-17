from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.selenium_fixtures import SeleniumFixturesMixin
from tests.selenium_setup import SeleniumTestCase


class SearchSeleniumTests(SeleniumFixturesMixin, SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a book to be found by search
        cls.book = cls.create_book(title="Unique Selenium Title", author="Test Author")

    def test_search_returns_results(self):
        # open home and perform search using the site's search form
        self.open_path("/")

        # attempt to find a site-wide search input (navbar or homepage)
        try:
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='q'], input#search")
        except Exception:
            # fallback to opening the search page directly
            self.open_path("/search?q=Unique+Selenium+Title")
        else:
            search_input.clear()
            search_input.send_keys("Unique Selenium Title")
            search_input.submit()

        # navigate directly to the search endpoint (books) to avoid JS-only submission
        self.open_path("/search?type=books&q=Unique+Selenium+Title")

        # wait for result items to render
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-result-item"))
        )

        # assert that our book title appears in one of the result titles
        titles = [el.text for el in self.driver.find_elements(By.CSS_SELECTOR, ".search-book-title")]
        assert any("Unique Selenium Title" in t for t in titles)
