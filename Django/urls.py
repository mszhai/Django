"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from . import view
from blog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello$', view.hello),
    url(r'^test01$', view.test),
    url(r'^echarts/', view.echarts),
    url(r'^pie/', view.pie),
    url(r'^test02/', view.test02),
    url(r'^doctor/', view.doctor),
    url(r'^index/', views.index),
    url(r'^index/$', views.others),
    url(r'^doctor01.html/', views.doctor01),
    url(r'^doctor02.html/', views.doctor02),
    #url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': 'static/'}),
]
