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
            url=shop_url,
            defaults={
                'name': shop_name
            }
        )

        spider.logger.debug('spider Shop DB instance= %s, created = %s', self.shop, created)

    def process_item(self, item, spider):
        spider.logger.debug('at process_item::process_item item=%s', item)

        scrapped_product = Product(
            url=item.get('url'),
            name=item.get('name'),
            barcode=item.get('barcode'),
            image_url=item.get('image_url'),
        )

        db_product, is_new_product = Product.objects.get_or_create(
            # search product by url, url will always be unique and not null for a product
            url=scrapped_product.url,

            # values to insert
            defaults={
                'name': scrapped_product.name,
                'barcode': scrapped_product.barcode,
                'shop': self.shop,
                'image_url': scrapped_product.image_url
            }
        )

        spider.logger.debug('Product id=%d, is_new_product=%s', db_product.id, is_new_product)

        # -- Update Product
        if not is_new_product:
            changed = False
            if db_product.name != scrapped_product.name:
                db_product.name = scrapped_product.name
                changed = True

            if db_product.image_url != scrapped_product.image_url:
                db_product.image_url = scrapped_product.image_url
                changed = True

            # Barcode of a product cannot change but it may have been saved as null before
            if db_product.barcode != scrapped_product.barcode:
                db_product.barcode = scrapped_product.barcode
                changed = True

            if db_product.description != scrapped_product.description:
                db_product.description = scrapped_product.description
                changed = True

            if changed:
                db_product.save()

        # -- Create/Update Product Brand
        brand_name = item.get('brand')
        if brand_name and (is_new_product or db_product.brand.name is None):
            brand, brand_created = Brand.objects.get_or_create(name=brand_name)
            db_product.brand = brand
            db_product.save()

        # -- Create/Update Price
        product_price = int(item.get('price'))
        price_history = PriceHistory.objects.filter(product=db_product)
        if price_history.exists():
            latest_price_history = price_history.latest('date_created')
            if latest_price_history.price != product_price:
                PriceHistory.objects.create(
                    product=db_product,
                    price=product_price
                )
            else:
                spider.logger.debug(
                    'Price for product=%d is the same as the last register price, Price history will not be created',
                    db_product.id)
        else:
            PriceHistory.objects.create(
                product=db_product,
                price=product_price
            )

        return item
