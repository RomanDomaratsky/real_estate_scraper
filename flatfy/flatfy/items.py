# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class FlatItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    area_total = scrapy.Field(output_processor=TakeFirst())
    built_year = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    district = scrapy.Field(output_processor=TakeFirst())
    micro_district = scrapy.Field(output_processor=TakeFirst())
    street = scrapy.Field(output_processor=TakeFirst())
    house_number = scrapy.Field(output_processor=TakeFirst())
    city = scrapy.Field(output_processor=TakeFirst())
    publication_date = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    room_count = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field(output_processor=TakeFirst())
