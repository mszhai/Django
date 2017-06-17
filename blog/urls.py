from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^hello$', views.hello, name='hello'),
    url(r'^test01$', views.test),
    url(r'^echarts/', views.echarts),
    url(r'^pie/', views.pie),
    url(r'^test02/', views.test02),
    url(r'^doctor/', views.doctor),
    url(r'^index.html', views.index, name='index'),
    url(r'^nav/$', views.others),
    url(r'^doctor01.html/', views.doctor01, name='doctor01'),
    url(r'^doctor02.html/', views.doctor02, name='doctor02'),
]