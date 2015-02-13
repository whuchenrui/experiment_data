# coding=utf-8
__author__ = 'CRay'
"""
画evaluation图, 结果输出到为html文件
"""
import calculate_similarity
import make_pic_collection
from lib.Config import Config


def draw_evaluation(behavior, train_st, train_end, pic_num, test_st, test_end, page_num, data2, data3):
    test_group = calculate_similarity.get_pic_group(test_st, test_end, page_num)
    data1_click, data2_prob = make_pic_collection.test_data_baseline_all(behavior, train_st, train_end)
    data3_pb = make_pic_collection.test_data_position_bias(data2)
    data4_full, data_name = make_pic_collection.test_data_full_model(data3)

    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fout = open(path+'four_ranking.txt', 'w')
    fout.write('rank_click:\t'+str(data1_click)+'\n\n')
    fout.write('rank_prob:\t'+str(data2_prob)+'\n\n')
    fout.write('rank_pb:\t'+str(data3_pb)+'\n\n')
    fout.write('rank_full:\t'+str(data4_full)+'\n\n')
    fout.close()

    ranking_click, ranking_prob, ranking_pb, ranking_full = \
        make_pic_collection.select_share_pic(data1_click, data2_prob, data3_pb, data4_full, pic_num)

    test_info, test_ranking = \
        calculate_similarity.get_test_data_ranking(test_st, test_end, test_group)
    # 画 full model 的 similarity 数据
    similarity_full, average_pic_num = calculate_similarity.draw_chart(ranking_full, test_ranking)

    fout = open(path+'test_ranking.txt', 'w')
    fout.write(str(test_ranking))
    fout.close()

    # 画 position bias 的 similarity 数据
    similarity_pb, average_pic_num = calculate_similarity.draw_chart(ranking_pb, test_ranking)

    # 按照 prob 逆序后 算相似度
    similarity_prob, average_pic_num = calculate_similarity.draw_chart(ranking_prob, test_ranking)

    # 按照click 逆序后 算相似度
    similarity_click, average_pic_num = calculate_similarity.draw_chart(ranking_click, test_ranking)
    print 'average', str(average_pic_num)

    cf_data = Config('data.conf')
    data_path = cf_data.get('path', 'dataset_path')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = behavior+'_train_'+train_st+'_'+train_end+'_K='+str(pic_num)+'_average='+str(average_pic_num)+'_test_'+test_st+'_'+test_end+'_L='+str(page_num)+data_name+'_union'
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


def draw_ndcg(behavior, data_name):
    similarity_click, similarity_prob, similarity_pb, similarity_full = calculate_similarity.prepare_ndcg_data()

    cf_data = Config('data.conf')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = behavior+'_nDCG' + data_name
    fout_html = open(chart_path+file_name+'.html', 'w')
    fout_html.write('<!doctype html><html lang="en"><meta charset="UTF-8"><head><script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script><script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script><script>$(function () { $("#container").highcharts({ chart: { zoomType: "xy" }, title: { text: "nDCG" }, xAxis: [{ tickInterval: 1 }], yAxis: [{ title: { text: "相似度" }}], tooltip: { shared: true }, series: [{ name: "图片点击次数", data:')
    fout_html.write(str(similarity_click))
    fout_html.write('} ,{ name:"图片点击概率", data: ')
    fout_html.write(str(similarity_prob)+'},{ name: "考虑Position bias效应",data: ')
    fout_html.write(str(similarity_pb)+'},{ data: ')
    fout_html.write(str(similarity_full))
    fout_html.write(',name: "完整模型" }] }); }); </script></head><body><div id="container" style="min-width:700px;height:400px"></div></body></html>')
    fout_html.close()
