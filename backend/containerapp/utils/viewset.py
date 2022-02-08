"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:19
@Remark: 自定义视图集
"""
from rest_framework.viewsets import ModelViewSet

from containerapp.utils.json_response import SuccessResponse, ErrorResponse


class CustomModelViewSet(ModelViewSet):
    """
    自定义的ModelViewSet:
    统一标准的返回格式;新增,查询,查询单个,修改，局部修改，删除
    """

    def create(self, request, *args, **kwargs):
        """创建"""
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return SuccessResponse(data=serializer.data)

    def list(self, request, *args, **kwargs):
        """查看"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """查看"""
        try:
            instance = self.get_object()
        except:
            return ErrorResponse(data="找不到查询对象！")
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """修改"""
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            return ErrorResponse(data="找不到修改对象！")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return SuccessResponse(data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """局部修改"""
        partial = kwargs.pop('partial', True)
        try:
            instance = self.get_object()
        except:
            return ErrorResponse(data="找不到修改对象！")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return SuccessResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除"""
        try:
            instance = self.get_object()
            print(instance,111)
        except:
            return ErrorResponse(data="找不到删除对象！")
        print(self.get_object(),222)
        self.perform_destroy(instance)
        return SuccessResponse(data="删除成功！")

