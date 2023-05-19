import scrapy
import json
from scrapy.loader import ItemLoader
from ..items import FlatItem
from ..json_extractor import extract_field


class FlatSpiderSpider(scrapy.Spider):
    name = "flat_spider"
    pages = 99
    allowed_domains = ["flatfy.ua"]
    start_urls = ["https://flatfy.ua/api/realties?currency=UAH&geo_id=1&is_without_fee=false&lang=uk"
                  "&price_sqm_currency=UAH&section_id=2&sort=insert_time"]

    def parse(self, response):
        for page in range(1, self.pages + 1):
            next_page_url = f"{self.start_urls[0]}&page={page}"
            print("Next Page URL : ", next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_flats)

    def parse_flats(self, response):
        global l
        flats = json.loads(response.body)

        for flat in flats['data']:
            extract_field(flat, 'street')
            l = ItemLoader(item=FlatItem(), selector=flat)
            l.add_value('id', flat['id'])
            l.add_value('area_total', flat['area_total'])
            l.add_value('built_year', flat['built_year'])
            l.add_value('currency', flat['currency'])
            l.add_value('district', extract_field(flat, 'district'))
            l.add_value('micro_district', extract_field(flat, 'microdistrict'))
            l.add_value('street', extract_field(flat, 'street'))
            l.add_value('house_number', extract_field(flat, 'house'))
            l.add_value('publication_date', flat['insert_time'])
            l.add_value('description', flat['text'])
            l.add_value('city', extract_field(flat, 'city'))
            l.add_value('price', flat['price'])
            l.add_value('room_count', flat['room_count'])
            l.add_value('floor', flat['floor'])
            flat_item = l.load_item()
            yield flat_item

