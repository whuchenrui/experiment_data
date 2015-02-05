# coding=utf-8
__author__ = 'CRay'
"""
横坐标: 页码 0, 4, 8, 12, 16 ...
纵坐标: 概率 [0, 1]
1: 统计翻页概率,  继续向后翻看的人/(停在该请求的人 + 继续向后翻看的人)
2: 统计用户分布
"""
import os
from lib import Function
from lib.Config import Config


def basic_data(st_time, end_time):
    cf = Config('data.conf')
    fin_path = cf.get('path', 'filter_data')
    chart_path = cf.get('path', 'chart_result')
    list_time = Function.get_time_list(st_time, end_time)
    dict_user_distribution = {}
    total = 0
    for day in list_time:
        folder_path = fin_path + day
        if os.path.exists(folder_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in_result = folder_path + '\\result_' + temp_name + str(i)
                if os.path.exists(file_in_result):
                    fin_result = open(file_in_result, 'r')
                    while True:
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        length = len(list_result)
                        request_num = length/36
                        if request_num not in dict_user_distribution:
                            dict_user_distribution[request_num] = 0
                        dict_user_distribution[request_num] += 1
                        total += 1
                    fin_result.close()

    req_total = 0
    for req in dict_user_distribution:
        req_total += dict_user_distribution[req]
    if req_total != total:
        print '计算出错!'
        return False

    list_user_distribution = [[0, 0]]
    list_user_prob = [[0, 1]]
    rest_cnt = total
    for req in dict_user_distribution:
        temp = round(float(dict_user_distribution[req])/total, 3)
        page = req*4
        list_user_distribution.append([page, temp])
        rest_cnt -= dict_user_distribution[req]
        if rest_cnt != 0:
            prob = 1 - float(dict_user_distribution[req])/rest_cnt
            list_user_prob.append([page, round(prob, 3)])
        else:
            list_user_prob.append([page, 0])
    name = '4-1-user-distribution_'+st_time+'_'+end_time+'.result'
    fout = open(chart_path+name, 'w')
    fout.write('user distribution: \n'+str(list_user_distribution))
    fout.write('\n\n user general turn probability: \n' + str(list_user_prob))
    fout.close()
    print 'finish ok!'
    return True