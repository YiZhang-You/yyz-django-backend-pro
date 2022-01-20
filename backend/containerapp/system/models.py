from django.db import models
from django.contrib.auth.models import AbstractUser

from containerapp.utils.models import CoreModel


class Users(AbstractUser, CoreModel):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号')
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True)
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True)
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True)
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")

    gender = models.IntegerField(choices=((0, "女"), (1, "男")), default=1, verbose_name="性别", null=True, blank=True)
    role = models.ManyToManyField(to='Role', verbose_name='关联角色')

    class Meta:
        db_table = "system_users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Role(CoreModel):
    title = models.CharField(verbose_name='角色名称', max_length=32)
    key = models.CharField(max_length=64, verbose_name="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序")
    remark = models.TextField(verbose_name="备注", null=True, blank=True)
    status = models.IntegerField(choices=((0, "禁用"), (1, "启用")), default=1, verbose_name="角色状态")
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    class Meta:
        db_table = "system_role"
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Permission(CoreModel):
    title = models.CharField(verbose_name='权限名称', max_length=32)
    value = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")

    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
        (4, "PATCH"),
        (5, "OPTIONS"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True, help_text="接口请求方法")
    icon = models.CharField(verbose_name='图标', max_length=32, null=True, blank=True, help_text='菜单才设置图标')
    is_menu = models.BooleanField(verbose_name='是否是菜单', default=False)

    class Meta:
        db_table = "system_permission"
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = 'system_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
