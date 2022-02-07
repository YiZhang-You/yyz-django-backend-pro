"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:27
@Remark: 自定义分页
"""
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class OrdinaryPageNumberPagination(PageNumberPagination):
    """普通分页"""
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 1),
            ('message', 'success'),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CuttingPageNumberPagination(LimitOffsetPagination):
    """切割分页"""
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 1),
            ('message', 'success'),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class EncryptionPageNumberPagination(CursorPagination):
    """加密分页"""
    cursor_query_param = 'cursor'
    page_size = 1
    ordering = 'id'
    page_size_query_param = 'size'
    max_page_size = 1

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 1),
            ('message', 'success'),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))