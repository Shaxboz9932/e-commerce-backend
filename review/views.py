from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from review.models import Review
from review.serializers import ReviewSerializer
from .permissions import IsYourReview


class ReviewListorCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        exists = Review.objects.filter(user=request.user, product=request.data['product']).exists()
        if exists:
            return Response({'detail': "Siz bu maxsulotga review qoldirgansiz..."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data)

class ReviewUpdateOrDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsYourReview]

    def patch(self, request, pk):
        review = get_object_or_404(Review, id=pk)

        # Object permission tekshiriladi
        self.check_object_permissions(request, review)

        serializer = ReviewSerializer(
            instance=review,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = get_object_or_404(Review, id=pk)

        # Object permission tekshiriladi
        self.check_object_permissions(request, review)

        review.delete()
        return Response({"detail": "Siz review o‘chirdingiz"})


# 12.5

class GetReviewsByProductId(APIView):

    def get(self, request, pk):
        reviews = Review.objects.filter(product=pk)
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(serializer.data)

# 12.5