from django.db import models


# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    url = models.CharField(max_length=400, null=False)
    description = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

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
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)






