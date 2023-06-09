"""
@author: 游YIZHANG
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/2/9 15:25
@Remark: 记录日志
"""
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from containerapp.system.models import OperationLog, Permission
from containerapp.utils.request_util import get_request_user, get_request_ip, get_request_data, get_request_path, \
    get_os, get_browser


class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.operation_log_id = None
        self.content = None
        self.message = None

    def process_request(self, request):
        request.request_ip = get_request_ip(request)  # 获取ip
        request.request_data = get_request_data(request)  # 获取用户请求数据
        request.request_path = get_request_path(request)  # 获取用户请求地址

    def process_response(self, request, response):
        body = getattr(request, 'request_data', {})
        if isinstance(body, dict) and body.get('password', ''):  # 将请求密码变成*
            body['password'] = '*' * len(body['password'])
        get_request_user(request)
        method_list = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        modular = Permission.objects.filter(method=method_list.index(request.method), url=request.request_path).first()
        user = get_request_user(request)
        try:
            self.content = response.data.get("code")
            self.message = response.data.get("message")
        except:
            self.content = 0
            self.message = "服务器错误！"

        info = {
            'request_path': request.request_path,
            'request_body': body,
            'request_method': request.method,
            'request_ip': request.request_ip,
            'request_browser': get_browser(request),
            'response_code': self.content,
            "user": user if not isinstance(user, AnonymousUser) else None,
            'request_os': get_os(request),
            "request_modular": modular.title if modular else "*",
            'request_msg': request.session.get('request_msg'),
            'status': True if self.content in [1, ] else False,
            'json_result': {"code": self.content, "message": self.message},
        }

        OperationLog.objects.update_or_create(defaults=info, id=self.operation_log_id)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        return

    def process_exception(self, request, exception):
        pass
