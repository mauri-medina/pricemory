import scrapy

from ..items import ProductItem


class StockSpiderSpider(scrapy.Spider):
    name = 'stock_spider'
    allowed_domains = ['www.stock.com.py']
    start_urls = ['https://www.stock.com.py/']

    custom_settings = {
        'SHOP_NAME': 'Stock',
        'SHOP_URL': start_urls[0],
    }

    def parse(self, response):
        self.logger.info('Parse site: %s', response.url)
        scraped_links = list(set(response.css('.level3 .collapsed::attr(href)').getall()))
        categories_link = list(set(scraped_links))

        for category in categories_link:
            yield scrapy.Request(url=category, callback=self.parse_category_page)

    def parse_category_page(self, response):
        self.logger.info('Parse category: %s', response.url)

        products = response.css('.product-title-link')

        for product in products:
            product_link = product.css('::attr(href)').get()
            yield scrapy.Request(url=product_link, callback=self.parse_product_page)

        next_page_link = response.css('span~ a+ a::attr(href)').get()
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse_category_page)

    def parse_product_page(self, response):
        self.logger.info('Parse product: %s', response.url)

        # Some products redirects (http code: 301) to this page
        if 'gana.stock.com.py' in response.url:
            self.logger.warning('Ignoring url: %s', response.url)
        else:
            items = ProductItem()

            name = response.css('.productname::text').get()
            if name:
                items['name'] = name.strip()

            barcode = response.css('.sku::text').get()
            if barcode:
                items['barcode'] = barcode.strip().split(':')[1]

            price = response.css('.productPrice::text').get()
            if price:
                price = price.replace('.', '')
                price = price.strip()

                items['price'] = int(price)

            brand = response.css('.manufacturers a::text').get()
            if brand:
                items['brand'] = brand.strip()

            items['image_url'] = response.css('#img-slider img::attr(src)').get()
            items['url'] = response.request.url

            yield items
