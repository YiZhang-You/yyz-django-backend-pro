# 1、拉取项目

新建一个文件夹使用git拉取

```
git clone https://gitee.com/yyzlt/yyz-django-backend-pro.git
```

# 2、配置

找到settings,中的dev（开发）.和prod（生产）【部署修改的时候在manage.py中换成application.settings.prod】

## 2.1 配置数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'backend_pro'  # 数据库名字
    },
}
```

## 2.2 配置redis

```python
# redis
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/15",
        "OPTIONS": {
            "PASSWORD": "",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/14",
        "OPTIONS": {
            "PASSWORD": "",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "access_record": {  # 访问记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "PASSWORD": "",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
```

# 3、迁移文件

```python
python manage.py makemigrations
python manage.py migrate
python manage.py init_data  # 初始化数据
```



# 4、测试

```
http://127.0.0.1:8000/doc/
http://127.0.0.1:8000/redoc/

https://www.apizza.net/project/9b2603cc9d479f649f35cc330efdb0be/browse
密码：123456
```



# 5、报错解决

## 5.1 项目导包路径报红色，

选择根目录backend右键--》Mark Directory as -->第一个

```
https://blog.csdn.net/qq_30622831/article/details/80978118
```

## 5.2 使用django_filters报AttributeError: 'list' object has no attribute 'split'

改下载的django_filters中的widgets.py中的213行

```python
return value.split(',')
# return str(value).split(',')  # 把列表改成字符串，因为是版本的原因
```

## 5.3 访问接口文档的时候报错（未解决）