from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from containerapp.system.models import Permission
from containerapp.utils.viewset import CustomModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination


# ================================================= #
# ****************** 序列化 ***************** #
# ================================================= #
class PermissionListSerializer(serializers.ModelSerializer):
    """查看"""

    # status = serializers.CharField(source="get_status_display")
    method = serializers.CharField(source="get_method_display")

    class Meta:
        model = Permission
        fields = "__all__"


class PermissionCreateSerializer(serializers.ModelSerializer):
    """新增"""

    class Meta:
        model = Permission
        fields = "__all__"


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
# ****************** 过滤器 ***************** #
# ================================================= #
class PermissionFilter(FilterSet):
    class Meta:
        model = Permission
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "value": ['exact', 'iexact', 'contains', 'icontains'],
            "url": ['exact', 'iexact', 'contains', 'icontains'],
            "method": ['exact', 'iexact', 'contains', 'icontains'],
            "icon": ['exact', 'iexact', 'contains', 'icontains'],
            "is_menu": ['exact', 'iexact'],
            "create_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
        }


# ================================================= #
# *********************** 视图 ********************* #
# ================================================= #
class PermissionViewSet(CustomModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = PermissionFilter

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
