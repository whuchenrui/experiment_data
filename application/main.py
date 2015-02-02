# coding=utf-8
__author__ = 'CRay'
import traceback
from application.raw_data import filter_dataset
from application.raw_data import split_dataset
from application.draw_charts import page_positon_bais, turn_probability
from application.evaluation import init_db


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
        page_positon_bais.position_bias(st_time, end_time, behavior)         # page的postion图
        print 'Page position bias finish !'
        turn_probability.turn_probability(st_time, end_time, behavior, 3, 15, 2, 0, 20)
        print 'Turn probability with last 8 pages finish !'
    except:
        print traceback.format_exc()


def exec_evaluation(st_time, end_time, ):
    init_db.count_pic_info(st_time, end_time, 50)   # 最后一个删除呈现次数过少的信息


if __name__ == '__main__':
    Select_dataset = 'save'  # view 对应 view数据集,  save对应save数据集   all 对应所有数据集
    St_time = '2014-11-04'
    End_time = '2014-12-14'
    # exec_dataset(St_time, End_time)
    # draw_chart(St_time, End_time, Select_dataset)
    exec_evaluation(St_time, End_time)
    # main_filter_data(27, act_type)
    # main_pic_click(27, act_type)
    # main_turn_probability(act_type)
    # link_hour('2014-11-03', '2014-11-24', 27, 5)  # 开始日期, 结束日期, 统计27*4页内的信息, 至少出现的页码数
