from django_filters import FilterSet
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend

from containerapp.system.models import Users
from containerapp.utils.json_response import ErrorResponse, SuccessResponse
from containerapp.utils.viewset import CustomModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination


# ================================================= #
# ****************** 序列化 ***************** #
# ================================================= #
class UsersListSerializer(serializers.ModelSerializer):
    """查看"""
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = Users
        fields = "__all__"
        # exclude = ["password", "user_permissions", "groups", "date_joined", "is_superuser"]
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


class UsersCreateSerializer(serializers.ModelSerializer):
    """新增"""
    password = serializers.CharField(required=False,
                                     default=make_password("123456".encode(encoding="UTF-8")))
    is_active = serializers.CharField(required=False, default=True)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]

    def validate_password(self, value):
        return make_password(f"{value}".encode(encoding="UTF-8"))


class UsersUpdateSerializer(serializers.ModelSerializer):
    """修改"""

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


class UsersPartialUpdateSerializer(serializers.ModelSerializer):
    """局部修改"""

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


# ================================================= #
# ****************** 过滤器 ***************** #
# ================================================= #
class UsersFilter(FilterSet):
    """
        根据名字过滤忽略大小写:使用双下划线的方式进行筛选（ 自定义django_filters不能有列表，可以改源码加个str()）
        http://127.0.0.1:8000/api/system/user/?username__icontains=admin3
    """

    class Meta:
        model = Users
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "gender": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            # "groups": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],  # 不能有列表
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
        # search_fields = ("id", 'name', 'username')  # 允许模糊查询的字段


# ================================================= #
# *********************** 视图 ********************* #
# ================================================= #
class UsersViewSet(CustomModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = UsersFilter

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
                return Users.objects.exclude(is_superuser=1).all()
            else:
                return Users.objects.exclude(is_superuser=1).filter(id=id)
        else:
            return Users.objects.filter().none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return UsersListSerializer
        elif self.action in ['create']:
            return UsersCreateSerializer
        elif self.action in ['update']:
            return UsersUpdateSerializer
        elif self.action in ['partial_update']:
            return UsersPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def user_info(self, request):
        """获取当前用户信息"""
        user = request.user
        data = {
            "name": user.name,
            "username": user.username,
            "mobile": user.mobile,
            "avatar": user.avatar,
            "gender": user.gender,
            "email": user.email,
        }
        return SuccessResponse(data=data)

    def update_user_info(self, request):
        """修改当前用户信息"""
        user = request.user
        user_obj = Users.objects.filter(id=user.id).first()
        serializer = UsersUpdateSerializer(user_obj, data=request.data.copy(), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data)

    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        instance = Users.objects.filter(id=kwargs.get('pk')).first()
        data = request.data
        old_pwd = data.get('oldPassword')
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(data="两次密码不匹配")
            if old_pwd == new_pwd:
                return ErrorResponse(data="修改密码和原密码一致")
            elif instance.check_password(old_pwd):
                instance.password = make_password(new_pwd.encode(encoding="UTF-8"))
                instance.save()
                return SuccessResponse(data=None)
            else:
                return ErrorResponse(data="旧密码不正确")
        else:
            return ErrorResponse(data="未获取到用户")
