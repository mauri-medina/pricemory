import re

import scrapy

from ..items import ProductItem


class TupiSpider(scrapy.Spider):
    name = 'tupi_spider'
    allowed_domains = ['tupi.com.py']
    start_urls = ['https://www.tupi.com.py/']

    custom_settings = {
        'SHOP_NAME': 'Tupi',
        'SHOP_URL': 'https://www.tupi.com.py/',
    }

    category_url = 'https://www.tupi.com.py/rubros_paginacion'

    def parse(self, response):
        # There are different sections with different categories links so just grab them all and filter
        all_page_links = response.css('a::attr(href)').getall()
        unique_links = list(set(all_page_links))
        categories = []
        for link in unique_links:
            if '/rubros/' in link:
                categories.append(link)

        for category in categories:
            category_url = self.get_category_next_page_url(category)
            self.logger.info("Going to category page --> {}".format(category_url))

            yield scrapy.Request(url=category_url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        products = response.css('.product-inner')
        if products:
            for product in products:
                item = ProductItem()

                name = product.css('.nombre_producto_ug a::text').get()
                if name:
                    item['name'] = name.strip()

                # TODO get brand from product page

                # This is the web price
                price_content = product.css('.amount::text').getall()
                if price_content:
                    price = ''.join(price_content)
                    price = price.replace('Gs', '')
                    price = price.replace('.', '')
                    price = price.strip()
                    item['price'] = price

                item['image_url'] = product.css('.wp-post-image::attr(src)').get()
                item['url'] = product.css('.nombre_producto_ug a::attr(href)').get()

                yield item

            next_page_url = self.get_category_next_page_url(response.url)
            self.logger.info("Going to next page --> {}".format(next_page_url))

            yield scrapy.Request(url=next_page_url, callback=self.parse_category_page)
        else:
            self.logger.info('No Products found, reached last page of search')

    def get_category_next_page_url(self, current_category_url):
        """
         Get the category id from the url and join it with the categories url and add the pagination
        """
        found = re.findall(r"/(\d+)", current_category_url)

        category = found[0]
        current_page = int(found[1]) if len(found) > 1 else 0

        # url example -> 'https://www.tupi.com.py/rubros_paginacion/9/1/'
        return '/'.join([self.category_url, category, str(current_page + 1), ''])
