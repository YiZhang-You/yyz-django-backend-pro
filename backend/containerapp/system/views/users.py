from django.http import StreamingHttpResponse
from django_filters import FilterSet
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from containerapp.system.models import Users
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
        exclude = ["password", "role", "user_permissions", "groups", "date_joined", "is_superuser"]
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


class UsersCreateSerializer(serializers.ModelSerializer):
    """新增"""
    password = serializers.CharField(required=False,
                                     default=make_password("123456".encode(encoding="UTF-8")))
    is_active = serializers.CharField(required=False, default=True)

    class Meta:
        model = Users
        exclude = ["role", "user_permissions", "groups", "is_superuser"]
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]

    def validate_password(self, value):
        return make_password(f"{value}".encode(encoding="UTF-8"))


class UsersUpdateSerializer(serializers.ModelSerializer):
    """修改"""

    class Meta:
        model = Users
        exclude = ["role", "user_permissions", "groups", "is_superuser"]
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


class UsersPartialUpdateSerializer(serializers.ModelSerializer):
    """局部修改"""

    class Meta:
        model = Users
        exclude = ["role", "user_permissions", "groups", "is_superuser"]
        read_only_fields = ['id', 'update_datetime', 'create_datetime', ]


class FileRenderSerializer(serializers.ModelSerializer):
    """局部修改"""

    class Meta:
        model = Users
        exclude = ["role", "user_permissions", "groups", "is_superuser"]
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


# ================================================= #
# *********************** 下载 ********************* #
# ================================================= #
from rest_framework_csv.renderers import CSVStreamingRenderer


def file_headers():
    return [
        'id',
        'username',
        'name',
    ]


def cn_data_header():
    return dict([
        ('id', u'员工用户名'),
        ('username', u'员工类型'),
        ('name', u'创建时间'),
    ])


def en_data_header():
    return dict([
        ('staff_name', u'Staff Name'),
        ('staff_type', u'Staff Type'),
        ('create_time', u'Create Time'),
    ])


class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()


class FileRenderEN(CSVStreamingRenderer):
    header = file_headers()
    labels = en_data_header()


from rest_framework.filters import OrderingFilter


class UsersDownloadView(CustomModelViewSet):
    renderer_classes = (FileRenderCN,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', ]
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
        if self.action in ['list']:
            return FileRenderSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return FileRenderCN().render(data)
            else:
                return FileRenderEN().render(data)
        else:
            return FileRenderEN().render(data)

    def list(self, request, *args, **kwargs):
        from datetime import datetime
        dt = datetime.now()
        data = (
            FileRenderSerializer(instance).data
            for instance in self.filter_queryset(self.get_queryset())
        )
        renderer = self.get_lang(data)
        response = StreamingHttpResponse(
            renderer,
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='Users_{}.csv'".format(
            str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response
