from django_filters import FilterSet
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

from containerapp.system.models import OperationLog
from containerapp.utils.viewset import ListModelViewSet
from containerapp.utils.pagination import OrdinaryPageNumberPagination


# ================================================= #
# ********************* 序列化 ******************** #
# ================================================= #
class OperationLogListSerializer(serializers.ModelSerializer):
    """查看"""

    class Meta:
        model = OperationLog
        fields = "__all__"


# ================================================= #
# ********************* 过滤器 ******************** #
# ================================================= #
class OperationLogFilter(FilterSet):
    class Meta:
        model = OperationLog
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "request_modular": ['exact', 'iexact', 'contains', 'icontains'],
            "request_path": ['exact', 'iexact', 'contains', 'icontains'],
            "request_body": ['exact', 'iexact', 'contains', 'icontains'],
            "request_method": ['exact', 'iexact', 'contains', 'icontains'],
            "request_msg": ['exact', 'iexact', 'contains', 'icontains'],
            "request_ip": ['exact', 'iexact', 'contains', 'icontains'],
            "request_browser": ['exact', 'iexact', 'contains', 'icontains'],
            "response_code": ['exact', 'iexact', 'contains', 'icontains'],
            "request_os": ['exact', 'iexact', 'contains', 'icontains'],
            "json_result": ['exact', 'iexact', 'contains', 'icontains'],
            "status": ['exact', 'iexact', 'contains', 'icontains'],
            "create_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_datetime": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
        }


# ================================================= #
# *********************** 视图 ******************** #
# ================================================= #
class OperationLogViewSet(ListModelViewSet):
    pagination_class = OrdinaryPageNumberPagination
    filter_backends = (DjangoFilterBackend,)  # 导入过滤器
    filter_class = OperationLogFilter

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
                return OperationLog.objects.all()
            else:
                return OperationLog.objects.filter(id=id)
        else:
            return OperationLog.objects.filter().none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', ]:
            return OperationLogListSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
