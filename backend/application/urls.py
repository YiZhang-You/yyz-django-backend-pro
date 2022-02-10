"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from containerapp.system.views.logout import CancellationView
from containerapp.system.views.login import LoginView, CaptchaView
from containerapp.utils.swagger import CustomOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="yyz-django-backend-pro",
        default_version='v1',
        description="接口文档",
        terms_of_service="https://www.tweet.org",
        contact=openapi.Contact(email="1246268651@qq.com"),
        license=openapi.License(name="YOUYIZHANG"),
    ),
    public=True,  # 如果为 False，则仅包括当前用户有权访问的端点
    permission_classes=(permissions.AllowAny,),  # 架构视图本身的权限类
    generator_class=CustomOpenAPISchemaGenerator,  # 使用的模式生成器类
)

# 这里结束

urlpatterns = [
    path('admin/', admin.site.urls),
    # DRF 提供的一系列身份认证的接口，用于在页面中认证身份，详情查阅DRF文档
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 刷新Token有效期的接口,当refresh快到期，可以调用这个接口传递refresh的token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/system/', include('containerapp.system.urls')),
    path('login/', LoginView.as_view()),  # 修改的登录,得到二个refresh，access(用这个token)
    path('cancellation/', CancellationView.as_view()),  # 注销用户（！删除）
    path('api/captcha/', CaptchaView.as_view()),  # 图片验证码
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- 这里
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # <-- 这里
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # <-- 这里
]

# https://www.apizza.net/project/9b2603cc9d479f649f35cc330efdb0be/browse 123456
# admin 123456
# admin11 123456aaa
