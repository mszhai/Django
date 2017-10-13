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
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    group = models.CharField(max_length=200, default='doctor')
    phone = models.CharField(max_length=200, blank=True)
    docname = models.CharField(max_length=200, blank=True)

class PatientInfo(models.Model):
    patid_fk = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)
    birthday = models.DateTimeField(null=True)
    sex = models.CharField(max_length=2, null=True)
    update_time = models.DateTimeField(auto_now=True)

class HospitalizationInfo(models.Model):
    hospitno_fk = models.CharField(max_length=50, null=True)
    evaluate_status = models.IntegerField(default=1)
    patid = models.ForeignKey(PatientInfo, null=True, on_delete=None)
    patid_fk = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Profile, default=999999, on_delete=None)
    entdate = models.DateTimeField(null=True)
    outdate = models.DateTimeField(null=True)
    dignose = models.CharField(max_length=50, null=True)
    update_time = models.DateTimeField(auto_now=True)
    fallowupdate = models.DateTimeField(null=True)
    bingcheng = models.CharField(max_length=200, blank=True)

class Barthel(models.Model):
    hospid = models.ForeignKey(HospitalizationInfo, on_delete=None)
    profile = models.ForeignKey(Profile, on_delete=None)
    evaluate_time = models.DateTimeField(auto_now=True)
    dabian = models.IntegerField()
    xiaobian = models.IntegerField()
    xiushi = models.IntegerField()
    yongce = models.IntegerField()
    chifan = models.IntegerField()
    zhuanyi = models.IntegerField()
    huodong = models.IntegerField()
    chuanyi = models.IntegerField()
    louti = models.IntegerField()
    xizao = models.IntegerField()
    total_score = models.IntegerField()
    times = models.IntegerField()

class MedHistory(models.Model):
    hospid = models.ForeignKey(HospitalizationInfo, on_delete=None)
    stroke_time = models.DateTimeField(null=True)
    conservative_treatment = models.NullBooleanField(null=True)
    first_recover_care = models.NullBooleanField(null=True)
    diabetes = models.NullBooleanField(null=True)
    hypertension = models.NullBooleanField(null=True)
    smoke = models.NullBooleanField(null=True)
    drink = models.NullBooleanField(null=True)
    dignose = models.CharField(max_length=50, null=True)
    glu = models.IntegerField(null=True)
    tg = models.IntegerField(null=True)
    ldl_c = models.IntegerField(null=True)
    createtime = models.DateTimeField(auto_now=True)

class ModelResult(models.Model):
    hospid = models.ForeignKey(HospitalizationInfo, on_delete=None)
    m_id = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    prob_improve = models.FloatField(null=True, max_length=20)

class ModelResultFactor(models.Model):
    model_result_id = models.ForeignKey(ModelResult, on_delete=None)
    ci_high = models.FloatField(null=True, max_length=20)
    ci_low = models.FloatField(null=True, max_length=20)
    factor_name = models.CharField(max_length=200, null=True)
    is_positive = models.NullBooleanField(null=True)
    odds_ratio = models.FloatField(null=True, max_length=20)
    p_value = models.FloatField(null=True, max_length=20)

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
