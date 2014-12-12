# coding=utf-8
__author__ = 'CRay'

import codecs
from ConfigParser import ConfigParser
""" 画scatter图，证明图片质量有差别 """


def quality(_type):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    source_path = cf.get('dataset', 'path')
    action = int(cf.get('type', 'type'))

    if _type == 'save':
        name = 'result_raw'
        name2 = 'pic_raw'
    else:
        name = 'result'
        name2 = 'pic'

    fin_result = codecs.open(source_path+name, 'r', encoding='UTF-8')
    fin_pic = codecs.open(source_path+name2, 'r', encoding='UTF-8')

    dict_result = {}  # {0:{pic: [1, 2]}}  list值[点击数量, 出现的次数]
    while True:
        line_result = fin_result.readline()
        line_pic = fin_pic.readline()
        if not line_result:
            break
        result = line_result.strip('\n').split(' ')
        picture = line_pic.strip('\n').split(' ')
        length = len(result)
        requests = length/36
        for index, item in enumerate(result):
            result[index] = int(item)
        for req in range(1, requests+1):
            page = req*4 - 3
            if page not in dict_result:
                dict_result[page] = {}
            for j in range((page-1)*9, page*9):  # 计算指定请求的点击情况
                pic = picture[j]
                if pic not in dict_result[page]:
                    dict_result[page][pic] = [0, 0]
                if result[j] > action:
                    dict_result[page][pic][0] += 1
                dict_result[page][pic][1] += 1
    print_result(dict_result)
    fin_result.close()
    fin_pic.close()


def print_result(result):
    cf = ConfigParser()
    cf.read('..\\config\\data.conf')
    chart_data = cf.get('dataset', 'chart')
    output = []
    for page in result:
        temp = result[page]
        num = len(temp)
        num *= 0.1  # 选取呈现量为前10%的数据
        num = int(num)
        tuple_sorted = sorted(temp.items(), key=lambda d: d[1][1], reverse=True)
        # [(1, [1, 4]), (2, [2, 5])]
        tuple_sorted = tuple_sorted[0: num]
        for j in range(0, num):
            if tuple_sorted[j][1][1] < 100:
                continue
            click_cnt = tuple_sorted[j][1][0]
            show_cnt = tuple_sorted[j][1][1]
            probability = round(float(click_cnt)/show_cnt, 3)
            output.append([page, probability])
    fout = codecs.open(chart_data+'pic_position.log', 'w', encoding='UTF-8')
    output_str = str(output)
    fout.write(output_str)
    fout.close()


# if __name__ == '__main__':
#     quality()