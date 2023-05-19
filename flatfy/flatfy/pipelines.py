# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FlatfyPipeline:
    def process_item(self, item, spider):
        return item


class CurrencyConversionPipeline:
    def process_item(self, item, spider):
        currency = item['currency']
        price = item['price']

        if currency == 'USD':
            # Set the constant exchange rate
            nbu_exchange_rate = 36.5686  # Replace with your actual exchange rate

            # Perform the conversion
            price_in_hryvnia = int(price * nbu_exchange_rate)

            # Update the item with the converted price
            item['price'] = price_in_hryvnia
            item['currency'] = 'UAH'

        return item
