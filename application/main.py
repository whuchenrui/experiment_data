# coding=utf-8
__author__ = 'CRay'
import traceback
from application.raw_data import filter_dataset, split_dataset
from application.draw_charts import page_positon_bais, turn_probability, basic_data, picture_quality
from application.evaluation import init_db, draw_evaluation
from datetime import datetime
from lib.Config import Config


def exec_dataset(st_time, end_time):
    try:
        line_cnt = filter_dataset.count_seq_info(st_time, end_time)
        valid_cnt = filter_dataset.filter_data(st_time, end_time)
        print '去0剩余记录： ' + str(line_cnt) + '条'
        print '过滤后保留记录： ' + str(valid_cnt) + '条'
        split_dataset.split_dataset(st_time, end_time)
    except:
        print traceback.format_exc()


def draw_chart(st_time, end_time, behavior):
    try:
        picture_quality.quality(st_time, end_time, 500)
        # basic_data.basic_data(st_time, end_time)
        # page_positon_bais.position_bias(st_time, end_time, behavior)         # page的postion图
        # print 'Page position bias finish !'
        # turn_probability.turn_probability(st_time, end_time, behavior, 3, 15, 2, 0, 20)
        # print 'Turn probability with last 8 pages finish !'
    except:
        print traceback.format_exc()


def exec_evaluation(train_st, train_end, pic_num, test_st, test_end, page_num):
    draw_evaluation.draw_evaluation(train_st, train_end, pic_num, test_st, test_end, page_num)


if __name__ == '__main__':
    Select_dataset = 'all'  # view 对应 view数据集,  save对应save数据集   all 对应所有数据集
    Train_st_time = '2014-11-07'
    Train_end_time = '2014-11-11'
    K = 1500  # 图片集合个数
    Test_st_time = '2014-11-12'
    Test_end_time = '2014-11-16'
    L = 40  # 展现的页码
    for pic_number in [2000]:
        exec_evaluation(Train_st_time, Train_end_time, pic_number, Test_st_time, Test_end_time, L)
    # draw_chart(Train_st_time, Train_end_time, Select_dataset)