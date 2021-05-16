import scrapy

from ..items import ProductItem
import re


class SalemmaSpider(scrapy.Spider):
    name = 'salemma_spider'
    allowed_domains = ['salemmaonline.com.py']
    start_urls = ['https://salemmaonline.com.py/buscar?q=%']

    custom_settings = {
        'SHOP_NAME': 'Salemma',
        'SHOP_URL': 'https://salemmaonline.com.py/',
    }

    last_visited_page = 1

    def parse(self, response):
        products = response.css('.divproduct')
        if products:
            for product in products:
                item = ProductItem()

                name = product.css('.apsubtitle::text').get()
                if name:
                    item['name'] = name.strip()

                # TODO couldn't find product barcode

                price = product.css('.pprice::text').get()
                if price:
                    price = price.strip()

                    # Remove all characters except numbers
                    # using regex because there are many variations of price text
                    regex = re.compile(r'\D')
                    price = regex.sub('', price)
                    item['price'] = int(price)

                brand = product.css('.ptitle::text').get()
                if brand:
                    item['brand'] = brand.strip()

                item['image_url'] = product.css('.imgprodts img::attr(src)').get()
                item['url'] = product.css('.apsubtitle::attr(href)').get()

                yield item

            next_page_url = self.get_next_page_url()
            self.logger.info("Going to next page --> {}".format(next_page_url))
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info('No Products found, reached last page of search')

    def get_next_page_url(self) -> str:
        self.last_visited_page += 1
        return self.start_urls[0] + '&page=' + str(self.last_visited_page)
