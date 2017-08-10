from django.conf.urls import url
from blog import views

urlpatterns = [
    #url(r'', views.logout, name='logout'),
    url(r'^login_verify/$',views.login_verify, name='login_verify'),
    url(r'^login_success/$', views.login_success, name='login_success'),
    url(r'login.html', views.login, name='login'),
    url(r'dbshow.html', views.dbshow, name='dbshow'),
    url(r'^barthel.html', views.barthel, name='barthel'),
    url(r'^index.html', views.index, name='index'),
    url(r'^doctor.html', views.doctor, name='doctor'),
    url(r'^model.html', views.model, name='model'),
    url(r'^hello$', views.hello, name='hello'),
    url(r'^test01$', views.test),
    url(r'^echarts/', views.echarts),
    url(r'^pie/', views.pie),
    url(r'^test02/', views.test02),
    #url(r'^doctor/', views.doctor),
    url(r'^nav/$', views.others),
    url(r'^doctor01.html/', views.doctor01, name='doctor01'),
    url(r'^doctor02.html/', views.doctor02, name='doctor02'),
]