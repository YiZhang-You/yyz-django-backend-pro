"""
@author: 游益章
@contact: WX:largestrongyyz QQ:1246268651
@Created on: 2022/2/6 21:48
@Remark: 初始化数据
"""
import os

import django

from containerapp.utils.core_initialize import CoreInitialize
from containerapp.system.models import Permission, Role, Users

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.dev')
django.setup()


class Initialize(CoreInitialize):
    def init_role(self):
        """
        初始化角色表
        """
        data = [
            {"id": 1, "title": "总经理", "key": "admin", "sort": 1, "status": 1,
             "permissions": [ele.get("id") for ele in self.menu_button_data + self.menu_button_parent_data]},  # 全部权限
            {"id": 2, "title": "经理", "key": "CEO", "sort": 2, "status": 1,
             "permissions": [1, 2, 3, 7, 8, 9, 13, 14, 15]},  # 全部权限
            {"id": 3, "title": "员工", "key": "user", "sort": 3, "status": 1, "permissions": [1, 2, 7, 8, 13, 14]},
            # 全部权限

        ]
        self.save(Role, data, "角色表")

    def init_permission(self):
        """
        初始化菜单权限表
        """
        id1 = Permission.objects.filter(id=1).first()
        id7 = Permission.objects.filter(id=7).first()
        id13 = Permission.objects.filter(id=13).first()
        self.menu_button_data = [
            {"id": 2, "title": "用户模块查看单个", "sort": "1", "url": "/api/system/user/{id}", "method": 0, "icon": "",
             "is_menu": False, "parent": id1},
            {"id": 3, "title": "用户模块新增", "sort": "2", "url": "/api/system/user/", "method": 1, "icon": "",
             "is_menu": False, "parent": id1},
            {"id": 4, "title": "用户模块删除", "sort": "3", "url": "/api/system/user/{id}", "method": 3, "icon": "",
             "is_menu": False, "parent": id1},
            {"id": 5, "title": "用户模块修改", "sort": "4", "url": "/api/system/user/{id}", "method": 2, "icon": "",
             "is_menu": False, "parent": id1},
            {"id": 6, "title": "用户模块局部修改", "sort": "5", "url": "/api/system/user/{id}", "method": 4, "icon": "",
             "is_menu": False, "parent": id1},
            {"id": 8, "title": "角色模块查看单个", "sort": "1", "url": "/api/system/role/{id}", "method": 0, "icon": "",
             "is_menu": False, "parent": id7},
            {"id": 9, "title": "角色模块新增", "sort": "2", "url": "/api/system/role/", "method": 1, "icon": "",
             "is_menu": False, "parent": id7},
            {"id": 10, "title": "角色模块删除", "sort": "3", "url": "/api/system/role/{id}", "method": 3, "icon": "",
             "is_menu": False, "parent": id7},
            {"id": 11, "title": "角色模块修改", "sort": "4", "url": "/api/system/role/{id}", "method": 2, "icon": "",
             "is_menu": False, "parent": id7},
            {"id": 12, "title": "角色模块局部修改", "sort": "5", "url": "/api/system/role/{id}", "method": 4, "icon": "",
             "is_menu": False, "parent": id7},
            {"id": 14, "title": "权限模块查看单个", "sort": "1", "url": "/api/system/permission/{id}", "method": 0, "icon": "",
             "is_menu": False, "parent": id13},
            {"id": 15, "title": "权限模块新增", "sort": "2", "url": "/api/system/permission/", "method": 1, "icon": "",
             "is_menu": False, "parent": id13},
            {"id": 16, "title": "权限模块删除", "sort": "3", "url": "/api/system/permission/{id}", "method": 3, "icon": "",
             "is_menu": False, "parent": id13},
            {"id": 17, "title": "权限模块修改", "sort": "4", "url": "/api/system/permission/{id}", "method": 2, "icon": "",
             "is_menu": False, "parent": id13},
            {"id": 18, "title": "权限模块局部修改", "sort": "5", "url": "/api/system/permission/{id}", "method": 4, "icon": "",
             "is_menu": False, "parent": id13},
            {"id": 19, "title": "权限模块批量删除", "sort": "6", "url": "/api/system/permission/multiple_delete/", "method": 3,
             "icon": "", "is_menu": False, "parent": id13},
            {"id": 20, "title": "权限模块批量局部修改", "sort": "7", "url": "/api/system/permission/multiple_partial_update/",
             "method": 2, "icon": "", "is_menu": False, "parent": id13},
            {"id": 21, "title": "权限模块批量修改", "sort": "8", "url": "/api/system/permission/multiple_update/", "method": 2,
             "icon": "", "is_menu": False, "parent": id13},
        ]

        self.save(Permission, self.menu_button_data, "菜单权限表")

    def init_parent_permission(self):
        self.menu_button_parent_data = [
            {"id": 1, "title": "用户模块查看", "sort": "1", "url": "/api/system/user/", "method": 0, "icon": "",
             "is_menu": True},
            {"id": 7, "title": "角色模块查看", "sort": "2", "url": "/api/system/role/", "method": 0, "icon": "",
             "is_menu": True},
            {"id": 13, "title": "权限模块查看", "sort": "3", "url": "/api/system/permission/", "method": 0, "icon": "",
             "is_menu": True},
        ]
        self.save(Permission, self.menu_button_parent_data, "菜单权限表")

    def init_users(self):
        """
        初始化用户表
        """
        data = [
            {"id": 1,
             "password": "pbkdf2_sha256$260000$XTCM9H6NfgntgnjVPaRQO9$LlzdSe+nF9bLMQM7FGQ08FVF/aEkTTaeDb0pASPNuLI=",
             "is_superuser": 1, "is_staff": 1, "is_active": 1, "username": "superadmin",
             "name": "超级管理员", "gender": 1, "email": "yyz@qq.com", "mobile": "88888888888"},
            {"id": 2,
             "password": "pbkdf2_sha256$260000$XTCM9H6NfgntgnjVPaRQO9$LlzdSe+nF9bLMQM7FGQ08FVF/aEkTTaeDb0pASPNuLI=",
             "is_superuser": 0, "is_staff": 0, "is_active": 1, "username": "admin",
             "name": "管理员", "gender": 0, "role": [2, 3]},
            {"id": 3,
             "password": "pbkdf2_sha256$260000$XTCM9H6NfgntgnjVPaRQO9$LlzdSe+nF9bLMQM7FGQ08FVF/aEkTTaeDb0pASPNuLI=",
             "is_superuser": 0, "is_staff": 0, "is_active": 1, "username": "test",
             "name": "测试", "gender": 0, "role": [2, 3]},
            {"id": 4,
             "password": "pbkdf2_sha256$260000$XTCM9H6NfgntgnjVPaRQO9$LlzdSe+nF9bLMQM7FGQ08FVF/aEkTTaeDb0pASPNuLI=",
             "is_superuser": 0, "is_staff": 0, "is_active": 0, "username": "customer",
             "name": "客户", "gender": 0, "role": [3, ]},
            {"id": 5,
             "password": "pbkdf2_sha256$260000$XTCM9H6NfgntgnjVPaRQO9$LlzdSe+nF9bLMQM7FGQ08FVF/aEkTTaeDb0pASPNuLI=",
             "is_superuser": 0, "is_staff": 0, "is_active": 1, "username": "supercustomer",
             "name": "总经理", "gender": 0, "role": [1, ]},
        ]
        self.save(Users, data, "用户表")

    def run(self):
        self.init_parent_permission()
        self.init_permission()
        self.init_role()
        self.init_users()


# 项目init 初始化，默认会执行 main 方法进行初始化
def main(reset=False):
    Initialize(reset).run()
    pass


if __name__ == '__main__':
    main()
