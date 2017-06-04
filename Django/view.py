# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
import json
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def test(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'test01.html', context)

def echarts(request):
    data_y = ['销售KA一部(高媛_京_销售经理)', '销售KA二部(李天明_京_销售主管)', '销售KA三部(刘扬_京_销售)', '销售精英一部(余姗姗_京_销售经理)', '销售精英二部(王凯_京_销售经理)', '销售精英三部(王欣_京_销售主管)', '销售精英四部(过成伟_京_销售)', '销售精英五部(王昆仑_京_销售)', '销售成长一部(王睿_京_销售经理)', '销售成长二部(尹龙君_京_销售主管)', '销售成长三部(张璐璐_京_销售经理)', '销售成长四部(刘倩_京_销售主管)', '销售成长五部(袁野_京_销售主管)', '销售成长七部(朱志明_京_销售主管)', '销售成长八部(丁世超_京_销售主管)', '销售成长九部(李艳丽_京_销售经理)', '销售成长十一部(孔繁星_京_销售经理)', '销售成长十二部(郄一潇_京_销售主管)', '销售成长十三部(孙媛媛_京_销售主管)', '销售成长十四部(陈焕锋_京_销售主管)',
            '销售成长十五部(王春艳_京_销售主管)', '销售成长十七部(陈爽_京_销售)', '销售成长十八部(杨婷婷_京_销售经理)', '销售培训一部(任源夏_京_销售经理)', '销售培训二部(张腾_京_销售)', '销售培训三部(张春燕_京_销售)', '销售培训四部(赵妍妍_京_销售主管)', '销售培训五部(吴功利_京_销售)', '销售培训六部(刘明_京_销售主管)', '销售培训七部(刘惠娟_京_销售主管)', '销售培训八部(唐景云_京_销售主管)']
    data_x = [3786.5, 3317.6, 2754.8, 2114.2 ,917.1, 1185.1, 1365.3, 2251.7, 627.8, 341.5, 655.0, 553.7, 733.5, 467.6,
            571.9, 590.8, 504.5, 346.7, 389.8, 539.1, 654.5, 581.4, 38.0, 19.4, 46.4, 7.7, 27.8, 22.2, 36.3, 26.1, 38.1]
    return render(request, 'echarts.html', {'dataY': json.dumps(data_y),
                                            'dataX': json.dumps(data_x)})

def pie(request):
    return render(request, 'pie.html')

def test02(request):
    return render(request, 'test02.html')