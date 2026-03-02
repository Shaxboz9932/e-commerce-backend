from django_filters import FilterSet, NumberFilter, CharFilter

from product.models import Product


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    category = CharFilter(field_name='category__title', lookup_expr='iexact')
    brand = CharFilter(field_name='brand__title', lookup_expr='iexact')

    search = CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ['category', 'brand']
