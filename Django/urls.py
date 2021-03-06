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

from django.contrib.staticfiles import views
from django.conf import settings

#from . import view
from blog import views as view_blog

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^medcare/', include('blog.urls')),
    url(r'login.html', view_blog.login, name='login'),
    url(r'^$', view_blog.login, name='login'),
    #url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': 'static/'}),
]

if settings.DEBUG is False:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': settings.STATIC1_ROOT}, name="static"),
        #url(r'^media/(?P<path>.*)$', views.static.serve, {'document_root': settings.MEDIA_ROOT}, name="media")
    ]
