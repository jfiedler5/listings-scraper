import scrapy


class ListingItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()

