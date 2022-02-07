"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:07
@Remark: 路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from containerapp.system.views.roles import RoleViewSet
from containerapp.system.views.users import UsersViewSet, UsersDownloadView

system_url = routers.SimpleRouter()
system_url.register(r'user', UsersViewSet, basename="users")
system_url.register(r'role', RoleViewSet, basename="roles")

urlpatterns = [
    re_path('user/export/', UsersDownloadView.as_view({'get': 'list'})),

    # path(r'file/', RoleDownloadView.as_view({"get": "list"}), name="stafffiledownload"),

]
urlpatterns += system_url.urls
