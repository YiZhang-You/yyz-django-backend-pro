"""
@author: 游YIZHANG
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 12:17
@Remark: 用户登录
"""
import base64
from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import serializers
from captcha.models import CaptchaStore
from captcha.views import captcha_image
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import Users
from ...utils.json_response import SuccessResponse
from ...utils.throttle import RecordThrottle


class CaptchaView(APIView):
    """生成图片验证码"""
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        hash_key = CaptchaStore.generate_key()  # 生成hash
        print(f"验证码：{CaptchaStore.objects.filter(hashkey=hash_key).first().response}")
        image = captcha_image(request, hash_key)
        image_base = base64.b64encode(image.content)
        json_data = {"key": hash_key, "image_base64/png": "data:" + image_base.decode('utf-8')}
        return SuccessResponse(data=json_data)


class LoginSerializer(TokenObtainPairSerializer):
    captcha = serializers.CharField(min_length=4, max_length=4, required=False,
                                    error_messages={
                                        "max_length": "图片验证码格式错误",
                                        "min_length": "图片验证码格式错误",
                                        "required": "请输入图片验证码"
                                    }, help_text="图片验证码")
    captcha_key = serializers.CharField(max_length=255, required=False,
                                        error_messages={
                                            "max_length": "格式错误",
                                            "required": "请输入图片验证码"
                                        }, help_text="验证码的key", )

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {
        'no_active_account': ('该账号已被禁用,请联系管理员')
    }

    def validate(self, attrs):
        # 验证码
        captcha = attrs["captcha"]
        captcha_key = attrs["captcha_key"]
        captcha_obj = CaptchaStore.objects.filter(hashkey=captcha_key).first()
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=10, seconds=0)  # 大于刷新时间验证码到期
        if not captcha_obj:
            raise ValidationError(detail="验证码过期！")
        if five_minute_ago > captcha_obj.expiration:
            captcha_obj.delete()
            raise ValidationError(detail="验证码过期！")
        else:
            if str(captcha).lower() == captcha_obj.response:
                captcha_obj.delete()
            else:
                captcha_obj.delete()
                raise ValidationError(detail="验证码输入错误")

        username = attrs['username']
        password = attrs['password']
        user = Users.objects.filter(Q(username=username)).first()
        if user and user.check_password(password):  # check_password() 对明文进行加密,并验证
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['username'] = self.user.username
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            result = {
                "code": 1,
                "message": "success",
                "data": data
            }
        else:
            result = {
                "code": 0,
                "message": "error",
                "data": "账号/密码不正确"
            }
        return result


class LoginView(TokenObtainPairView):
    """修改用户登录
    用户调用登录接口先去加载`api/captcha/`图片验证码接口，然后登录的时候把key和验证码传递过来即可
    """
    serializer_class = LoginSerializer
