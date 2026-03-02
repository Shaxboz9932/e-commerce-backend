from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from .permissions import IsYourItem
from .serializers import CartItemSerializer

class CartItemListOrCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if cart_items.exists():
            serializer = CartItemSerializer(instance=cart_items, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Savatda hali maxsulot yuq..."}, status=404)

    def post(self, request):
        product_id = request.data.get("product_id")

        cart_item = CartItem.objects.filter(user=request.user, product_id=product_id)

        if cart_item.exists():
            return Response({"detail": "Bu maxsulot savatda bor..."},status=status.HTTP_409_CONFLICT)

        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsYourItem]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)
        self.check_object_permissions(request, cart_item)

        cart_item.delete()
        return Response({"detail": "Maxsulotni savatdan o'chirdingiz..."})

class CartItemQuantityUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsYourItem]

    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)
        self.check_object_permissions(request, cart_item)

        serializer = CartItemSerializer(instance=cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

