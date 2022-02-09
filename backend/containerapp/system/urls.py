"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:07
@Remark: 路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from containerapp.system.views.operation_log import OperationLogViewSet
from containerapp.system.views.permission import PermissionViewSet
from containerapp.system.views.roles import RoleViewSet
from containerapp.system.views.users import UsersViewSet

system_url = routers.SimpleRouter()
system_url.register(r'user', UsersViewSet, basename="users")
system_url.register(r'role', RoleViewSet, basename="roles")
system_url.register(r'permission', PermissionViewSet, basename="permissions")
system_url.register(r'operation_log', OperationLogViewSet, basename="operation_logs")

urlpatterns = [
    path('user/user_info/', UsersViewSet.as_view({"get": "user_info"})),  # 登录成功获取用户的基本信息
    re_path(r'user/update_user_info/', UsersViewSet.as_view({"put": "update_user_info"})),  # 修改当前用户的信息
    re_path('user/change_password/(?P<pk>.*?)/', UsersViewSet.as_view({'put': 'change_password'})),  # 用户密码修改

    path('permission/web_router/', PermissionViewSet.as_view({'get': 'web_router'})),  # web_router函数的名称

    # re_path('user/export/', UsersViewSet.as_view({'get': 'export'})),

    # path(r'file/', RoleDownloadView.as_view({"get": "list"}), name="stafffiledownload"),

]
urlpatterns += system_url.urls
