# coding=utf-8
__author__ = 'CRay'
"""
画evaluation图, 结果输出到为html文件
"""
import calculate_similarity
import make_pic_collection
from datetime import datetime
from lib.Config import Config


def draw_evaluation(train_st, train_end, pic_num, test_st, test_end, page_num):
    start = datetime.now()
    test_group = calculate_similarity.get_pic_group(test_st, test_end, page_num)
    now = datetime.now()
    print 'test group 构造耗时: ', now - start
    data3_full_ranking_raw, data_name = make_pic_collection.data_full_model(pic_num)
    data2_pb_ranking, data3_full_ranking, pic_num = make_pic_collection.data_position_bias(data3_full_ranking_raw)
    now2 = datetime.now()
    print '3个Ranking 构造耗时: ', now2 - now

    # 画 full model 的 similarity 数据
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data3_full_ranking)
    now3 = datetime.now()
    print '计算出test天数上每页上的图片的使用信息耗时: ', now3 - now2
    similarity_full = calculate_similarity.draw_chart(data3_full_ranking, test_ranking)
    now_full = datetime.now()
    print 'full 用时: ', now_full - now3
    # end

    # 画 position bias 的 similarity 数据
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data2_pb_ranking)
    similarity_pb = calculate_similarity.draw_chart(data2_pb_ranking, test_ranking)
    # end
    now_pb = datetime.now()
    print 'pb 用时: ', now_pb - now_full

    # 画 baseline 的 similarity 数据
    # 按照 click 逆序后 算相似度
    data1_click_ranking, data1_prob_ranking = \
        make_pic_collection.data_baseline(train_st, train_end, data2_pb_ranking)
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data1_click_ranking)
    similarity_click = calculate_similarity.draw_chart(data1_click_ranking, test_ranking)
    now_click = datetime.now()
    print 'click 用时: ', now_click - now_pb

    # 按照prob 逆序后 算相似度
    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group, data1_prob_ranking)
    similarity_prob = calculate_similarity.draw_chart(data1_prob_ranking, test_ranking)
    now_prob = datetime.now()
    print 'prob 用时: ', now_prob-now_click

    cf_data = Config('data.conf')
    data_path = cf_data.get('path', 'dataset_path')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = 'train_'+train_st+'_'+train_end+'_K='+str(pic_num)+'_test_'+test_st+'_'+test_end+'_L='+str(page_num)+'_filter-'+data_name
    fout_data = open(data_path+file_name+'.data', 'w')
    fout_data.write('Baseline click data: \n' + str(similarity_click) + '\n\n')
    fout_data.write('Baseline prob data: \n' + str(similarity_prob) + '\n\n')
    fout_data.write('Position bias: \n' + str(similarity_pb) + '\n\n')
    fout_data.write('Full model: \n' + str(similarity_full))
    fout_data.close()

    fout_html = open(chart_path+file_name+'.html', 'w')
    fout_html.write('<!doctype html><html lang="en"><meta charset="UTF-8"><head><script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script><script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script><script>$(function () { $("#container").highcharts({ chart: { zoomType: "xy" }, title: { text: "Similarity Charts" }, xAxis: [{ tickInterval: 1 }], yAxis: [{ title: { text: "相似度" }}], tooltip: { shared: true }, series: [{ name: "图片点击次数", data:')
    fout_html.write(str(similarity_click))
    fout_html.write('} ,{ name:"图片点击概率", data: ')
    fout_html.write(str(similarity_prob)+'},{ name: "考虑Position bias效应",data: ')
    fout_html.write(str(similarity_pb)+'},{ data: ')
    fout_html.write(str(similarity_full))
    fout_html.write(',name: "完整模型" }] }); }); </script></head><body><div id="container" style="min-width:700px;height:400px"></div></body></html>')
    fout_html.close()

