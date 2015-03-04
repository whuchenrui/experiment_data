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


def exec_evaluation(behavior, train_time, pic_num, test_st, test_end, page_num, data2, data3):
    draw_evaluation.draw_evaluation(behavior, train_time, pic_num, test_st, test_end, page_num, data2, data3)


if __name__ == '__main__':
    # 时间设置为字典格式, key为日期, value 为小时. 查询会遍历这些指定的时间
    Train_time = {'2014-11-13': ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']}

    Test_st_time = '2014-11-14'
    Test_end_time = '2014-11-18'

    data2_name = 'rank-13-13-pos-save'
    data3_name = 'rank-13-13-turn2-save'
    L = 40      # 展现的页码
    Union_size = [1000]
    Behavior = 'save'    # 3个值, save(所有序列都含有2), click(所有序列都没有2), all(前面2个序列汇总)
                         # behavior 只影响train集合中, 按照点击数量和点击概率排序的ranking, 不作用于test集合
    for pic_number in Union_size:
        now = datetime.now()
        exec_evaluation(Behavior, Train_time, pic_number, Test_st_time, Test_end_time, L, data2_name, data3_name)
        print 'K='+str(pic_number)+' 用时: ', datetime.now()-now
    # draw_evaluation.draw_ndcg(Behavior, data3_name)
