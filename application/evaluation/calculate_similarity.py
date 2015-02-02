# coding=utf-8
__author__ = 'CRay'

import itertools
from lib import Function
from lib.Mongo import Mongo


# 引自:  Kendall's τ 《2002_Optimizing search engines using click through》
def calculate_similarity(ranking_main, ranking_second):
    concordant = 0
    discordant = 0
    intersection = set(ranking_main) & set(ranking_second)
    for combination in itertools.combinations(intersection, 2):
        p1 = combination[0]
        p2 = combination[1]
        result = (ranking_main.index(p1)-ranking_main.index(p2)) * (ranking_second.index(p1)-ranking_second.index(p2))
        if result > 0:
            concordant += 1
        else:
            discordant += 1
    if (concordant + discordant) > 0:
        temp = float(concordant-discordant)/(concordant+discordant)
        similarity = round(temp, 4)
        return similarity
    else:
        return 0


def get_pic_group(st_time, end_time, st_page, end_page):
    list_time = Function.get_time_list(st_time, end_time)
    dict_page_pic_group = {}
    for page in range(st_page, end_page+1):
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
                for page in range(st_page, end_page+1):
                    selected_pic = list_result[(page-1)*9: page*9]
                    for pic in selected_pic:
                        dict_page_pic_group[page].add(pic)
            else:
                print rank_time, 'is missing!'

    # 计算图片的点击概率
    dict_pic_click_info = {}
    mongo.set_collection('pic_click_info')
    set_target_ranking = set(Target_ranking)
    for page in dict_page_pic_group:
        if page not in dict_pic_click_info:
            dict_pic_click_info[page] = {}
        intersection = set_target_ranking & dict_page_pic_group[page]
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
                print page, pic
        temp_rank.sort(key=lambda x: x[0], reverse=True)
        for item in temp_rank:
            list_pic.append(item[1])
        dict_result[page] = list_pic
    return dict_page_pic_group, dict_pic_click_info, dict_result


def draw_chart(compare_ranking, input_dict):
    result = []
    for page in input_dict:
        second_ranking = input_dict[page]
        similarity = calculate_similarity(compare_ranking, second_ranking)
        result.append([page, similarity])
        print str(page), '  ', compare_ranking, second_ranking
    print result


if __name__ == '__main__':
    Target_ranking = ['206513153', '201058305', '184364289', '179245825', '203859969', '210742529', '213793025']
    St_time = '2014-11-04'
    End_time = '2014-11-04'
    St_page = 1
    End_page = 4
    Pic_group, Pic_click_info, Pic_page_ranking = get_pic_group(St_time, End_time, St_page, End_page)
    draw_chart(Target_ranking, Pic_page_ranking)
    # print Pic_group