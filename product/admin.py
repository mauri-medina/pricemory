from django.contrib import admin

# Register your models here.
from product.models import *

admin.site.register(Brand)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(PriceHistory)