# -*- coding: utf-8 -*- 
#字体库
import reportlab.lib.fonts

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph

import json
import os
from django.conf import settings

def barthel_temp(response, pat_info):
    age = pat_info['age']
    name = pat_info['name']
    sex = pat_info['sex']
    dignose = pat_info['dignose']
    entdate = pat_info['entdate']
    outdate = ' &nbsp &nbsp '
    bingcheng = ' &nbsp '
    fallowupdate = ' &nbsp &nbsp '
    hospitno = pat_info['hospitno']

    barthel_data = json.loads(pat_info['barthel_data'])
    #字体
    simsun = os.path.join(settings.BASE_DIR, 'json/simsun.ttc')
    pdfmetrics.registerFont(TTFont('hei', simsun))
    #展示的内容
    content = []
    styleSheet = getSampleStyleSheet()
    normalStyle = styleSheet['Normal']
    doc = SimpleDocTemplate(response, pagesize=A4)
    #title
    title = '<para autoLeading="off" fontSize=15 align=center><b><font face="hei">复旦大学附属华山医院康复医学中心</font></b><br/><br/><br/></para>'
    content.append(Paragraph(title, normalStyle))
    #副标题 Barthel指数量表
    title2 = '<para autoLeading="off" fontSize=15 align=center><b><b><font face="hei">Barthel指数量表</font></b></b><br/><br/></para>'
    content.append(Paragraph(title2, normalStyle))

    #detail
    detail1 = '<font face="hei">姓名 <u> &nbsp {name} &nbsp </u>性别 <u> &nbsp {sex} &nbsp</u>年龄 <u>&nbsp {age} &nbsp </u> 疾病 <u> &nbsp {dignose} &nbsp  </u> 病程 <u> &nbsp {bingcheng} &nbsp  </u></font><br/>'
    detail2 = '<font face="hei">住院号 <u>{hospitno} &nbsp  </u> 入院时间 <u>&nbsp  {entdate} &nbsp  </u> 出院时间 <u>&nbsp  {outdate} &nbsp  </u> 随访时间 <u> &nbsp {fallowupdate} &nbsp </u></font><br/><br/>'
    detail1 = detail1.format(name=name, sex=sex, age=age, dignose=dignose, bingcheng=bingcheng)
    detail2 = detail2.format(hospitno=hospitno, entdate=entdate, outdate=outdate, fallowupdate=fallowupdate)
    content.append(Paragraph(detail1, normalStyle))
    content.append(Paragraph(detail2, normalStyle))
    #table_td_1_1 = Paragraph('<b><font face="hei" color=red>项目</font></b>', styleSheet["BodyText"])
    #量表主题内容
    data_1 = ''
    batthel_json = os.path.join(settings.BASE_DIR, 'json/barthel_temp.json')
    with open(batthel_json, 'rt', encoding='utf8') as f:
        data_1 = json.load(f)
    data = []
    data_temp2 = data_1['content']
    row_b = 0
    for key in data_temp2:
        row = []
        value = data_temp2[key]
        column_b = 0
        for item in value:
            if row_b == 0 and column_b == 2:
                item = item.format(barthel_data.get('score1date', ' &nbsp '), barthel_data.get('score2date', ' &nbsp '), barthel_data.get('score3date', ' &nbsp '))
            elif column_b > 1:
                item = item.format(barthel_data.get('score'+str(column_b-1)+str(row_b-1), ''))
            temp1 = Paragraph(item, normalStyle)
            row.append(temp1)
            column_b += 1
        data.append(row)
        row_b += 1

    # 计算列宽
    pwidth = (doc.pagesize[0]-20)/1000
    width = 84
    colwidths = (None, None, pwidth*width, pwidth*width, pwidth*width)
    t = Table(data, colWidths=colwidths)
    t.setStyle(TableStyle([
        ('SPAN', (2,0), (4,0)),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN', (0,1), (0,-1), 'TOP'),
        #('ALIGNMENT', (0,0), (-1,-1), 'CENTER'),
        #('VALIGN', (2,1), (-1,-1),'MIDDLE'),
        ('VALIGN', (0,0), (-1,-1),'MIDDLE'),
        #('ALIGN', (0,0), (4,0),'RIGHT'),
        ('GRID', (0,0), (-1,-1), 1.1, colors.black),
        ('BOX', (0,0), (-1,-1), 1.1, colors.black),
        ]))

    #t._argW[3]=1.5*inch
    content.append(t)
    #adl
    adl = '<br\><font face="hei">*ADL 能力缺陷程度：0~20=极严重功能缺陷；25~45=严重功能缺陷；50~70=中度功能缺陷；<br\>75~95=轻度功能缺陷；100=ADL 自理</font><br\>'
    content.append(Paragraph(adl, normalStyle))
    doc.build(content)


if __name__ == "__main__":
    barthel_temp()