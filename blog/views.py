from django.shortcuts import render
from django.conf import settings
import json
import os
from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
from blog.models import API_UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login0
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import blog.models as models
import datetime


@login_required
def evaluate(request):
    return render(request, 'blog/evaluate.html')

@login_required
def pat_panel(request):
    user = User.objects.get(username=request.user)
    role = models.Profile.objects.get(user_id=user.id)
    page_html = ''
    pat_panel = '''
    <div class="col-lg-3 col-sm-3">
        <div class="panel panel-info">
            <div class="panel-heading">
                <i class="fa fa-male"></i> {name}
            </div>
            <div class="panel-body">
                <table class="table table-condensed" frame="void">
                    <tr>
                        <td>住院号 </td>
                        <td>{hospno}</td>
                    </tr>
                    <tr>
                        <td>性别 </td>
                        <td>{sex} </td>
                    </tr>
                    <tr>
                        <td>年龄 </td>
                        <td>{age} </td>
                    </tr>
                    <tr>
                        <td>卒中类型 </td>
                        <td>{dignose} </td>
                    </tr>
                </table>
            </div>
            <div class="panel-footer">
                <a onclick="evaluate1('{patid1}')"><i class="fa fa-link"></i> 评定</a>
                <a onclick="check1({patid2})"><i class="fa fa-link"></i> 查看</a>
            </div>
        </div>
    </div>
    <!-- /.col-lg-3 -->
    '''
    if role.group == 'doctor':#in=[role.id]
        patients = models.HospitalizationInfo.objects.filter(doctor__in=[role.id, 999999])
        for pat in patients:
            a_patient = models.PatientInfo.objects.get(id=pat.patid_id)
            age = int((pat.entdate - a_patient.birthday).days / 365 + 1)
            page_html += pat_panel.format(name=a_patient.name, hospno=pat.hospitno_fk, sex=a_patient.sex, age=age, dignose=pat.dignose, patid1=pat.id, patid2=pat.id)
    page_html = mark_safe(page_html)
    ret = {"page_html": page_html}
    return render(request, 'blog/patpanel.html', ret)

def register(request):
    return render(request, 'blog/register.html')

def barthel_input(request):
    return render(request, 'blog/barthelInput.html')

def patinfo(request):
    return render(request, 'blog/patinfo.html')

# Create your views here.
def similarity(request):
    batthel_json = os.path.join(settings.BASE_DIR, 'json/result_pred_0626.json')
    with open(batthel_json, 'rt', encoding='utf8') as f:
        data = json.load(f)
    return render(request, 'blog/similarity.html', {'model_data': data})

def predict(request):
    return render(request, 'blog/predict.html')


def admin(request):
    return render(request, 'blog/admin.html')

@login_required
def index(request):
    data = {'Clinical': 90, 'Non-clinical': 54, 'Treatment': 33}
    data2 = {'血管栓塞史': 30,
             '糖尿病患病年数': 20,
             '高血压&心衰': 20,
             '颅内出血': 20,
             'BMI': 34,
             '目前吸烟': 10,
             '控制心室率药物': 10,
             'PCI最近一次时间': 10,
             '阿司匹林&\beta 阻滞剂': 15,
             'ARB&阿司匹林': 8}
    legend = list()
    inner_pie = list()
    out_pie = list()
    for element in data.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data[element]
        dic_tem['name'] = element
        inner_pie.append(dic_tem)
    for element in data2.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data2[element]
        dic_tem['name'] = element
        out_pie.append(dic_tem)
    return render(request, 'blog/index.html', {'legend': json.dumps(legend),
                                                'innerpie': json.dumps(inner_pie),
                                                'outpie': json.dumps(out_pie)})

def doctor(request):
    data = {'Clinical': 90, 'Non-clinical': 54, 'Treatment': 33}
    data2 = {'血管栓塞史': 30,
             '糖尿病患病年数': 20,
             '高血压&心衰': 20,
             '颅内出血': 20,
             'BMI': 34,
             '目前吸烟': 10,
             '控制心室率药物': 10,
             'PCI最近一次时间': 10,
             '阿司匹林&\beta 阻滞剂': 15,
             'ARB&阿司匹林': 8}
    legend = list()
    inner_pie = list()
    out_pie = list()
    for element in data.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data[element]
        dic_tem['name'] = element
        inner_pie.append(dic_tem)
    for element in data2.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data2[element]
        dic_tem['name'] = element
        out_pie.append(dic_tem)
    return render(request, 'blog/doctor.html', {'legend': json.dumps(legend),
                                                'innerpie': json.dumps(inner_pie),
                                                'outpie': json.dumps(out_pie)})

def model(request):
    return render(request, 'blog/model.html')

def others(request):
    return render(request, 'blog/nav.html')

def doctor02(request):
    return render(request, 'blog/doctor02.html')

def doctor01(request):
    data = {'Clinical': 90, 'Non-clinical': 54, 'Treatment': 33}
    data2 = {'血管栓塞史': 30,
             '糖尿病患病年数': 20,
             '高血压&心衰': 20,
             '颅内出血': 20,
             'BMI': 34,
             '目前吸烟': 10,
             '控制心室率药物': 10,
             'PCI最近一次时间': 10,
             '阿司匹林&\beta 阻滞剂': 15,
             'ARB&阿司匹林': 8}
    legend = list()
    inner_pie = list()
    out_pie = list()
    for element in data.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data[element]
        dic_tem['name'] = element
        inner_pie.append(dic_tem)
    for element in data2.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data2[element]
        dic_tem['name'] = element
        out_pie.append(dic_tem)
    return render(request, 'blog/doctor01.html', {'legend': json.dumps(legend),
                                                  'innerpie': json.dumps(inner_pie),
                                                  'outpie': json.dumps(out_pie)})

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'test/hello.html', context)

def test(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'test/test01.html', context)

def echarts(request):
    data_y = ['销售KA一部(高媛_京_销售经理)', '销售KA二部(李天明_京_销售主管)', '销售KA三部(刘扬_京_销售)', '销售精英一部(余姗姗_京_销售经理)', '销售精英二部(王凯_京_销售经理)', '销售精英三部(王欣_京_销售主管)', '销售精英四部(过成伟_京_销售)', '销售精英五部(王昆仑_京_销售)', '销售成长一部(王睿_京_销售经理)', '销售成长二部(尹龙君_京_销售主管)', '销售成长三部(张璐璐_京_销售经理)', '销售成长四部(刘倩_京_销售主管)', '销售成长五部(袁野_京_销售主管)', '销售成长七部(朱志明_京_销售主管)', '销售成长八部(丁世超_京_销售主管)', '销售成长九部(李艳丽_京_销售经理)', '销售成长十一部(孔繁星_京_销售经理)', '销售成长十二部(郄一潇_京_销售主管)', '销售成长十三部(孙媛媛_京_销售主管)', '销售成长十四部(陈焕锋_京_销售主管)',
            '销售成长十五部(王春艳_京_销售主管)', '销售成长十七部(陈爽_京_销售)', '销售成长十八部(杨婷婷_京_销售经理)', '销售培训一部(任源夏_京_销售经理)', '销售培训二部(张腾_京_销售)', '销售培训三部(张春燕_京_销售)', '销售培训四部(赵妍妍_京_销售主管)', '销售培训五部(吴功利_京_销售)', '销售培训六部(刘明_京_销售主管)', '销售培训七部(刘惠娟_京_销售主管)', '销售培训八部(唐景云_京_销售主管)']
    data_x = [3786.5, 3317.6, 2754.8, 2114.2 ,917.1, 1185.1, 1365.3, 2251.7, 627.8, 341.5, 655.0, 553.7, 733.5, 467.6,
              571.9, 590.8, 504.5, 346.7, 389.8, 539.1, 654.5, 581.4, 38.0, 19.4, 46.4, 7.7, 27.8, 22.2, 36.3, 26.1, 38.1]
    return render(request, 'test/echarts.html', {'dataY': json.dumps(data_y),
                                                 'dataX': json.dumps(data_x)})

def pie(request):
    return render(request, 'test/pie.html')

def test02(request):
    return render(request, 'test/test02.html')

def doctor03(request):
    data = {'Clinical': 90, 'Non-clinical': 54, 'Treatment': 33}
    data2 = {'血管栓塞史': 30,
             '糖尿病患病年数': 20,
             '高血压&心衰': 20,
             '颅内出血': 20,
             'BMI': 34,
             '目前吸烟': 10,
             '控制心室率药物': 10,
             'PCI最近一次时间': 10,
             '阿司匹林&\beta 阻滞剂': 15,
             'ARB&阿司匹林': 8}
    legend = list()
    inner_pie = list()
    out_pie = list()
    for element in data.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data[element]
        dic_tem['name'] = element
        inner_pie.append(dic_tem)
    for element in data2.keys():
        legend.append(element)
        dic_tem = {}
        dic_tem['value'] = data2[element]
        dic_tem['name'] = element
        out_pie.append(dic_tem)
    return render(request, 'test/doctor.html', {'legend': json.dumps(legend),
                                                'innerpie': json.dumps(inner_pie),
                                                'outpie': json.dumps(out_pie)})

def barthel(request):
    batthel_json = os.path.join(settings.BASE_DIR, 'json/result_pred_0626.json')
    with open(batthel_json, 'rt', encoding='utf8') as f:
        data = json.load(f)
    return render(request, 'blog/barthel.html', {'ori_data': data})
"""
def barthel(request):
    batthel_json = os.path.join(settings.BASE_DIR, 'json/result_pred_0626.json')
    with open(batthel_json, 'rt', encoding='utf8') as f:
        data = json.load(f)
    barthel = dict()
    b_data = list()
    barthel['inhosp_no'] = data['inhosp_no']
    tem_dic = dict()
    tem_dic['name'] = data['total_score']['model_name']
    tem_dic['current'] = data['total_score']['admission_score']
    tem_dic['pre'] = data['total_score']['predicted_score']
    b_data.append(tem_dic)
    tem_dic = dict()
    tem_dic['name'] = data['total_level']['model_name']
    tem_dic['current'] = data['total_level']['admission_score']
    tem_dic['pre'] = data['total_level']['predicted_score']
    b_data.append(tem_dic)
    for item in data['subitem_scores']:
        tem_dic = dict()
        tem_dic['name'] = item['model_name']
        tem_dic['current'] = item['admission_score']
        tem_dic['pre'] = item['predicted_score']
        b_data.append(tem_dic)
    barthel['data'] = b_data
    return render(request, 'blog/barthel.html', {'batthel_json': json.dumps(barthel), 'ori_data': data})
"""
def dbshow(request):
    return render(request, 'blog/dbshow.html')

def login(request):
    """
    if request.method=='POST':
        username=request.POST.get('name','')
        password=request.POST.get('password','')
        #models.API_UserInfo.objects.create(username=username,password=password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login0(request, user)
        else:
            return HttpResponse('用户名或密码错误')
    """
    return render(request, 'blog/login.html')

def regist(request):
    #if request.user.is_authenticated():
        #return HttpResponseRedirect("/index.html")
    try:
        if request.method == 'POST':
            username = request.POST.get('name', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            errors = []

            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()

            #登录前需要先验证
            new_user = auth.authenticate(username=username, password=password)
            if new_user is not None:
                auth.login(request, new_user)
                return HttpResponse('regist tt!!!')
    except Exception as e:
        return HttpResponse('some error.')
    return render(request, 'blog/register.html')

def login_verify(request): #登陆信息提交验证
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/patpanel.html')
    return HttpResponse('some error.')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login.html')

"""
def login_verify(request): #登陆信息提交验证
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = API_UserInfo.objects.all()
        for user in users:
            if user.username == username and user.password == password:
                #user_list = API_UserInfo.objects.all()
                #context = {'user_list': user_list}
                request.session['username'] = username  
                #request.session.set_expiry(600) #session的
                return HttpResponse('1')
        return HttpResponse('-1')
    else:
        return HttpResponse('0')
"""

def login_success(request):#登陆成功之后跳转的页面
    return index(request)
    """
    username = request.session['username']
    if username == '11':
        return index(request)
    else:
        return doctor(request)
    """

def verify(request):#权限判断
    username = request.session['username']
    return HttpResponse('1')
    if username == '11':
        return HttpResponse('1')
    else:
        return HttpResponse('-1')

"""
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/blog/login")
"""