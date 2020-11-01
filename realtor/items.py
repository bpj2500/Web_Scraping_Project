# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealtorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    have_beds = scrapy.Field() 
    beds = scrapy.Field() 
    baths = scrapy.Field() 
    sqft = scrapy.Field() 
    property_type = scrapy.Field() 
    area = scrapy.Field()
    year_built = scrapy.Field()
