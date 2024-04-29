# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import psycopg2


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


class DatePipeline:
    def process_item(self, item, spider):
        # Input timestamp string
        timestamp_str = item['publication_date']

        # Parse the timestamp string into a datetime object
        timestamp = datetime.fromisoformat(timestamp_str)

        # Extract the date portion
        date_only = timestamp.date()

        # Convert the date portion back to string format
        date_str = date_only.isoformat()

        item['publication_date'] = date_str

        return item


class SavingToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="apartments",
            user="postgres",
            password="is-91060502",
            port="5432")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            # Start a transaction
            self.cur.execute("BEGIN")

            # Execute your SQL command(s)
            self.cur.execute("""
                INSERT INTO kyiv_apartments 
                (flat_id, area_total, built_year, currency, district, micro_district, street, house_number, 
                 publication_date, description, city, price, room_count, floor)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                             (item['flat_id'], item['area_total'], item['built_year'], item['currency'],
                              item['district'], item['micro_district'], item['street'], item['house_number'],
                              item['publication_date'], item['description'], item['city'], item['price'],
                              item['room_count'], item['floor']))

            # Commit the transaction
            self.cur.execute("COMMIT")
        except Exception as e:
            # Rollback the transaction
            self.cur.execute("ROLLBACK")
            # Log or handle the exception
            print(f"Error: {e}")

        return item
