from django_filters import FilterSet
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django_filters.rest_framework import DjangoFilterBackend

from containerapp.system.models import Role
from containerapp.utils.viewset import CustomModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination


# ================================================= #
# ********************* 序列化 ******************** #
# ================================================= #
class RoleListSerializer(serializers.ModelSerializer):
    """查看"""
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Role
        # exclude = ["permissions", ]
        fields = "__all__"


class RoleCreateSerializer(serializers.ModelSerializer):
    """新增"""
    title = serializers.CharField(required=True, max_length=80,
                                  validators=[
                                      UniqueValidator(queryset=Role.objects.all(), message="角色已存在")],
                                  )

    class Meta:
        model = Role
        exclude = ["permissions", ]


class RoleUpdateSerializer(serializers.ModelSerializer):
    """修改"""

    class Meta:
        model = Role
        fields = "__all__"


class RolePartialUpdateSerializer(serializers.ModelSerializer):
    """局部修改"""

    class Meta:
        model = Role
        fields = "__all__"


# ================================================= #
# ********************* 过滤器 ******************** #
# ================================================= #
class RoleFilter(FilterSet):
    class Meta:
        model = Role
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "sort": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "status": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "key": ['exact', 'iexact', 'contains', 'icontains'],
            "remark": ['exact', 'iexact', 'contains', 'icontains'],
            "create_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
        }


# ================================================= #
# *********************** 视图 ********************* #
# ================================================= #
class RoleViewSet(CustomModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = RoleFilter

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
                return Role.objects.all()
            else:
                return Role.objects.filter(id=id)
        else:
            return Role.objects.filter().none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return RoleListSerializer
        elif self.action in ['create']:
            return RoleCreateSerializer
        elif self.action in ['update']:
            return RoleUpdateSerializer
        elif self.action in ['partial_update']:
            return RolePartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
