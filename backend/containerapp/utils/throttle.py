"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/1/20 10:26
@Remark: 自定义限流
"""
import time

from django_redis import get_redis_connection
from rest_framework.throttling import BaseThrottle


class RecordThrottle(BaseThrottle):
    """60秒只能访问3次
    更加用户IP地址保存在redis或者数据库
    """

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """返回True表示可以访问"""
        remote_addr = request.META.get('REMOTE_ADDR')  # 获取当前用户的IP
        ctime = time.time()
        redis_coon = get_redis_connection('access_record')
        record_list = redis_coon.lrange(remote_addr, 0, -1, )  # 获取全部的数据
        if not record_list:
            redis_coon.lpush(remote_addr, ctime)
        self.record_list = record_list
        try:
            show = True
            while show and float(record_list[-1]) < ctime - 6:  # 如果最后一个时间戳小于当前时间戳-60秒(就为True),
                if not redis_coon.rpop(remote_addr):  # 移除并返回最后一个
                    show = False
        except IndexError as e:
            pass
        finally:
            record_list = redis_coon.lrange(remote_addr, 0, -1, )  # 获取全部的数据
            if len(record_list) < 3:  # 只让访问3次
                redis_coon.lpush(remote_addr, ctime)
                return True

    def wait(self):
        """还需要等待多少秒才可以执行"""
        ctime = time.time()
        sleep = 6 - (ctime - float(self.record_list[0]))
        return 0 if sleep < 0 else sleep
