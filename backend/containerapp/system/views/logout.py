"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/2/9 14:42
@Remark: 注销
"""
from rest_framework.views import APIView

from containerapp.utils.json_response import SuccessResponse


class CancellationView(APIView):

    def post(self, request, *args, **kwargs):
        request.user.delete()
        return SuccessResponse(data=None)

