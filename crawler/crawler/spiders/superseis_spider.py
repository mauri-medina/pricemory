import scrapy

# scrapy crawl superseis_spider -o superseis_products.json

from ..items import ProductItem


class SuperseisSpider(scrapy.Spider):
    name = 'superseis_spider'
    allowed_domains = ['superseis.com.py']
    start_urls = ['http://superseis.com.py/']

    custom_settings = {
        'SHOP_NAME': 'Superseis',
        'SHOP_URL': start_urls[0],
    }

    def parse(self, response):
        scraped_links = list(set(response.css('.level3 .collapsed::attr(href)').getall()))
        categories_link = list(set(scraped_links))

        for category in categories_link:
            yield scrapy.Request(url=category, callback=self.parse_category_page)

    def parse_category_page(self, response):
        products = response.css('.product-title-link')

        for product in products:
            product_link = product.css('::attr(href)').get()
            yield scrapy.Request(url=product_link, callback=self.parse_product_page)

        next_page_link = response.css('span~ a+ a::attr(href)').get()
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse_category_page)

    def parse_product_page(self, response):
        item = ProductItem()

        name = response.css('.productname::text').get()
        if name:
            item['name'] = name.strip()

        barcode = response.css('.sku::text').get()
        if barcode:
            item['barcode'] = barcode.strip().split(':')[1]

        price = response.css('.productPrice::text').get()
        if price:
            # todo should i do this in a pipeline??
            price = price.replace('.', '')
            price = price.strip()

            item['price'] = int(price)

        brand = response.css('.manufacturers a::text').get()
        if brand:
            item['brand'] = brand.strip()

        item['image_url'] = response.css('#img-slider img::attr(src)').get()
        item['url'] = response.request.url

        yield item
