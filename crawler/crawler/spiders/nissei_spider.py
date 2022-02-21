import scrapy

from ..items import ProductItem
from urllib.parse import urljoin
import re


class NisseiSpider(scrapy.Spider):
    name = 'nissei_spider'
    allowed_domains = ['nissei.com']
    start_urls = ['https://nissei.com/py/catalogsearch/result/index/?q=%25']

    custom_settings = {
        'SHOP_NAME': 'Nissei',
        'SHOP_URL': 'https://www.casanissei.com/py/',
    }

    def parse(self, response):
        products = response.css('.item.product.product-item')
        if products:
            for product in products:
                item = ProductItem()

                name = product.css('.product-item-link::text').get()
                if name:
                    name = name.replace('\n', '')
                    name = name.strip()
                    item['name'] = name

                url = product.css('.product-item-link::attr(href)').get()
                url = self.join_to_base_url(url)
                item['url'] = url

                # TODO get brand from product page

                price = product.css('.price::text').get()
                if price:
                    price = price.replace('Gs', '')
                    price = price.replace('.', '')
                    item['price'] = int(price.strip())
                else:
                    # Out of stock products usually dont have price
                    self.logger.warning(
                        'Found product without price, ignore and continue with next item. product url={}'.format(url))
                    continue

                image_url = product.css('.product-image-photo::attr(data-src)').get()
                if image_url:
                    # The image url sometimes is the cache one, remove cache information to have the real url
                    if 'cache' in image_url:
                        regex = re.compile(r'cache\/.*?\/')
                        image_url = regex.sub('', image_url)

                    item['image_url'] = self.join_to_base_url(image_url)

                yield item

            next_page = response.css('.pages-item-next a::attr(href)').get()
            if next_page is not None:
                self.logger.info("Going to next page --> {}".format(next_page))
                yield response.follow(next_page, callback=self.parse)
            else:
                self.logger.info('Next page not found, reached last page of search')
        else:
            self.logger.info('No Products found, reached last page of search')

    def join_to_base_url(self, to_join):
        return urljoin('https://www.casanissei.com/', to_join)
