# coding=utf-8
__author__ = 'CRay'

import itertools
from lib import Function
from lib.Mongo import Mongo
from datetime import datetime

# 方法: Kendall's τ method.  引自: 《2002_Optimizing search engines using click through》
def calculate_similarity(ranking_a, ranking_b):
    """
    计算两个序列的相似度, 方法可优化之处: 缩小 ranking_main大小, 或改用dict存储 (大量时间损耗在index方法上)
    """
    concordant = 0
    discordant = 0
    for combination in itertools.combinations(ranking_a, 2):
        p1 = combination[0]
        p2 = combination[1]
        try:
            result = ranking_b.index(p2)-ranking_b.index(p1)
            if result > 0:
                concordant += 1
            else:
                discordant += 1
        except:
            pass   # 当图片不在list 跳过
    if (concordant + discordant) > 0:
        temp = float(concordant-discordant)/(concordant+discordant)
        similarity = round(temp, 4)
        return similarity
    else:
        return 0


def get_pic_group(st_time, end_time, page_num):
    """
    获得时间范围内每个页码上出现的图片集合
    dict_page_pic_group: {page: (pic1, pic2 ...)}
    """
    list_time = Function.get_time_list(st_time, end_time)
    dict_page_pic_group = {}
    for page in range(1, page_num+1):
        dict_page_pic_group[page] = set()
    mongo = Mongo('kdd', 'hour_ranking')
    for day in list_time:
        for i in range(0, 24):
            hour = ''
            if i < 10:
                hour = '0'
            hour += str(i)
            rank_time = day + ':' + hour
            record = mongo.collection.find({'time': rank_time}, {'_id': 0})
            if record.count() > 0:
                list_result = record[0]['ranking']
                for page in range(1, page_num+1):
                    selected_pic = list_result[(page-1)*9: page*9]
                    for pic in selected_pic:
                        dict_page_pic_group[page].add(pic)
            else:
                # print rank_time, 'is missing!'
                pass
    mongo.close()
    return dict_page_pic_group


def get_test_data_ranking(st_time, end_time, pic_group, target_ranking):
    # 计算图片的点击概率
    list_time = Function.get_time_list(st_time, end_time)
    mongo = Mongo('kdd', 'hour_ranking')
    dict_pic_click_info = {}
    mongo.set_collection('pic_click_info')
    set_target_ranking = set(target_ranking)
    same_group = 0
    for page in pic_group:
        if page not in dict_pic_click_info:
            dict_pic_click_info[page] = {}
        intersection = set_target_ranking & pic_group[page]
        same_group += len(intersection)
        for pic in intersection:
            if pic not in dict_pic_click_info[page]:
                dict_pic_click_info[page][pic] = [0, 0]
            record = mongo.collection.find({'pid': pic}, {'_id': 0})
            if record.count() > 0:
                pic_info = record[0]
                for day in list_time:
                    if day in pic_info:
                        if str(page) in pic_info[day]:   # page 为str类型
                            dict_pic_click_info[page][pic][0] += pic_info[day][str(page)][0]  # mongo 中page是字符串
                            dict_pic_click_info[page][pic][1] += pic_info[day][str(page)][1]
    mongo.close()
    pic_group_length = len(pic_group)
    print '平均共同图片数为: ', str(int(same_group)/pic_group_length)
    # end

    # 处理结果输出, 输出按照点击概率排序的图片列表
    dict_result = {}
    for page in dict_pic_click_info:
        if page not in dict_result:
            dict_result[page] = []
        temp_rank = []  # [图片点击概率, 图片id]
        list_pic = []
        for pic in dict_pic_click_info[page]:
            if dict_pic_click_info[page][pic][0] > 0:
                prob = float(dict_pic_click_info[page][pic][1])/dict_pic_click_info[page][pic][0]
                temp_rank.append([round(prob, 4), pic])
            else:
                # 数据库中数据过滤了呈现<50的记录,所以该图片如果几天内没有出现在这一页,那么这一页上的呈现就为0
                pass
        temp_rank.sort(key=lambda x: x[0], reverse=True)
        for item in temp_rank:
            list_pic.append(item[1])
        dict_result[page] = list_pic
    return dict_pic_click_info, dict_result


def draw_chart(model_ranking, test_ranking):  # test_ranking 是取交集后,按照点击概率逆序排列的图片集合
    result = []
    for page in test_ranking:
        second_ranking = test_ranking[page]

        temp = []
        for pic in test_ranking[page]:
            index_model = model_ranking.index(pic)
            temp.append([index_model, pic])
        temp.sort(key=lambda x: x[0])
        main_ranking = []
        for item in temp:
            main_ranking.append(item[1])

        similarity = calculate_similarity(main_ranking, second_ranking)
        result.append([page, similarity])
        # print str(page), ' ', len(second_ranking)
    return result


if __name__ == '__main__':
    St_time = '2014-11-07'
    End_time = '2014-11-10'
    Page_num = 30
    # Pic_group, Pic_click_info, Pic_page_ranking = get_pic_group(St_time, End_time, Page_num, Target_ranking)
    # draw_chart(Target_ranking, Pic_page_ranking)
    # print Pic_group