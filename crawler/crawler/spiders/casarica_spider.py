import scrapy

from ..items import ProductItem

from urllib.parse import urljoin


class CasaRicaSpider(scrapy.Spider):
    name = 'casarica_spider'
    allowed_domains = ['casarica.com.py']
    start_urls = ['https://www.casarica.com.py/productos?q=']

    custom_settings = {
        'SHOP_NAME': 'Casa Rica',
        'SHOP_URL': 'https://www.casarica.com.py/',
    }

    def parse(self, response):
        product_links = response.css('.ecommercepro-LoopProduct-link::attr(href)').getall()
        for product_link in product_links:
            product_url = self.join_to_base_url(product_link)
            yield scrapy.Request(url=product_url, callback=self.parse_product_page)

        next_page = response.css('.next::attr(href)').get()
        if next_page:
            next_page = self.join_to_base_url(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product_page(self, response):
        item = ProductItem()

        name = response.css('.entry-title::text').get()
        if name:
            item['name'] = name.strip()

        item['barcode'] = response.css('#producto-codigo::text').get()

        price = response.css('#producto-precio::text').get()
        if price:
            price = price.replace('₲', '')
            price = price.replace('.', '')
            item['price'] = int(price.strip())

        # TODO couldn't find product brand information
        item['image_url'] = response.css('.zoom img::attr(data-src)').get()
        item['url'] = response.request.url

        yield item

    def join_to_base_url(self, to_join):
        return urljoin('https://www.casarica.com.py', to_join)
