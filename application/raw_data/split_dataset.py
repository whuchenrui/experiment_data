# coding=utf-8
__author__ = 'CRay'

import os
from lib.Config import Config
from lib import Function


def split_dataset(st_time, end_time):
    cf_data = Config('data.conf')
    fin_path = cf_data.get('path', 'filter_data')
    view_path = cf_data.get('path', 'view_data')
    save_path = cf_data.get('path', 'save_data')

    list_time = Function.get_time_list(st_time, end_time)
    view_cnt = 0
    save_cnt = 0
    for day in list_time:
        input_path = fin_path + day
        view_output_path = view_path + day
        save_output_path = save_path + day
        if not os.path.exists(view_output_path):
            os.mkdir(view_output_path)
        if not os.path.exists(save_output_path):
            os.mkdir(save_output_path)
        if os.path.exists(input_path):
            for i in range(0, 24):
                temp_name = ''
                if i < 10:
                    temp_name = '0'
                file_in_pic = input_path + '\\pic_' + temp_name + str(i)
                file_in_result = input_path + '\\result_' + temp_name + str(i)
                if os.path.exists(file_in_result):
                    file_view_pic = view_output_path + '\\pic_' + temp_name + str(i)
                    file_view_result = view_output_path + '\\result_' + temp_name + str(i)
                    file_save_pic = save_output_path + '\\pic_' + temp_name + str(i)
                    file_save_result = save_output_path + '\\result_' + temp_name + str(i)
                    fout_view_pic = open(file_view_pic, 'w')
                    fout_view_result = open(file_view_result, 'w')
                    fout_save_pic = open(file_save_pic, 'w')
                    fout_save_result = open(file_save_result, 'w')

                    fin_pic = open(file_in_pic, 'r')
                    fin_result = open(file_in_result, 'r')
                    while True:
                        line_pic = fin_pic.readline()
                        line_result = fin_result.readline()
                        if not line_result:
                            break
                        list_result = line_result.strip('\n').strip(' ').split(' ')
                        for index, item in enumerate(list_result):
                            list_result[index] = int(item)
                        if 2 in list_result:   # 有2的则为save, 没有则全为view
                            fout_save_pic.write(line_pic)   # 这里直接输出line, 而line中有换行符, 所以这里不用显示输出'\n'
                            fout_save_result.write(line_result)
                            save_cnt += 1
                        else:
                            fout_view_pic.write(line_pic)
                            fout_view_result.write(line_result)
                            view_cnt += 1
                    fout_view_pic.close()
                    fout_view_result.close()
                    fout_save_pic.close()
                    fout_save_result.close()
                    fin_pic.close()
                    fin_result.close()
        print 'split ', day
    print 'view: ', str(view_cnt)
    print 'save: ', str(save_cnt)
