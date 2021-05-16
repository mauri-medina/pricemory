from django.db import models


# Create your models here.
from django.db.models.functions import Upper


class Brand(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'brand'
        ordering = [Upper('name')]

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    url = models.CharField(max_length=400, null=False)
    description = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'shop'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=400, null=False)
    description = models.CharField(max_length=400, null=True)
    barcode = models.CharField(max_length=200, null=True)
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=400, null=False, unique=True)
    image_url = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'price_history'
