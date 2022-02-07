"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/2/6 21:48
@Remark: 初始化数据
"""
import os

import django

from containerapp.system.models import Permission, Role, Users
from containerapp.utils.core_initialize import CoreInitialize

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.dev')
django.setup()


class Initialize(CoreInitialize):
    def init_role(self):
        """
        初始化角色表
        """
        data = [
            {"id": 1, "title": "管理员", "key": "admin", "sort": 1, "remark": "备注：",
             "status": 1, "permissions": [1, 2]  # 全部权限
             },
            {"id": 2, "title": "总经理", "key": "admin", "sort": 1, "remark": "备注：",
             "status": 1, "permissions": [ele.get("id") for ele in self.menu_button_data]  # 全部权限
             },

        ]
        self.save(Role, data, "角色表")

    def init_permission(self):
        """
        初始化菜单权限表
        """
        self.menu_button_data = [
            {"id": 1, "title": "用户新增",
             "value": "1", "url": "/api/system/user/", "method": 1, "icon": "311234", "is_menu": False},
            {"id": 2, "title": "用户查看",
             "value": "1", "url": "/api/system/user/", "method": 0, "icon": "311234", "is_menu": True},

        ]
        self.save(Permission, self.menu_button_data, "菜单权限表")
    def init_users(self):
        """
        初始化用户表
        """
        data = [
            {"id": 1,
             "password": "123456",
             "is_superuser": 0, "is_staff": 0,
             "is_active": 1, "username": "test", "name": "测试",
             "role": [1,],
             },
            {"id": 2,
             "password": "123456",
             "is_superuser": 1, "is_staff": 1,
             "is_active": 1, "username": "superadmin", "name": "超级管理员",
             "role": [2, ],

             },

        ]
        self.save(Users, data, "用户表")
    def run(self):
        self.init_permission()
        self.init_role()
        self.init_users()


# 项目init 初始化，默认会执行 main 方法进行初始化
def main(reset=False):
    Initialize(reset).run()
    pass


if __name__ == '__main__':
    main()
