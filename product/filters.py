import django_filters
from django import forms
from django_filters import CharFilter

from .models import *


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',
                      widget=forms.TextInput(attrs={'class': 'input'}))

    url = CharFilter(field_name='url', lookup_expr='icontains',
                     widget=forms.TextInput(attrs={'class': 'input'}))

    barcode = CharFilter(field_name='barcode', lookup_expr='icontains',
                         widget=forms.TextInput(attrs={'class': 'input'}))

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image_url', 'description', 'date_created']
