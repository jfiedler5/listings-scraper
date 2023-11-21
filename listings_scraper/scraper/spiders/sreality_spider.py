import scrapy
import json
import time
from ..items import ListingItem
from scrapy.exceptions import CloseSpider


class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    allowed_domains = ['sreality.cz']
    item_total = 500

    def start_requests(self):
        """
        Generates the initial request for the spider.
        """
        timestamp = int(time.time() * 1000)
        url = (f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&"
               f"per_page={self.item_total}&tms={timestamp}")
        yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        """
        Parses the API response and yields the listings.
        Closes the spider if the response format is not as expected.
        """
        # Attempt to decode JSON
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            raise CloseSpider('Invalid JSON response')

        # Check for the expected keys in the JSON data
        if not all(key in data for key in ('_embedded', 'page')):
            raise CloseSpider('Unexpected JSON structure')

        # Extract estates data
        estates = data.get('_embedded', {}).get('estates', [])
        if not estates:
            raise CloseSpider('No estates data found')

        # Process each estate item
        for index, item in enumerate(estates):
            yield self.extract_data(item, index)

    def extract_data(self, item, index):
        """
        Extracts and returns data from a single estate listing item.
        """
        item_id = f"{index + 1:04d}"
        title = item.get('name', 'No Title')
        image_urls = item.get('_links', {}).get('images', [])
        image_url = image_urls[0]['href'] if image_urls else 'No Image'
        return ListingItem(id=item_id, title=title, image_url=image_url)
