"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:07
@Remark: 路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

system_url = routers.SimpleRouter()


urlpatterns = [

]
urlpatterns += system_url.urls
