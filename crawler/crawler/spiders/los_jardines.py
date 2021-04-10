import scrapy

from ..items import ProductItem

from urllib.parse import urljoin


class CasaRicaSpider(scrapy.Spider):
    name = 'los_jardines'
    allowed_domains = ['losjardinesonline.com.py']
    start_urls = ['https://www.losjardinesonline.com.py/catalogo?q=']

    custom_settings = {
        'SHOP_NAME': 'Los Jardines',
        'SHOP_URL': 'https://losjardinesonline.com.py',
    }

    base_url = 'losjardinesonline.com.py'

    def parse(self, response):
        products = response.css('.product')
        for product in products:
            item = ProductItem()

            name = product.css('.ecommercepro-loop-product__title::text').get()
            if name:
                name = name.replace('\n', '')
                name = name.strip()
                item['name'] = name

            url = product.css('.ecommercepro-LoopProduct-link::attr(href)').get()
            item['url'] = self.join_to_base_url(url)

            # The first one is always the current price, it can be a sales prices on the right
            price = product.css('.price .amount::text').get()
            price = price.replace('₲', '')
            price = price.replace('.', '')
            price = price.strip()
            item['price'] = int(price)

            item['image_url'] = product.css('.product-list-image img::attr(data-src)').get()

            yield item

        next_page = response.css('.next.page-numbers::attr(href)').get()
        if next_page is not None:
            self.logger.info("Going to next page --> {}".format(next_page))
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info('Next page not found, reached last page of search')

    def join_to_base_url(self, to_join):
        return urljoin('https://losjardinesonline.com.py/', to_join)
