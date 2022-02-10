"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/2/9 15:08
@Remark: 自定义权限
"""
import re

from rest_framework.permissions import IsAuthenticated

from application.settings.dev import WHITELIST


def ValidationApi(reqApi, validApi):
    """
    验证当前用户是否有接口权限
    :param reqApi: 当前请求的接口
    :param validApi: 用于验证的接口
    :return: True或者False
    """
    if validApi is not None:
        valid_api = validApi.replace('{id}', '.*?')
        matchObj = re.match(valid_api, reqApi, re.M | re.I)
        if matchObj:
            return True
        else:
            return False
    else:
        return False


class CustomPermission(IsAuthenticated):
    """自定义权限"""

    def has_permission(self, request, view):
        """
        1. 获取当前用户请求的URL
        2. 获取当前用户权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        # return True
        # 判断是否是超级管理员
        if request.user.is_superuser:
            return True
        else:
            api = request.path  # 当前请求接口
            method = request.method  # 当前请求方法
            method_list = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
            method = method_list.index(method)
            if api in WHITELIST and int(request.user.is_active) == 1:
                return True
            if not hasattr(request.user, "role"):
                return False
            url_list = request.user.role.filter(permissions__isnull=False).values(  # 获取当前用户的角色拥有的所有接口
                "permissions__url",
                "permissions__method",
            ).order_by("permissions__id").distinct()
            for item in url_list:
                valid = ValidationApi(api, item.get('permissions__url'))
                if valid and (method == item.get('permissions__method')):
                    return True
        return False
