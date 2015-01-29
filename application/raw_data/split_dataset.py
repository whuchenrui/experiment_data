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
                file_in = input_path + '\\full_' + temp_name + str(i)
                if os.path.exists(file_in):
                    file_view = view_output_path + '\\full_' + temp_name + str(i)
                    file_save = save_output_path + '\\full_' + temp_name + str(i)
                    fout_view = open(file_view, 'w')
                    fout_save = open(file_save, 'w')

                    fin = open(file_in, 'r')
                    while True:
                        line = fin.readline()
                        if not line:
                            break
                        dict_line = eval(line)
                        list_result = dict_line['result']
                        if 2 in list_result:   # 有2的则为save, 没有则全为view
                            fout_save.write(line)   # 这里直接输出line, 而line中有换行符, 所以这里不用显示输出'\n'
                            save_cnt += 1
                        else:
                            fout_view.write(line)
                            view_cnt += 1
                    fout_view.close()
                    fout_save.close()
                    fin.close()
        print 'finish ', day
    print 'view: ', str(view_cnt)
    print 'save: ', str(save_cnt)
