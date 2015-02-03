# coding=utf-8
__author__ = 'CRay'
import traceback
from application.raw_data import filter_dataset
from application.raw_data import split_dataset
from application.draw_charts import page_positon_bais, turn_probability
from application.evaluation import init_db
from application.evaluation import calculate_similarity
from application.evaluation import make_pic_collection
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
        page_positon_bais.position_bias(st_time, end_time, behavior)         # page的postion图
        print 'Page position bias finish !'
        turn_probability.turn_probability(st_time, end_time, behavior, 3, 15, 2, 0, 20)
        print 'Turn probability with last 8 pages finish !'
    except:
        print traceback.format_exc()


def exec_evaluation(train_st, train_end, pic_num, test_st, test_end, page_num):
    start = datetime.now()
    test_group = calculate_similarity.get_pic_group(test_st, test_end, page_num)

    # 画 position bias 的 similarity 数据
    data2_pb_ranking = make_pic_collection.data_position_bias(pic_num)
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data2_pb_ranking)
    similarity_pb = calculate_similarity.draw_chart(data2_pb_ranking, test_ranking)
    # end
    now_pb = datetime.now()
    print 'pb 用时: ', now_pb-start
    # 画 baseline 的 similarity 数据
    # 按照 click 逆序后 算相似度
    data1_click_ranking, data1_prob_ranking = \
        make_pic_collection.data_baseline(train_st, train_end, data2_pb_ranking)
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data1_click_ranking)
    similarity_click = calculate_similarity.draw_chart(data1_click_ranking, test_ranking)
    now_click = datetime.now()
    print 'click 用时: ', now_click-now_pb

    # 按照prob 逆序后 算相似度
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data1_prob_ranking)
    similarity_prob = calculate_similarity.draw_chart(data1_prob_ranking, test_ranking)
    now_prob = datetime.now()
    print 'prob 用时: ', now_prob-now_click

    cf_data = Config('data.conf')
    data_path = cf_data.get('path', 'dataset_path')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = 'train_'+train_st+'_'+train_end+'_K='+str(pic_num)+'_test_'+test_st+'_'+test_end+'_L='+str(page_num)
    fout_data = open(data_path+file_name+'.data', 'w')
    fout_data.write('Baseline click data: \n' + str(similarity_click) + '\n\n')
    fout_data.write('Baseline prob data: \n' + str(similarity_prob) + '\n\n')
    fout_data.write('Position bias: \n' + str(similarity_pb))
    fout_data.close()

    fout_html = open(chart_path+file_name+'.html', 'w')
    fout_html.write('<!doctype html><html lang="en"><meta charset="UTF-8"><head><script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script><script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script><script>$(function () { $("#container").highcharts({ chart: { zoomType: "xy" }, title: { text: "Similarity Charts" }, xAxis: [{ tickInterval: 1 }], yAxis: [{ title: { text: "相似度" }}], tooltip: { shared: true }, series: [{ name: "图片点击次数", color: "#89A54E", data:')
    fout_html.write(str(similarity_click))
    fout_html.write('} ,{ name:"图片平均点击概率", color: "#FFA07A", data: ')
    fout_html.write(str(similarity_prob)+'},{ color: "#6495ED", data: ')
    fout_html.write(str(similarity_pb))
    fout_html.write(',name: "考虑Position bias效应" }] }); }); </script></head><body><div id="container" style="min-width:700px;height:400px"></div></body></html>')
    fout_html.close()


if __name__ == '__main__':
    Select_dataset = 'save'  # view 对应 view数据集,  save对应save数据集   all 对应所有数据集
    Train_st_time = '2014-11-07'
    Train_end_time = '2014-11-11'
    K = 1500  # 图片集合个数
    Test_st_time = '2014-11-12'
    Test_end_time = '2014-11-15'
    L = 40  # 展现的页码
    for pic_number in [700, 1000, 1300, 1600]:
        exec_evaluation(Train_st_time, Train_end_time, pic_number, Test_st_time, Test_end_time, L)
