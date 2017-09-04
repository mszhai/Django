from django.contrib import admin

# Register your models here.
from .models import API_UserInfo
from .models import Profile

admin.site.register(API_UserInfo)
admin.site.register(Profile)
