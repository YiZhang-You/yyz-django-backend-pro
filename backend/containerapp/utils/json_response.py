"""
@author: 游YIZHANG
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:20
@Remark: 自定义返回值
"""
from rest_framework.response import Response


class SuccessResponse(Response):
    """
    默认code返回1, 不支持指定其他返回码
    """

    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        std_data = {
            "code": 1,
            "message": "success",
            "data": data
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    """
    默认错误码返回0,
    """

    def __init__(self, data=None, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": 0,
            "message": "error",
            "data": data,

        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)
