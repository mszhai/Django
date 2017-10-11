from django.shortcuts import render
from django.conf import settings

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
import blog.pdf_create as PDFCreate

import datetime
import time
import json
import os
import requests

@login_required
def print_assessment(request):
    if request.method == 'GET':
        hosp_id = request.GET.get('hospid', '')
        # 展示的数据
        pat = models.HospitalizationInfo.objects.get(id=hosp_id)
        a_pat = models.PatientInfo.objects.get(id=pat.patid_id)
        #barthel_num = pat.barthel_set.count()
        barthel_data = pat.barthel_set.all()
        barthel_data_dic = {}
        num_i = 1
        for item in barthel_data:
            barthel_data_dic['score'+str(num_i)+'0'] = item.dabian
            barthel_data_dic['score'+str(num_i)+'1'] = item.xiaobian
            barthel_data_dic['score'+str(num_i)+'2'] = item.xiushi
            barthel_data_dic['score'+str(num_i)+'3'] = item.yongce
            barthel_data_dic['score'+str(num_i)+'4'] = item.chifan
            barthel_data_dic['score'+str(num_i)+'5'] = item.zhuanyi
            barthel_data_dic['score'+str(num_i)+'6'] = item.huodong
            barthel_data_dic['score'+str(num_i)+'7'] = item.chuanyi
            barthel_data_dic['score'+str(num_i)+'8'] = item.louti
            barthel_data_dic['score'+str(num_i)+'9'] = item.xizao
            barthel_data_dic['score'+str(num_i)+'10'] = item.total_score
            adl = ''
            if 0 <= item.total_score <= 20:
                adl = '极严重功能缺陷'
            elif 25 <= item.total_score <= 45:
                adl = '严重功能缺陷'
            elif 50 <= item.total_score <= 70:
                adl = '中度功能缺陷'
            elif 75 <= item.total_score <= 95:
                adl = '轻度功能缺陷'
            elif item.total_score == 100:
                adl = 'ADL自理'
            barthel_data_dic['score'+str(num_i)+'11'] = adl
            profile = models.Profile.objects.get(id=item.profile_id)
            barthel_data_dic['score'+str(num_i)+'12'] = profile.docname
            barthel_data_dic['score'+str(num_i)+'date'] = item.evaluate_time.strftime("%Y/%m/%d")
            num_i += 1
        pat_info = {}
        #年龄
        age = int((pat.entdate - a_pat.birthday).days / 365 + 1)
        pat_info['age'] = age
        pat_info['name'] = a_pat.name
        pat_info['sex'] = a_pat.sex
        pat_info['dignose'] = pat.dignose
        pat_info['entdate'] = pat.entdate.strftime("%Y-%m-%d")
        pat_info['hospitno'] = pat.hospitno_fk

        pat_info['barthel_data'] = json.dumps(barthel_data_dic)

        # response
        now = datetime.datetime.now().strftime("-%Y%m%d")
        filename = pat.hospitno_fk + now
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename={filename}.pdf'.format(filename=filename)
        #生成pdf
        PDFCreate.barthel_temp(response, pat_info)
        return response
    return HttpResponse('出现错误，请返回重新打印！')

@login_required
def model_result(request):
    if request.method == 'GET':
        hosp_id = request.GET.get('hospid', '')
        user = User.objects.get(username=request.user)
        userid = user.id
        #从数据库获取数据
        model_rt = get_model_result(hosp_id)
        hosp_info = models.HospitalizationInfo.objects.get(id=hosp_id)
        if len(model_rt) == 0 and hosp_info.evaluate_status + 1 == 2:
            #保存api接口数据到数据库
            result_data = api_data(hosp_id, userid)
            hosp_info.evaluate_status = 2
            hosp_info.save()
            #model_rt = get_model_result(hosp_id)
        data = get_model_predic_html(hosp_id)
    return render(request, 'blog/modelresult.html', data)

def get_model_predic_html(hospid):
    """
    获取预测模型前端展示的html数据

    hospid: 住院号
    """
    model_rt = get_model_result(hospid)
    result = {'factor_html': '', 'adl': '', 'factor_p': '', 'factor_n': ''}
    factor_html = ''
    for item in model_rt:
        p = ''
        if item.name == '出院改善_大便':
            p = get_factor_html(item, '大便')
            factor_html += p
        if item.name == '出院改善_小便':
            p = get_factor_html(item, '小便')
            factor_html += p
        if item.name == '出院改善_修饰':
            p = get_factor_html(item, '修饰')
            factor_html += p
        if item.name == '出院改善_用厕':
            p = get_factor_html(item, '用厕')
            factor_html += p
        if item.name == '出院改善_吃饭':
            p = get_factor_html(item, '吃饭')
            factor_html += p
        if item.name == '出院改善_转移':
            p = get_factor_html(item, '转移')
            factor_html += p
        if item.name == '出院改善_活动':
            p = get_factor_html(item, '活动')
            factor_html += p
        if item.name == '出院改善_穿衣':
            p = get_factor_html(item, '穿衣')
            factor_html += p
        if item.name == '出院改善_上楼梯':
            p = get_factor_html(item, '上楼梯')
            factor_html += p
        #adl缺陷程度
        if item.name == '出院Barthel总分':
            result['adl'] = adl(item.prob_improve)
        if item.name == '出院缺陷程度改善':
            factor_positive = list()
            factor_negative = list()
            factor = models.ModelResultFactor.objects.filter(model_result_id=item.id)
            for factor_item in factor:
                #将入院Barthel_xx 替换为'入院Barthel评分'
                factor_name = ''
                if '入院Barthel' in factor_item.factor_name:
                    factor_name = '入院Barthel评分'
                else:
                    factor_name = factor_item.factor_name
                # 正面影响和负面影响归类
                if factor_item.is_positive:
                    factor_positive.append(factor_name)
                else:
                    factor_negative.append(factor_name)
            if len(factor_positive) != 0:
                result['factor_p'] = '、'.join(factor_positive)
            else:
                result['factor_p'] = '无'
            if len(factor_negative) != 0:
                result['factor_n'] = '、'.join(factor_negative)
            else:
                result['factor_n'] = '无'
    result['factor_html'] = mark_safe(factor_html)
    return result

def adl(total_score):
    score = total_score - total_score % 5
    if 0 <= score <= 20:
        adl = '极严重功能缺陷'
    elif 25 <= score <= 45:
        adl = '严重功能缺陷'
    elif 50 <= score <= 70:
        adl = '中度功能缺陷'
    elif 75 <= score <= 95:
        adl = '轻度功能缺陷'
    elif score == 100:
        adl = 'ADL自理'
    else:
        adl = 'error: 分数{}有误'.format(total_score)
    return adl

def get_factor_html(model_rt, name):
    p = '''
        <p>&#8226<font color="green">{name}（{percent}）</font><br>
            {p_factor}
        </p>
        '''
    factor_positive = list()
    factor_negative = list()
    factor = models.ModelResultFactor.objects.filter(model_result_id=model_rt.id)
    for factor_item in factor:
        #将入院Barthel_xx 替换为'入院Barthel评分'
        factor_name = ''
        if '入院Barthel' in factor_item.factor_name:
            factor_name = '入院Barthel评分'
        else:
            factor_name = factor_item.factor_name
        # 正面影响和负面影响归类
        if factor_item.is_positive:
            factor_positive.append(factor_name)
        else:
            factor_negative.append(factor_name)
    p_factor = ''
    if len(factor_positive) != 0 and len(factor_negative) != 0:
        p_factor = '''&nbsp&nbsp&nbsp&nbsp&#8226 对康复提升的正面影响因素包括：{p}<br>
                    &nbsp&nbsp&nbsp&nbsp&#8226 对康复提升的<font color="red">负面</font>影响因素包括：{n}'''.format(p='、'.join(factor_positive), n='、'.join(factor_negative))
    elif len(factor_positive) != 0:
        p_factor = '&nbsp&nbsp&nbsp&nbsp&#8226 对康复提升的正面影响因素包括：{p}'.format(p='、'.join(factor_positive))
    elif len(factor_negative) != 0:
        p_factor = '&nbsp&nbsp&nbsp&nbsp&#8226 对康复提升的<font color="red">负面</font>影响因素包括：{n}'.format(n='、'.join(factor_negative))
    percent = format(model_rt.prob_improve, '.1%')
    result = p.format(name=name, percent=percent, p_factor=p_factor)
    return result


def get_model_result(hospid):
    model_rt = models.ModelResult.objects.filter(hospid=hospid).order_by('-prob_improve')
    return model_rt

def api_data(hospid, userid):
    med_history = models.MedHistory.objects.get(hospid=hospid)
    barthel_info = models.Barthel.objects.filter(hospid=hospid, times=1)
    hosp_info = models.HospitalizationInfo.objects.get(id=hospid)
    pat_info = models.PatientInfo.objects.get(id=hosp_info.patid_id)
    stroke_days = (barthel_info[0].evaluate_time - med_history.stroke_time).days
    first_recover_care = 0.0
    if med_history.first_recover_care:
        first_recover_care = 1.0
    glu = 5.63
    age = int((hosp_info.entdate - pat_info.birthday).days / 365 + 1)

    barthel_dic = dict()
    barthel_dic['n1'] = barthel_info[0].dabian
    barthel_dic['n2'] = barthel_info[0].xiaobian
    barthel_dic['n3'] = barthel_info[0].xiushi
    barthel_dic['n4'] = barthel_info[0].yongce
    barthel_dic['n5'] = barthel_info[0].chifan
    barthel_dic['n6'] = barthel_info[0].zhuanyi
    barthel_dic['n7'] = barthel_info[0].huodong
    barthel_dic['n8'] = barthel_info[0].chuanyi
    barthel_dic['n9'] = barthel_info[0].louti
    barthel_dic['n10'] = barthel_info[0].total_score
    barthel_dic['n11'] = barthel_info[0].total_score

    url_pat = 'http://10.111.25.203:80/api/v1/{userid}/risk/{modelid}/{patientid}'
    modelid_list = ['_risk_model_n{}'.format(item) for item in range(1, 10)]
    modelid_list.append('_risk_model_total_level')
    modelid_list.append('_risk_model_total_score')
    barthel_part = list()
    barthel_part.append('入院Barthel_大便')
    barthel_part.append('入院Barthel_小便')
    barthel_part.append('入院Barthel_修饰')
    barthel_part.append('入院Barthel_用厕')
    barthel_part.append('入院Barthel_吃饭')
    barthel_part.append('入院Barthel_转移')
    barthel_part.append('入院Barthel_活动')
    barthel_part.append('入院Barthel_穿衣')
    barthel_part.append('入院Barthel_上楼梯')
    barthel_part.append('入院Barthel总分')
    barthel_part.append('入院Barthel总分')

    result_data = dict()
    n_i = 0
    for modelid, barthel_item in zip(modelid_list, barthel_part):
        n_i += 1
        #dict_data2 = {'prob': 0, 'bscore': 0, 'stroke': 0, 'cure': 0, 'age': 0, 'glu': 0}
        url = url_pat.format(userid=userid, modelid=modelid, patientid=hospid)
        data = []
        dic0 = {'key': barthel_item, 'value': barthel_dic['n'+str(n_i)] + 0.0}
        dic1 = {'key': '距脑卒中发病天数', 'value': stroke_days + 0.0}
        dic2 = {'key': '首次治疗', 'value': first_recover_care}
        dic3 = {'key': '年龄', 'value': age + 0.0}
        dic4 = {'key': 'GLU', 'value': glu}
        data = [dic0, dic1, dic2, dic3, dic4]
        data_json = json.dumps(data, ensure_ascii=False)#, ensure_ascii=False
        data_json = data_json.encode('utf8')
        result = requests.post(url, data_json)
        result_text = result.text
        result_json = json.loads(result_text)
        if 'error_message' in result_json.keys():
            result_data['n'+str(n_i)] = result_json['error_message']
            #return {'error_message': result_json['error_message']}
        elif 'model_id' in result_json.keys():
            m_result = models.ModelResult()
            m_result.hospid = hosp_info
            m_result.m_id = result_json['model_id']
            m_result.name = result_json['model_name']
            if 'predicted_score' in result_json.keys():
                m_result.prob_improve = result_json['predicted_score']
                result_data['n'+str(n_i)] = result_json['predicted_score']
            else:
                m_result.prob_improve = result_json['probability_of_improvement']
                result_data['n'+str(n_i)] = result_json['probability_of_improvement']
            m_result.save()
            for item in result_json['influencing_factors']:
                m_r_factor = models.ModelResultFactor()
                m_r_factor.model_result_id = m_result
                m_r_factor.ci_high = item['ci_high']
                m_r_factor.ci_low = item['ci_low']
                m_r_factor.factor_name = item['factor_name']
                m_r_factor.is_positive = item['is_positive']
                if 'predicted_score' in result_json.keys():
                    m_r_factor.odds_ratio = item['coefficient']
                else:
                    m_r_factor.odds_ratio = item['odds_ratio']
                m_r_factor.p_value = item['p_value']
                m_r_factor.save()
    return result_data

@login_required
def modelpara(request):
    if request.method == 'POST':
        medhistory = models.MedHistory()
        hosp_id = request.POST.get('hospid', '')
        stroke_time = request.POST.get('stroke_time', '')
        if stroke_time:
            stroke_time = time.strptime(stroke_time, "%Y-%m-%d")
            stroke_time = datetime.datetime(* stroke_time[:3])
        else:
            return HttpResponse('-1')
        radio1 = request.POST.get('radio1', '')
        radio2 = request.POST.get('radio2', '')
        radio3 = request.POST.get('radio3', '')
        radio4 = request.POST.get('radio4', '')
        radio6 = request.POST.get('radio6', '')
        radio7 = request.POST.get('radio7', '')
        #radio5 = request.POST.get('radio5', '')
        radio5 = '失效'

        if not (radio1 or radio2 or radio3 or radio4 or radio5 or radio6 or radio7):
            return HttpResponse('-1')

        glu = request.POST.get('glu', '')
        tg = request.POST.get('tg', '')
        ldl_c = request.POST.get('ldl_c', '')

        #获取住院号
        hospinfo = models.HospitalizationInfo.objects.get(id=hosp_id)
        medhistory.hospid = hospinfo
        medhistory.stroke_time = stroke_time
        medhistory.conservative_treatment = radio4
        medhistory.first_recover_care = radio1
        medhistory.diabetes = radio3
        medhistory.hypertension = radio2
        medhistory.smoke = radio6
        medhistory.drink = radio7
        medhistory.dignose = radio5
        if glu:
            medhistory.glu = glu
        if tg:
            medhistory.tg = tg
        if ldl_c:
            medhistory.ldl_c = ldl_c
        medhistory.save()
        return HttpResponse('1')


@login_required
def predict_model(request):
    if request.method == 'POST':
        hosp_id = request.POST.get('hospid', '')
        barthel = models.Barthel.objects.filter(hospid=hosp_id, times=1)
        if len(barthel) == 0:
            return HttpResponse('-2')
        med_history = models.MedHistory.objects.filter(hospid=hosp_id)
        if med_history:
            return HttpResponse('2')
        return HttpResponse('1')
    return HttpResponse('-1')

@login_required
def predictbar(request):
    if request.method == 'GET':
        hosp_id = request.GET.get('hospid', '')
        pat = models.HospitalizationInfo.objects.get(id=hosp_id)
        a_pat = models.PatientInfo.objects.get(id=pat.patid_id)
        pat_info = {}
        barthel_num = pat.barthel_set.count()
        barthel_data = pat.barthel_set.all()
        barthel_data_dic = {}
        num_i = 1
        for item in barthel_data:
            barthel_data_dic['score'+str(num_i)+'0'] = item.dabian
            barthel_data_dic['score'+str(num_i)+'1'] = item.xiaobian
            barthel_data_dic['score'+str(num_i)+'2'] = item.xiushi
            barthel_data_dic['score'+str(num_i)+'3'] = item.yongce
            barthel_data_dic['score'+str(num_i)+'4'] = item.chifan
            barthel_data_dic['score'+str(num_i)+'5'] = item.zhuanyi
            barthel_data_dic['score'+str(num_i)+'6'] = item.huodong
            barthel_data_dic['score'+str(num_i)+'7'] = item.chuanyi
            barthel_data_dic['score'+str(num_i)+'8'] = item.louti
            barthel_data_dic['score'+str(num_i)+'9'] = item.xizao
            barthel_data_dic['score'+str(num_i)+'10'] = item.total_score
            adl = ''
            if 0 <= item.total_score <= 20:
                adl = '极严重功能缺陷'
            elif 25 <= item.total_score <= 45:
                adl = '严重功能缺陷'
            elif 50 <= item.total_score <= 70:
                adl = '中度功能缺陷'
            elif 75 <= item.total_score <= 95:
                adl = '轻度功能缺陷'
            elif item.total_score == 100:
                adl = 'ADL自理'
            barthel_data_dic['score'+str(num_i)+'11'] = adl
            profile = models.Profile.objects.get(id=item.profile_id)
            barthel_data_dic['score'+str(num_i)+'12'] = profile.docname
            barthel_data_dic['score'+str(num_i)+'date'] = item.evaluate_time.strftime("%Y-%m-%d")
            num_i += 1
        item_probability = pat.modelresult_set.all()
        for item in item_probability:
            prob = format(item.prob_improve, '.1%')
            if item.name == '出院改善_大便':
                barthel_data_dic['score50'] = prob
            if item.name == '出院改善_小便':
                barthel_data_dic['score51'] = prob
            if item.name == '出院改善_修饰':
                barthel_data_dic['score52'] = prob
            if item.name == '出院改善_用厕':
                barthel_data_dic['score53'] = prob
            if item.name == '出院改善_吃饭':
                barthel_data_dic['score54'] = prob
            if item.name == '出院改善_转移':
                barthel_data_dic['score55'] = prob
            if item.name == '出院改善_活动':
                barthel_data_dic['score56'] = prob
            if item.name == '出院改善_穿衣':
                barthel_data_dic['score57'] = prob
            if item.name == '出院改善_上楼梯':
                barthel_data_dic['score58'] = prob
                barthel_data_dic['score59'] = ''
            #adl缺陷程度
            if item.name == '出院Barthel总分':
                barthel_data_dic['score510'] = round(item.prob_improve, 1)
            if item.name == '出院缺陷程度改善':
                barthel_data_dic['score511'] = prob
        #年龄
        age = int((pat.entdate - a_pat.birthday).days / 365 + 1)
        pat_info['age'] = age
        pat_info['name'] = a_pat.name
        pat_info['sex'] = a_pat.sex
        pat_info['dignose'] = pat.dignose
        pat_info['entdate'] = pat.entdate.strftime("%Y/%m/%d")
        pat_info['hospitno'] = pat.hospitno_fk

        pat_info['hospid'] = pat.id
        pat_info['barthel_num'] = barthel_num
        pat_info['barthel_data'] = json.dumps(barthel_data_dic)
    return render(request, 'blog/predictbar.html', pat_info)

@login_required
def predictdoc(request):
    return render(request, 'blog/predictdoc.html')

@login_required
def add_model_para(request):
    if request.method == 'GET':
        hosp_id = request.GET.get('hospid', '')
        para = dict()
        para['hospid'] = hosp_id
    return render(request, 'blog/addmodelpara.html', para)

@login_required
def evaluate_submit(request):
    if request.method == 'POST':
        dic = request.POST.get('dic', '')
        dic = json.loads(dic)

        #获取关联医生，barthel评分者
        user = User.objects.get(username=request.user)
        doc = models.Profile.objects.get(user_id=user.id)
        #获取住院号
        hospinfo = models.HospitalizationInfo.objects.get(id=dic['hospid'])
        #获取barthel的评分次数
        barthel_num = hospinfo.barthel_set.count()
        if barthel_num + 1 == dic['barthel_num']:
            # 将病人状态由2改为3，条件为：病人状态为2（保证有康复预测）且第3次提交barthel评分。
            if barthel_num + 1 == 3:
                hospinfo.evaluate_status = 3
                hospinfo.save()
            barthel = models.Barthel()
            barthel.profile = doc
            barthel.hospid = hospinfo
            barthel.dabian = dic['score0']
            barthel.xiaobian = dic['score1']
            barthel.xiushi = dic['score2']
            barthel.yongce = dic['score3']
            barthel.chifan = dic['score4']
            barthel.zhuanyi = dic['score5']
            barthel.huodong = dic['score6']
            barthel.chuanyi = dic['score7']
            barthel.louti = dic['score8']
            barthel.xizao = dic['score9']
            barthel.total_score = dic['score10']
            barthel.times = dic['barthel_num']
            barthel.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    return HttpResponse('-1')

@login_required
def evaluate(request):
    if request.method == 'GET':
        hosp_id = request.GET.get('hospid', '')
        pat = models.HospitalizationInfo.objects.get(id=hosp_id)
        a_pat = models.PatientInfo.objects.get(id=pat.patid_id)
        barthel_num = pat.barthel_set.count()
        barthel_data = pat.barthel_set.all()
        barthel_data_dic = {}
        num_i = 1
        for item in barthel_data:
            barthel_data_dic['score'+str(num_i)+'0'] = item.dabian
            barthel_data_dic['score'+str(num_i)+'1'] = item.xiaobian
            barthel_data_dic['score'+str(num_i)+'2'] = item.xiushi
            barthel_data_dic['score'+str(num_i)+'3'] = item.yongce
            barthel_data_dic['score'+str(num_i)+'4'] = item.chifan
            barthel_data_dic['score'+str(num_i)+'5'] = item.zhuanyi
            barthel_data_dic['score'+str(num_i)+'6'] = item.huodong
            barthel_data_dic['score'+str(num_i)+'7'] = item.chuanyi
            barthel_data_dic['score'+str(num_i)+'8'] = item.louti
            barthel_data_dic['score'+str(num_i)+'9'] = item.xizao
            barthel_data_dic['score'+str(num_i)+'10'] = item.total_score
            adl = ''
            if 0 <= item.total_score <= 20:
                adl = '极严重功能缺陷'
            elif 25 <= item.total_score <= 45:
                adl = '严重功能缺陷'
            elif 50 <= item.total_score <= 70:
                adl = '中度功能缺陷'
            elif 75 <= item.total_score <= 95:
                adl = '轻度功能缺陷'
            elif item.total_score == 100:
                adl = 'ADL自理'
            barthel_data_dic['score'+str(num_i)+'11'] = adl
            profile = models.Profile.objects.get(id=item.profile_id)
            barthel_data_dic['score'+str(num_i)+'12'] = profile.docname
            barthel_data_dic['score'+str(num_i)+'date'] = item.evaluate_time.strftime("%Y/%m/%d")
            num_i += 1
        pat_info = {}
        #年龄
        age = int((pat.entdate - a_pat.birthday).days / 365 + 1)
        pat_info['age'] = age
        pat_info['name'] = a_pat.name
        pat_info['sex'] = a_pat.sex
        pat_info['dignose'] = pat.dignose
        pat_info['entdate'] = pat.entdate.strftime("%Y/%m/%d")
        pat_info['hospitno'] = pat.hospitno_fk

        pat_info['hospid'] = pat.id
        pat_info['barthel_num'] = barthel_num
        pat_info['barthel_data'] = json.dumps(barthel_data_dic)
        now = {}
        now['current_time'] = datetime.datetime.now().strftime("%Y/%m/%d")
        pat_info['current_time'] = json.dumps(now)
        #已经调用接口康复预测过
        have_data = get_model_result(hosp_id)
        pat_info['have_data'] = False
        if have_data:
            pat_info['have_data'] = True
    return render(request, 'blog/evaluate.html', pat_info)

@login_required
def add_patient(request):
    if request.method == 'POST':
        hospitno = request.POST.get('hospitno', '')
        patname = request.POST.get('patname', '')
        sex_t = request.POST.get('sex', '')
        sex = ''
        if sex_t == '0':
            sex = '男'
        elif sex_t == '1':
            sex = '女'
        birthday = request.POST.get('birthday', '')
        dignose_t = request.POST.get('dignose', '')
        dignose = ''
        if dignose_t == '0':
            dignose = '脑梗死'
        elif dignose_t == '1':
            dignose = '脑出血'
        elif dignose_t == '2':
            dignose = '蛛网膜下腔出血'
        if (hospitno is '') or (patname is '') or (sex is '') or (birthday is '') or (dignose is ''):
            return HttpResponse('-1')
        birthday = time.strptime(birthday, "%Y-%m-%d")
        birthday = datetime.datetime(* birthday[:3])

        patinfo = models.PatientInfo()
        patinfo.name = patname
        patinfo.sex = sex
        patinfo.birthday = birthday
        patinfo.save()

        hospinfo = models.HospitalizationInfo()
        hospinfo.hospitno_fk = hospitno
        hospinfo.dignose = dignose
        hospinfo.patid = patinfo
        user = User.objects.get(username=request.user)
        doc = models.Profile.objects.get(user_id=user.id)
        hospinfo.doctor = doc
        hospinfo.entdate = datetime.datetime.now()
        hospinfo.save()
        return HttpResponse('1')
        #return HttpResponseRedirect('/patpanel.html')
        #return render(request, 'blog/patpanel.html')
    return render(request, 'blog/addpatient.html')

@login_required
def pat_panel(request):
    user = User.objects.get(username=request.user)
    role = models.Profile.objects.get(user_id=user.id)
    page_html = ''
    pat_panel = '''
    <div class="col-lg-3 col-sm-3">
        <div class="panel panel-{evaluate_status_style}">
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
                {evaluate1}
                {barthel_bar}
                {check1}
            </div>
        </div>
    </div>
    <!-- /.col-lg-3 -->
    '''
    
    if role.group == 'doctor':#in=[role.id]
        #去掉999999，需要确保病人都有对应的医生
        patients = models.HospitalizationInfo.objects.filter(doctor__in=[role.id]).order_by('evaluate_status')
        for pat in patients:
            a_patient = models.PatientInfo.objects.get(id=pat.patid_id)
            age = int((pat.entdate - a_patient.birthday).days / 365 + 1)
            evaluate_status = pat.evaluate_status
            evaluate1 = '<a style="cursor:pointer" onclick="evaluate1({patid1})"><i class="fa fa-link"></i> 评定</a>'
            check1 = '<a style="cursor:pointer" onclick="check1({patid2}, {e_status})"><i class="fa fa-link"></i> 分析结果</a>'
            barthel_bar = '<a style="cursor:pointer" onclick="barthel_bar({patid1})"><i class="fa fa-link"></i> 量表</a>'
            evaluate1 = evaluate1.format(patid1=pat.id)
            barthel_bar = barthel_bar.format(patid1=pat.id)
            if evaluate_status == 2:
                check1 = check1.format(patid2=pat.id, e_status=2)
                page_html += pat_panel.format(name=a_patient.name, hospno=pat.hospitno_fk, sex=a_patient.sex, age=age, dignose=pat.dignose, evaluate1=evaluate1, barthel_bar='', check1=check1, evaluate_status_style='danger')
            elif evaluate_status == 3:
                check1 = check1.format(patid2=pat.id, e_status=3)
                page_html += pat_panel.format(name=a_patient.name, hospno=pat.hospitno_fk, sex=a_patient.sex, age=age, dignose=pat.dignose, evaluate1='', barthel_bar=barthel_bar, check1=check1, evaluate_status_style='warning')
            else:
                page_html += pat_panel.format(name=a_patient.name, hospno=pat.hospitno_fk, sex=a_patient.sex, age=age, dignose=pat.dignose, evaluate1=evaluate1, barthel_bar='', check1='', evaluate_status_style='info')
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
            docname = request.POST.get('docname', '')
            errors = []

            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            profile = models.Profile()
            profile.user = user
            profile.phone = '12121212'
            profile.docname = docname
            profile.save()

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
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            #return HttpResponseRedirect('/patpanel.html')
            return HttpResponse('1')
        return HttpResponse('-1')
    return HttpResponse('-1')

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