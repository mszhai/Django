data = {'Clinical': 90,'Non-clinical': 54,'Treatment': 33}
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
    inner_pie.append(dic_tem)