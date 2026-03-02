from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from .permissions import IsYourItem

class WishListOrCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wish_list = WishlistItem.objects.filter(user=request.user)
        serializer = WishlistItemSerializer(wish_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get("product_id")
        exists = WishlistItem.objects.filter(user=request.user, product_id=product_id).exists()

        if exists:
            return Response({"detail": "Bu maxsulot sizni ruyxatingizda bor..."}, status=status.HTTP_409_CONFLICT)

        serializer = WishlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WishlistItemDelete(APIView):
    permission_classes = [IsAuthenticated, IsYourItem]

    def delete(self, request, pk):
        wish_item = get_object_or_404(WishlistItem, id=pk)
        self.check_object_permissions(request, wish_item)

        wish_item.delete()
        return Response({"detail": "Maxsulotni sevimlilar ro'yxatidan o'chirdingiz..."})