import random
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from product.filters import ProductFilter
from product.models import *


def price_history_chart(request):
    context = {
        'chart_query_params': dict(request.GET)
    }
    return render(request, 'product/price_history_chart.html', context=context)


def api_chart_data(request):
    ids = request.GET.getlist('product_id')
    if not ids:
        return JsonResponse({
            'error': 'At least one product ID must be passed'
        }, status=400)

    start_date = request.GET.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')

    end_date = request.GET.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

    product_query = Product.objects.filter(id__in=ids)

    response = []
    for product in product_query:
        # -- Product Data
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'barcode': product.barcode,
            'url': product.url,
            'image_url': product.image_url,
            'date_created': product.date_created
        }

        # -- Shop Data
        shop = product.shop
        product_data['shop'] = {
            'id': shop.id,
            'name': shop.name
        }

        # -- Brand Data
        brand = product.brand
        if brand:
            product_data['brand'] = {
                'id': brand.id,
                'name': brand.name
            }

        # -- Price history Data
        prices_query = product.pricehistory_set
        if start_date:
            prices_query = prices_query.filter(date_created__gte=start_date)

        if end_date:
            prices_query = prices_query.filter(date_created__lte=end_date)

        prices = []
        for price in prices_query.all():
            prices.append({
                'price': price.price,
                'date': price.date_created
            })
        product_data['price_history'] = prices

        response.append(product_data)

    return JsonResponse(
        data=response,
        safe=False,
    )


def search(request):
    products = None
    search_parameters = None
    product_filter = ProductFilter(request.GET)

    if request.GET:  # does the call have a search or page param?
        # -- FILTERING
        products = Product.objects.all()
        product_filter = ProductFilter(request.GET, queryset=products)

        products = product_filter.qs.annotate(num_prices=Count('pricehistory'))

        # -- ORDER
        order_by = []
        for key, value in request.GET.items():
            if 'sort-' in key:
                column = key.replace('sort-', '')
                order_type = ''
                if value == 'asc':
                    order_type = '-'

                order_by.append(order_type + column)

        order_by.append('name')  # always order by name by default
        products = products.order_by(*order_by)

        # -- PAGINATION
        # page_number = request.GET.get('page', 1)
        get_copy = request.GET.copy()
        page_number = int(get_copy.pop('page', ['1'])[0])
        items_per_page = 20

        paginator = Paginator(products, items_per_page)
        products = paginator.page(page_number)

        # search_parameters = request.GET.copy().urlencode()
        search_parameters = get_copy.urlencode()  # get all params without page

    context = {
        'products': products,
        'myFilter': product_filter,
        'parameters': search_parameters,
    }

    return render(request, 'product/home.html', context=context)
