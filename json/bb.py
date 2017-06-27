import json
import os

if __name__ == '__main__':
    disk = os.getcwd()
    file_path = disk + r'\json\result_pred_0626.json'
    with open(file_path, 'rt', encoding='utf8') as f:
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
