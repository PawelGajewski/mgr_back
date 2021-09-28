from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    max_limit = 5


# class PageNumberPaginationDataOnly(PageNumberPagination):
#     # Set any other options you want here like page_size

    # def get_paginated_response(self, data):
    #     return Response(data)