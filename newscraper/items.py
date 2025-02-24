# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field() 
    author = scrapy.Field()
    published_date = scrapy.Field()
    url = scrapy.Field()

