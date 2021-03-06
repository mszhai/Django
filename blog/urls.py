from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'barthelInput.html', views.barthel_input, name='barthel_input'),
    url(r'patinfo.html', views.patinfo, name='patinfo'),
    url(r'similarity.html', views.similarity, name='similarity'),
    url(r'predict.html', views.predict, name='predict'),
    url(r'admin.html', views.admin, name='admin'),
    url(r'dbshow.html', views.dbshow, name='dbshow'),
    url(r'^barthel.html', views.barthel, name='barthel'),
    url(r'^index.html', views.index, name='index'),
    url(r'^doctor.html', views.doctor, name='doctor'),
    url(r'^model.html', views.model, name='model'),
]

urlpatterns += [
    url(r'^logout', views.logout, name='logout'),
    url(r'^register.html', views.register, name='register'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^login_verify/$',views.login_verify, name='login_verify'),
    url(r'^login_success/$', views.login_success, name='login_success'),
]

urlpatterns += [
    # 新页面设计
    url(r'^patpanel.html', views.pat_panel, name='patpanel'),
    url(r'^evaluate.html', views.evaluate, name='evaluate'),
    url(r'^modelresult.html', views.model_result, name='modelresult'),
    url(r'^addpatient.html', views.add_patient, name='addpatient'),
    url(r'^evaluate_submit/$', views.evaluate_submit, name='evaluate_submit'),
    url(r'^addmodelpara.html', views.add_model_para, name='addmodelpara'),
    url(r'^predictdoc.html', views.predictdoc, name='predictdoc'),
    url(r'^predictbar.html', views.predictbar, name='predictbar'),
    url(r'^predict_model/$', views.predict_model, name='predict_model'),
    url(r'^modelpara/$', views.modelpara, name='modelpara'),
    url(r'^print_assessment', views.print_assessment, name='print_assessment'),
]

urlpatterns += [
    # ajax
    url(r'^patpanelRemove', views.patpanel_remove, name='patpanelRemove'),
]

urlpatterns += [
    url(r'^hello$', views.hello, name='hello'),
    url(r'^test01$', views.test),
    url(r'^echarts/', views.echarts),
    url(r'^pie/', views.pie),
    url(r'^test02/', views.test02),
    url(r'^nav/$', views.others),
    url(r'^doctor01.html/', views.doctor01, name='doctor01'),
    url(r'^doctor02.html/', views.doctor02, name='doctor02'),
]