from django.db import models
from django.contrib.auth.models import AbstractUser

from containerapp.utils.models import CoreModel


class Users(AbstractUser, CoreModel):
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    role = models.ManyToManyField(to='Role', verbose_name='关联角色', help_text="关联角色")
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name="邮箱", help_text="邮箱")
    mobile = models.CharField(max_length=255, null=True, blank=True, verbose_name="电话", help_text="电话")
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name="头像", help_text="头像")
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号', help_text="用户账号")
    gender = models.IntegerField(choices=((0, "女"), (1, "男")), default=1, null=True, blank=True, verbose_name="性别",
                                 help_text="性别")

    class Meta:
        db_table = "system_users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Role(CoreModel):
    key = models.CharField(max_length=64, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    title = models.CharField(max_length=32, verbose_name='角色名称', help_text="角色名称")
    remark = models.TextField(null=True, blank=True, verbose_name="备注", help_text="备注")
    permissions = models.ManyToManyField(to='Permission', blank=True, verbose_name='拥有的所有权限', help_text="拥有的所有权限")
    status = models.IntegerField(choices=((0, "禁用"), (1, "启用")), default=1, verbose_name="角色状态", help_text="角色状态")

    class Meta:
        db_table = "system_role"
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Permission(CoreModel):
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
        (4, "PATCH"),
        (5, "OPTIONS"),
    )
    title = models.CharField(max_length=32, verbose_name='名称', help_text="名称")
    sort = models.IntegerField(default=1, verbose_name="权限排序", help_text="权限排序")
    url = models.CharField(max_length=128, verbose_name='含正则的URL', help_text="含正则的URL")
    is_menu = models.BooleanField(default=False, verbose_name='是否是菜单', help_text="是否是菜单")
    method = models.IntegerField(choices=METHOD_CHOICES, verbose_name="接口请求方法", help_text="接口请求方法")
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name="菜单设置图标", help_text="菜单设置图标")
    parent = models.ForeignKey(to='self', null=True, blank=True, related_name='parents', on_delete=models.CASCADE,
                               verbose_name='关联的权限', help_text="关联的权限")  # 一个菜单下面有几个,只有is_menu=True，parent都为none

    class Meta:
        db_table = "system_permission"
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class OperationLog(CoreModel):
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")
    json_result = models.TextField(null=True, blank=True, verbose_name="返回信息", help_text="返回信息")
    request_msg = models.TextField(null=True, blank=True, verbose_name="操作说明", help_text="操作说明")
    request_body = models.TextField(null=True, blank=True, verbose_name="请求参数", help_text="请求参数")
    user = models.CharField(max_length=128, null=True, blank=True, verbose_name="操作人", help_text="操作人")
    request_os = models.CharField(max_length=64, null=True, blank=True, verbose_name="操作系统", help_text="操作系统")
    request_ip = models.CharField(max_length=32, null=True, blank=True, verbose_name="请求ip地址", help_text="请求ip地址")
    request_path = models.CharField(max_length=400, null=True, blank=True, verbose_name="请求地址", help_text="请求地址")
    request_method = models.CharField(max_length=8, null=True, blank=True, verbose_name="请求方式", help_text="请求方式")
    response_code = models.CharField(max_length=32, null=True, blank=True, verbose_name="响应状态码", help_text="响应状态码")
    request_modular = models.CharField(max_length=64, null=True, blank=True, verbose_name="请求模块", help_text="请求模块")
    request_browser = models.CharField(max_length=64, null=True, blank=True, verbose_name="请求浏览器", help_text="请求浏览器")

    class Meta:
        db_table = 'system_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
