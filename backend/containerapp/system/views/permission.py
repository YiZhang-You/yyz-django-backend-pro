import operator

from django_filters import FilterSet
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

from containerapp.system.models import Permission
from containerapp.utils.viewset import CustomMultipleModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination
from containerapp.utils.json_response import SuccessResponse, ErrorResponse


# ================================================= #
# ********************* 序列化 ******************** #
# ================================================= #
class PermissionListSerializer(serializers.ModelSerializer):
    """查看"""

    method = serializers.CharField(source="get_method_display")

    class Meta:
        model = Permission
        fields = "__all__"


class PermissionCreateSerializer(serializers.ModelSerializer):
    """新增"""

    class Meta:
        model = Permission
        fields = "__all__"

    def validate(self, attrs):
        if attrs["is_menu"]:
            attrs["parent"] = None
        return attrs


class PermissionUpdateSerializer(serializers.ModelSerializer):
    """修改"""

    class Meta:
        model = Permission
        fields = "__all__"


class PermissionPartialUpdateSerializer(serializers.ModelSerializer):
    """局部修改"""

    class Meta:
        model = Permission
        fields = "__all__"


# ================================================= #
# ********************* 过滤器 ******************** #
# ================================================= #
class PermissionFilter(FilterSet):
    class Meta:
        model = Permission
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "sort": ['exact', 'iexact', 'contains', 'icontains'],
            "url": ['exact', 'iexact', 'contains', 'icontains'],
            "method": ['exact', 'iexact', 'contains', 'icontains'],
            "icon": ['exact', 'iexact', 'contains', 'icontains'],
            "is_menu": ['exact', 'iexact'],
            "create_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
        }


# ================================================= #
# *********************** 视图 ******************** #
# ================================================= #
class PermissionViewSet(CustomMultipleModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = PermissionFilter

    def __init__(self, *args, **kwargs):
        super().__init__(Permission, PermissionUpdateSerializer)  # 使用批量操作的时候用

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            if id is None:
                return Permission.objects.all()
            else:
                return Permission.objects.filter(id=id)
        else:
            return Permission.objects.filter().none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return PermissionListSerializer
        elif self.action in ['create']:
            return PermissionCreateSerializer
        elif self.action in ['update']:
            return PermissionUpdateSerializer
        elif self.action in ['partial_update']:
            return PermissionPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def permission_tree_select(self, request, *args, **kwargs):
        """查看"""
        queryset = Permission.objects.all()
        serializer = PermissionListSerializer(data=queryset, many=True)
        serializer.is_valid()
        permission_dict = {}
        menu_list = []
        for item in serializer.data:
            id = item.get("id")
            parent = item.get("parent")
            if parent == None:
                permission_dict[id] = {
                    "id": item.get("id"),
                    "sort": item.get("sort"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "method": item.get("method"),
                    "icon": item.get("icon"),
                    "is_menu": item.get("is_menu"),
                    "parent": item.get("parent"),
                    "children": []
                }
            else:
                menu_list.append(item)

        for item in menu_list:
            permission_dict[item.get("parent")]["children"].append({
                "id": item.get("id"),
                "sort": item.get("sort"),
                "title": item.get("title"),
                "url": item.get("url"),
                "method": item.get("method"),
                "icon": item.get("icon"),
                "is_menu": item.get("is_menu"),
                "parent": item.get("parent"),
            })
        permission_dict = sorted(permission_dict.values(), key=lambda item: item["sort"], reverse=False)  # 外部sort排序
        for row in permission_dict:
            children = row.get("children")
            if children is not None:
                row["children"] = sorted(children, key=operator.itemgetter('sort'), reverse=True)  # 内部children中的sort排序
        return SuccessResponse(data=permission_dict)

    def web_router(self, request):
        """获取用户使用的权限permission"""
        user = request.user
        # 当前用户所有权限
        data = user.role.filter(permissions__isnull=False).values(
            "permissions__id",
            "permissions__title",
            "permissions__sort",
            "permissions__url",
            "permissions__method",
            "permissions__icon",
            "permissions__is_menu",
            "permissions__parent",
        ).order_by("permissions__id").distinct()
        if not data:
            return ErrorResponse(data="用户没有可访问任何权限！")
        permission_dict = {}
        menu_list = []
        for item in data:
            id = item.get("permissions__id")
            parent = item.get("permissions__parent")
            if parent == None:
                permission_dict[id] = {
                    'id': item['permissions__id'],
                    'sort': item['permissions__sort'],
                    'title': item['permissions__title'],
                    'url': item['permissions__url'],
                    'method': item['permissions__method'],
                    'icon': item['permissions__icon'],
                    'is_menu': item['permissions__is_menu'],
                    'parent': item['permissions__parent'],
                    'children': []
                }
            else:
                menu_list.append(item)
        for item in menu_list:
            parent = item.get("permissions__parent")
            permission_dict[parent]["children"].append({
                'id': item['permissions__id'],
                'sort': item['permissions__sort'],
                'title': item['permissions__title'],
                'url': item['permissions__url'],
                'method': item['permissions__method'],
                'icon': item['permissions__icon'],
                'is_menu': item['permissions__is_menu'],
                'parent': item['permissions__parent'],
            })
        permission_dict = sorted(permission_dict.values(), key=lambda item: item["sort"], reverse=False)  # 外部sort排序
        for row in permission_dict:
            children = row.get("children")
            if children is not None:
                row["children"] = sorted(children, key=operator.itemgetter('sort'), reverse=True)  # 内部children中的sort排序
        return SuccessResponse(data=permission_dict)
