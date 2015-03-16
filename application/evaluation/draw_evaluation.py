# coding=utf-8
__author__ = 'CRay'
"""
画evaluation图, 结果输出到为html文件
"""
import calculate_similarity
import make_test_ranking
import make_train_ranking
from lib.Config import Config


def draw_evaluation(behavior, train_time, pic_num, test_st, test_end, page_num, data2, data3):
    test_group = make_test_ranking.get_pic_group(test_st, test_end, page_num)
    data1_click, data2_prob = make_train_ranking.train_data_baseline_all(behavior, train_time)
    data3_pb = make_train_ranking.train_data_position_bias(data2)
    data4_full, data_name = make_train_ranking.train_data_full_model(data3)

    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fout = open(path+'four_ranking.txt', 'w')
    fout.write('rank_click:\t'+str(data1_click)+'\n\n')
    fout.write('rank_prob:\t'+str(data2_prob)+'\n\n')
    fout.write('rank_pb:\t'+str(data3_pb)+'\n\n')
    fout.write('rank_full:\t'+str(data4_full)+'\n\n')
    fout.close()

    ranking_click, ranking_prob, ranking_pb, ranking_full = \
        make_train_ranking.select_share_pic(data1_click, data2_prob, data3_pb, data4_full, pic_num)

    test_pic_info = make_test_ranking.get_test_data_ranking(test_st, test_end, test_group, 0, 0)
    test_ranking = make_test_ranking.sort_rank_by_click_show(test_pic_info)

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


    days = train_time.keys()
    days.sort(reverse=True)
    train_st = days[-1]
    train_end = days[0]

    cf_data = Config('data.conf')
    data_path = cf_data.get('path', 'dataset_path')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = behavior+'_train_'+train_st+'_'+train_end+'_K='+str(pic_num)+'_average='+str(average_pic_num)+'_test_'+test_st+'_'+test_end+'_'+data_name
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


def compare_test_ranking_similarity(test_st, test_end, page_num, min_show, min_click):
    test_group = make_test_ranking.get_pic_group(test_st, test_end, page_num)
    test_pic_info = make_test_ranking.get_test_data_ranking(test_st, test_end, test_group, min_show, min_click)
    ranking_click_show = make_test_ranking.sort_rank_by_click_show(test_pic_info)
    ranking_save_click = make_test_ranking.sort_rank_by_save_click(test_pic_info)
    # ranking_save_show = make_test_ranking.sort_rank_by_save_show(test_pic_info)
    list_similarity = []
    print 'click show', ranking_click_show
    print 'save, click', ranking_save_click
    # print 'save, show', ranking_save_show
    for page in ranking_click_show:
        rank_a = ranking_click_show[page]
        rank_b = ranking_save_click[page]
        similarity = calculate_similarity.calculate_similarity(rank_a, rank_b)
        list_similarity.append([page, similarity])
    list_similarity.sort(key=lambda x: x[0], reverse=False)
    print list_similarity

    cf_data = Config('data.conf')
    chart_path = cf_data.get('path', 'chart_result')
    file_name = Name+'_Test_time_'+test_st+'_'+test_end+'_Min_show='+str(min_show)+'_Min_click='+str(min_click)
    fout_html = open(chart_path+file_name+'.html', 'w')
    fout_html.write('<!doctype html><html lang="en"><meta charset="UTF-8"><head><script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script><script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script><script>$(function () { $("#container").highcharts({ chart: { zoomType: "xy" }, title: { text: "Click_show与'+Name+'的相似度" }, xAxis: [{ tickInterval: 1 }], yAxis: [{ title: { text: "相似度" }}], tooltip: { shared: true }, series: [{ name: "Click_show 与'+Name+'相似度", data:')
    fout_html.write(str(list_similarity))
    fout_html.write('}] }); }); </script></head><body><div id="container" style="min-width:700px;height:400px"></div></body></html> ')
    fout_html.close()


if __name__ == '__main__':
    Test_st = '2014-12-01'
    Test_end = '2014-12-07'
    Page_num = 40
    Min_show = 1000
    Min_click = 30
    Name = 'Save_click'
    compare_test_ranking_similarity(Test_st, Test_end, Page_num, Min_show, Min_click)