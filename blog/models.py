from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class API_UserInfo(models.Model):
    #id = models.AutoField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

    #class Meta:
        #permissions = 

class Profile(models.Model):
    user = models.OneToOneField(User)

    group = models.CharField(max_length=200, default='doctor')
    phone = models.CharField(max_length=200, blank=True)
    
"""
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name

class Classification(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Article(models.Model):
    caption = models.CharField(max_length=30)
    subcaption = models.CharField(max_length=50, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author)
    classification = models.ForeignKey(Classification)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
"""
