from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer
from wishlist.models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    class Meta:
        model =WishlistItem
        fields = ["id", "user", "product", 'created_at', 'product_id']

        read_only_fields = ['user']
