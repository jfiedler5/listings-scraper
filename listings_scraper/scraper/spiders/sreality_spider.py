from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import ListingItem
import scrapy

class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    allowed_domains = ['sreality.cz']
    item_count = 0
    max_items = 50  # Adjustable number of items

    def start_requests(self):
        url = "https://www.sreality.cz/hledani/prodej/byty?strana=1"
        yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        driver = None
        try:
            driver = self.init_webdriver(response)
            listings = self.get_listings(driver)
            for listing in listings:
                if self.item_count >= self.max_items:
                    break
                yield self.extract_data(listing)
                self.item_count += 1
        finally:
            if driver:
                driver.quit()

        if self.item_count < self.max_items:
            yield from self.paginate(response)

    def init_webdriver(self, response):
        """Initialize and return a Selenium WebDriver for the given response."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(response.url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#page-layout .property.ng-scope"))
        )
        return driver

    def get_listings(self, driver):
        """Return listings from the page using the given WebDriver."""
        return scrapy.Selector(text=driver.page_source).css("#page-layout .property.ng-scope")

    def extract_data(self, listing):
        """Extract and yield data from a single listing."""
        item_id = f"{self.item_count + 1:04d}"
        title = listing.css('.text-wrap h2 a.title span.name::text').get()
        image_url = listing.css('div._15Md1MuBeW62jbm5iL0XqR a:first-child img::attr(src)').get()
        return ListingItem(id=item_id, title=title, image_url=image_url)

    def paginate(self, response):
        """Generate the next page request if the item count hasn't reached the maximum."""
        current_page = response.meta.get('page', 1)
        next_page = current_page + 1
        next_page_url = f"https://www.sreality.cz/hledani/prodej/byty?strana={next_page}"
        return [scrapy.Request(url=next_page_url, callback=self.parse_page, meta={'page': next_page})]
