# coding=utf-8
__author__ = 'CRay'

"""
画scatter图，证明图片质量有差别
dict_pic_quality:  {page1: {pic: [show, click], ....}, page2: {pic: [show, click]...}}
"""
import os
from lib import Function
from lib.Config import Config


def quality(st_time, end_time, min_show):
    cf = Config('data.conf')
    fin_path = cf.get('path', 'filter_data')
    chart_path = cf.get('path', 'chart_result')
    list_time = Function.get_time_list(st_time, end_time)
    dict_pic_quality = {}
    for day in list_time:
        folder_path = fin_path + day
        if os.path.exists(folder_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in_pic = folder_path + '\\pic_' + temp_name + str(i)
                file_in_result = folder_path + '\\result_' + temp_name + str(i)
                if os.path.exists(file_in_result):
                    fin_result = open(file_in_result, 'r')
                    fin_pic = open(file_in_pic, 'r')
                    while True:
                        line_result = fin_result.readline()
                        line_pic = fin_pic.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        list_pic = line_pic.strip('\n').strip(' ').split(' ')
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        length = len(list_result)
                        request_num = length/36
                        for j in range(1, 5):
                            if j not in dict_pic_quality:
                                dict_pic_quality[j] = {}
                            for k in range((j-1)*9, j*9):
                                pic = list_pic[k]
                                if pic not in dict_pic_quality[j]:
                                    dict_pic_quality[j][pic] = [0, 0]
                                if list_result[k] >= 1:
                                    dict_pic_quality[j][pic][1] += 1
                                dict_pic_quality[j][pic][0] += 1
                        for j in range(2, request_num+1):
                            page = j*4 - 3
                            if page not in dict_pic_quality:
                                dict_pic_quality[page] = {}
                            for k in range((page-1)*9, page*9):
                                pic = list_pic[k]
                                if pic not in dict_pic_quality[page]:
                                    dict_pic_quality[page][pic] = [0, 0]
                                if list_result[k] >= 1:
                                    dict_pic_quality[page][pic][1] += 1
                                dict_pic_quality[page][pic][0] += 1
                    fin_result.close()
                    fin_pic.close()

    list_output = []
    for page in dict_pic_quality:
        if page <= 80:
            for pic in dict_pic_quality[page]:
                info = dict_pic_quality[page][pic]
                if info[0] >= min_show:
                    prob = float(info[1])/info[0]
                    list_output.append([page, round(prob, 3)])
    name = '4-1-pic-quality_'+st_time+'_'+end_time+'.result'
    fout = open(chart_path+name, 'w')
    output_str = str(list_output)
    fout.write('图片质量: \n\n'+output_str)
    fout.close()


# if __name__ == '__main__':
#     quality()