# coding=utf-8
__author__ = 'CRay'
import traceback
from application.raw_data import filter_dataset, split_dataset
from application.draw_charts import page_positon_bais, turn_probability, basic_data, picture_quality
from application.evaluation import init_db, draw_evaluation
from datetime import datetime


def exec_dataset(st_time, end_time):
    try:
        line_cnt = filter_dataset.count_seq_info(st_time, end_time)
        valid_cnt = filter_dataset.filter_data(st_time, end_time)
        print '去0剩余记录： ' + str(line_cnt) + '条'
        print '过滤后保留记录： ' + str(valid_cnt) + '条'
        split_dataset.split_dataset(st_time, end_time)
    except:
        print traceback.format_exc()


def draw_chart(st_time, end_time, behavior, max_req):
    try:
        picture_quality.quality(st_time, end_time, 500)
        basic_data.basic_data(st_time, end_time)
        page_positon_bais.position_bias(st_time, end_time, behavior, max_req)         # page的postion图
        print 'Page position bias finish !'
        turn_probability.turn_probability(st_time, end_time, behavior, 8, 60, 8, 0, 20)
        print 'Turn probability with last 8 pages finish !'
    except:
        print traceback.format_exc()


def exec_evaluation(behavior, train_st, train_end, pic_num, test_st, test_end, page_num, data2, data3):
    draw_evaluation.draw_evaluation(behavior, train_st, train_end, pic_num, test_st, test_end, page_num, data2, data3)


if __name__ == '__main__':
    Train_st_time = '2014-11-04'
    Train_end_time = '2014-11-05'

    Test_st_time = '2014-11-04'
    Test_end_time = '2014-11-05'

    data2_name = '1107-1111_data2_pb'
    data3_name = '1107-1111_data3_full_initial_para_window_8_extra_end_iter10'
    L = 40      # 展现的页码
    Union_size = [800]
    Behavior = 'click'   # 3个值, save(所有序列都含有2), click(所有序列都没有2), all(前面2个序列汇总)
                         # behavior 只印象train集合中, 按照点击数量和点击概率排序的ranking, 不作用于test集合
    for pic_number in Union_size:
        now = datetime.now()
        exec_evaluation(Behavior, Train_st_time, Train_end_time, pic_number, Test_st_time, Test_end_time, L, data2_name, data3_name)
        print 'K='+str(pic_number)+' 用时: ', datetime.now()-now
    draw_evaluation.draw_ndcg(Behavior, data3_name)
