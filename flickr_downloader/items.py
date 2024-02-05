# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FlickrDownloaderItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    tag = scrapy.Field()
