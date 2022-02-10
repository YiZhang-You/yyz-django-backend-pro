"""
@author: 游YIZHANG
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:19
@Remark: 自定义视图集 CustomMultipleModelViewSet(增删改查批量),CustomModelViewSet(增删改查),ListModelViewSet(查看,查看单个)
"""
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404

from containerapp.utils.json_response import SuccessResponse, ErrorResponse


class CustomMultipleModelViewSet(ModelViewSet):
    """
    统一标准的返回格式;新增,查询,查询单个,修改，局部修改，删除，批量操作
    """

    def __init__(self, class_models=None, class_serializer=None, *args, **kwargs):
        super().__init__()
        self.class_models = class_models
        self.class_serializer = class_serializer

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
        except:
            return ErrorResponse(data="找不到删除对象！")
        self.perform_destroy(instance)
        return SuccessResponse(data="删除成功！")

    # 批量操作
    # 通过many=True直接改造原有的API，使其可以批量创建  报错："无效数据。期待为字典类型，得到的是 list 。"
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    # 新增一个批量删除的API。删除单个对象，依然建议使用原API 通过DELETE访问访问 /multiple_delete/?pks=4,5
    @action(methods=["delete"], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        pks = request.query_params.get("pks", None)
        if not pks:
            return ErrorResponse(data="缺少参数！")
        for pk in pks.split(','):
            try:
                get_object_or_404(self.class_models, id=int(pk)).delete()
            except:
                return ErrorResponse(data="删除对象不存在！")
        return SuccessResponse(data="删除成功！")

    # 新增一个批量修改的API。更新单个对象，依然建议使用原API 通过PUT方法访问/multiple_update/
    # 发送json格式的数据，数据是个列表，列表中的每一项是个字典，每个字典是一个实例
    @action(methods=["put"], detail=False)
    def multiple_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = []
        for item in request.data:
            instance = get_object_or_404(self.class_models, id=int(item["id"]))
            serializer = self.class_serializer(instance, data=item, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data.append(serializer.data)  # 将数据添加到列表中
        return SuccessResponse(data=data)

    # 局部批量操作（还是要传递）
    @action(methods=["put"], detail=False)
    def multiple_partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        data = []
        for item in request.data:
            instance = get_object_or_404(self.class_models, id=int(item["id"]))
            serializer = self.class_serializer(instance, data=item, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data.append(serializer.data)
        return SuccessResponse(data=data)


class CustomModelViewSet(ModelViewSet):
    """
    统一标准的返回格式;新增,查询,查询单个,修改，局部修改，删除
    """

    def __init__(self, class_models=None, class_serializer=None, *args, **kwargs):
        super().__init__()
        self.class_models = class_models
        self.class_serializer = class_serializer

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
        except:
            return ErrorResponse(data="找不到删除对象！")
        self.perform_destroy(instance)
        return SuccessResponse(data="删除成功！")


class ListModelViewSet(ReadOnlyModelViewSet):
    """查询,查询单个"""

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
        """查看单个"""
        try:
            instance = self.get_object()
        except:
            return ErrorResponse(data="找不到查询对象！")
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)
