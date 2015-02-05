# coding=utf-8
__author__ = 'CRay'



def draw_evaluation(train_st, train_end, pic_num, test_st, test_end, page_num):
    start = datetime.now()
    test_group = calculate_similarity.get_pic_group(test_st, test_end, page_num)

    data3_full_ranking_raw = make_pic_collection.data_full_model(pic_num)
    # 画 position bias 的 similarity 数据
    data2_pb_ranking, data3_full_ranking, pic_num = make_pic_collection.data_position_bias(data3_full_ranking_raw)
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
    fout_html.write('} ,{ name:"图片点击概率", color: "#FFA07A", data: ')
    fout_html.write(str(similarity_prob)+'},{ color: "#6495ED", data: ')
    fout_html.write(str(similarity_pb))
    fout_html.write(',name: "考虑Position bias效应" }] }); }); </script></head><body><div id="container" style="min-width:700px;height:400px"></div></body></html>')
    fout_html.close()

