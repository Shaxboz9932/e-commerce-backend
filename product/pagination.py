from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPagination(PageNumberPagination):
    page_size_query_param = 'page-size'
    page_size = 9

    def get_paginated_response(self, data):
        # CursorPagination odatda count qaytarmaydi,
        # shuning uchun queryset.count() ni olish uchun self.page.queryset ishlatamiz


        return Response({
            "next": self.get_next_link(),
            'results': data
        })
