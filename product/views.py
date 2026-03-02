from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product.filters import ProductFilter
from product.models import Product, Category, Brand
from product.permissions import IsAdminForPost, IsAdminForPatch, IsAdminForDelete
from product.serializers import ProductSerializer, CategorySerializer, BrandSerializer
from product.pagination import MyPagination

from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class GetProductsAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, IsAdminForPost]
    filterset_class = ProductFilter

    def get(self, request):
        queryset = Product.objects.all()

        # filter
        filter_backend = DjangoFilterBackend()
        queryset = filter_backend.filter_queryset(
            request=request,
            queryset=queryset,
            view=self
        )

        # ordering
        order = request.query_params.get('order')
        if order == 'price':
            queryset = queryset.order_by('price')
        elif order == '-price':
            queryset = queryset.corder_by('-price')

        total_count = queryset.count()

        if total_count == 0:
            return Response({
                'detail': "Empty page",
                'results': []
            }, status=status.HTTP_200_OK)


        paginator = Paginator(queryset, 8)
        page_number = request.GET.get("page", 1) # default holatda 1
        page_range = []
        try:
            page_obj = paginator.page(page_number)
            for p in paginator.page_range:
                page_range.append(p)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            return Response({"detail": "Empty page"}, status=404)

        serializer = self.serializer_class(page_obj.object_list, many=True)

        # base url (query params saqlanadi)
        base_url = request.build_absolute_uri(request.path)

        return Response({
            "count": total_count,
            "page": int(page_number),
            "next": page_obj.has_next(),
            "previous": page_obj.has_previous(),
            "next_link": f"{base_url}?page={page_obj.next_page_number()}&brand={request.GET.get('brand', '')}&category={request.GET.get('category', '')}&search={request.GET.get('search', '')}" if page_obj.has_next() else None,
            "previous_link": f"{base_url}?page={page_obj.previous_page_number()}&brand={request.GET.get('brand', '')}&category={request.GET.get('category', '')}&search={request.GET.get('search', '')}" if page_obj.has_previous() else None,
            "start_index": page_obj.start_index(),
            "end_index": page_obj.end_index(),
            "page_range": page_range,
            "page_number": int(page_number),
            "results": serializer.data,

        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetProductAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, IsAdminForPatch, IsAdminForDelete]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = self.serializer_class(instance=product)
        return Response(serializer.data)

    def patch(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = self.serializer_class(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"detail": "Maxsulot o'chirildi"})

class GetCategory(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)

class GetBrand(APIView):
    serializer_class = BrandSerializer

    def get(self, request):
        brands = Brand.objects.all()
        serializer = self.serializer_class(brands, many=True)
        return Response(serializer.data)

