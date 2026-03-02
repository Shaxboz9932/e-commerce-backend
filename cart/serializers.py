from rest_framework import serializers
from cart.models import CartItem
from product.models import Product
from product.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    class Meta:
        model = CartItem
        fields = ["id", "user", "quantity", "added_at", "product", "product_id"]

        read_only_fields = ["user"]
