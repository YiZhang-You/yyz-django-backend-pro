"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:07
@Remark: 路由文件
"""
from rest_framework import routers

from containerapp.system.views.permission import PermissionViewSet
from containerapp.system.views.roles import RoleViewSet
from containerapp.system.views.users import UsersViewSet

system_url = routers.SimpleRouter()
system_url.register(r'user', UsersViewSet, basename="users")
system_url.register(r'role', RoleViewSet, basename="roles")
system_url.register(r'permission', PermissionViewSet, basename="permissions")

urlpatterns = [
    # re_path('user/export/', UsersViewSet.as_view({'get': 'export'})),

    # path(r'file/', RoleDownloadView.as_view({"get": "list"}), name="stafffiledownload"),

]
urlpatterns += system_url.urls
