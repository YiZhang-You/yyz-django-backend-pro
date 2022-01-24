from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers

from containerapp.system.models import Users
from containerapp.utils.viewset import CustomModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination


# ================================================= #
# ****************** 序列化 ***************** #
# ================================================= #
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


# ================================================= #
# ****************** 过滤器 ***************** #
# ================================================= #
class UsersFilter(FilterSet):
    # 根据名字过滤忽略大小写
    class Meta:
        model = Users
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "gender": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "groups": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "user_permissions": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "role": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "first_name": ['exact', 'iexact', 'contains', 'icontains'],
            "last_name": ['exact', 'iexact', 'contains', 'icontains'],
            "username": ['exact', 'iexact', 'contains', 'icontains'],
            "email": ['exact', 'iexact', 'contains', 'icontains'],
            "mobile": ['exact', 'iexact', 'contains', 'icontains'],
            "avatar": ['exact', 'iexact', 'contains', 'icontains'],
            "name": ['exact', 'iexact', 'contains', 'icontains'],
            "is_superuser": ['exact', 'iexact'],
            "is_staff": ['exact', 'iexact'],
            "is_active": ['exact', 'iexact'],
            "last_login": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "date_joined": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "create_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
        }
        # search_fields = ('name', 'username')  # 允许模糊查询的字段


# ================================================= #
# *********************** 视图 ********************* #
# ================================================= #
class UsersViewSet(CustomModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = UsersFilter
    # filter_fields = ('username', 'id')  # http://127.0.0.1:8000/api/system/user/?id=1

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
                return Users.objects.all()
            else:
                return Users.objects.filter(id=id)
        else:
            return Users.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return UserSerializer
        elif self.action in ['create']:
            return UserSerializer
        elif self.action in ['update']:
            return UserSerializer
        elif self.action in ['partial_update']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
