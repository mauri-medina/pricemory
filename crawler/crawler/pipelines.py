# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem

from product.models import *


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


class DataBasePipeline:
    shop = None

    # This method is called once per spider when the spider is opened
    def open_spider(self, spider):
        shop_name = spider.settings['SHOP_NAME']
        if shop_name is None:
            raise ValueError("Spider must have shop name")

        shop_url = spider.settings['SHOP_URL']
        if shop_url is None:
            raise ValueError("Spider must have shop url")

        self.shop, created = Shop.objects.get_or_create(
            name=shop_name,
            url=shop_url
        )

        spider.logger.debug('spider Shop DB instance= %s, created = %s', self.shop, created)

    def process_item(self, item, spider):
        spider.logger.debug('at process_item::process_item item=%s', item)

        product_price = int(item.get('price'))
        product_url = item.get('url')
        product_name = item.get('name')

        product, created = Product.objects.get_or_create(
            # Any keyword arguments passed to get_or_create() will be used in a get() call
            name=product_name,
            url=product_url
        )
        spider.logger.debug('Product id=%d, created=%s', product.id, created)

        if created:
            brand_name = item.get('brand')
            brand = None
            if brand_name:
                brand, created = Brand.objects.get_or_create(
                    name=brand_name
                )

            product.image_url = item.get('image_url')
            product.barcode = item.get('barcode')
            product.shop = self.shop
            product.brand = brand
            product.save()

            PriceHistory.objects.create(
                product=product,
                price=product_price
            )

        else:
            latest_price_history = PriceHistory.objects.filter(product=product).latest('date_created')
            if latest_price_history.price != product_price:
                PriceHistory.objects.create(
                    product=product,
                    price=product_price
                )
            else:
                spider.logger.debug(
                    'Price for product=%d is the same as the last register price, Price history will not be created',
                    product.id)

        return item
