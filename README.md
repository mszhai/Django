Django
=====
> A Django projection, for practicing.

启动服务器：
```python
python manage.py runserver 0.0.0.0:8000
```

关闭防火墙，访问 http://10.111.11.67:8000/index.html

设置：ALLOWED_HOSTS = ['*']

## echarts
* [所需图标列表](https://github.com/ecomfe/echarts/blob/master/index.js)

style="background:#F36A5A
 style="white-space:nowrap"



## Django 时间与时区设置问题

在Django的配置文件settings.py中，有两个配置参数是跟时间与时区有关的，分别是TIME_ZONE和USE_TZ
如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。

如果USE_TZ 设置为False，而TIME_ZONE设置为None，则Django还是会使用默认的America/Chicago时间。若TIME_ZONE设置为其它时区的话，则还要分情况，如果是Windows系统，则TIME_ZONE设置是没用的，Django会使用本机的时间。如果为其他系统，则使用该时区的时间，入设置USE_TZ = False, TIME_ZONE = 'Asia/Shanghai', 则使用上海的UTC时间。

## csrf
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt