# coding=utf-8
__author__ = 'CRay'

from lib import Function
from lib.Mongo import Mongo


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


# 增加过滤 show过少, click过少的条件
def get_test_data_ranking(st_time, end_time, pic_group, min_show, min_click):
    # 计算图片的点击概率
    list_time = Function.get_time_list(st_time, end_time)
    mongo = Mongo('kdd', 'hour_ranking')
    dict_pic_click_info = {}
    db_name = 'pic_info_all'
    mongo.set_collection(db_name)
    # set_target_ranking = set(target_ranking)
    for page in pic_group:
        if page not in dict_pic_click_info:
            dict_pic_click_info[page] = {}
        # intersection = set_target_ranking & pic_group[page]
        intersection = pic_group[page]
        for pic in intersection:
            total_show = 0
            total_click = 0
            total_save = 0
            if pic not in dict_pic_click_info[page]:
                dict_pic_click_info[page][pic] = [0, 0, 0]  # show, click, save
            record = mongo.collection.find({'pid': pic}, {'_id': 0})
            if record.count() > 0:
                pic_info = record[0]
                for day in list_time:
                    for t in range(0, 24):
                        if t < 10:
                            hour = '0' + str(t)
                        else:
                            hour = str(t)
                        full_time = day + ':' + hour
                        if full_time in pic_info:
                            if pic_info[full_time][3] == page:
                                total_show += pic_info[full_time][0]
                                total_click += pic_info[full_time][1]
                                total_save += pic_info[full_time][2]
            if total_show > min_show and total_click > min_click:
                dict_pic_click_info[page][pic][0] += total_show
                dict_pic_click_info[page][pic][1] += total_click
                dict_pic_click_info[page][pic][2] += total_save
    mongo.close()
    # end
    return dict_pic_click_info


# 按照click/show由高到低排序, 计算出指定时间范围内, test数据集的每一页上的图片的排序
def sort_rank_by_click_show(dict_pic_click_info):
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
    return dict_result


# 按照save/click由高到低排序, 计算出指定时间范围内, test数据集的每一页上的图片的排序
def sort_rank_by_save_click(dict_pic_click_info):
    # 处理结果输出, 输出按照点击概率排序的图片列表
    dict_result = {}
    for page in dict_pic_click_info:
        if page not in dict_result:
            dict_result[page] = []
        temp_rank = []  # [图片点击概率, 图片id]
        list_pic = []
        for pic in dict_pic_click_info[page]:
            if dict_pic_click_info[page][pic][0] > 0:
                prob = float(dict_pic_click_info[page][pic][2])/dict_pic_click_info[page][pic][1]  # 这里控制排序方式
                temp_rank.append([round(prob, 4), pic])
            else:
                # 数据库中数据过滤了呈现<50的记录,所以该图片如果几天内没有出现在这一页,那么这一页上的呈现就为0
                pass
        temp_rank.sort(key=lambda x: x[0], reverse=True)
        for item in temp_rank:
            list_pic.append(item[1])
        dict_result[page] = list_pic
    return dict_result

# 按照save/show由高到低排序, 计算出指定时间范围内, test数据集的每一页上的图片的排序
def sort_rank_by_save_show(dict_pic_click_info):
    # 处理结果输出, 输出按照点击概率排序的图片列表
    dict_result = {}
    for page in dict_pic_click_info:
        if page not in dict_result:
            dict_result[page] = []
        temp_rank = []  # [图片点击概率, 图片id]
        list_pic = []
        for pic in dict_pic_click_info[page]:
            if dict_pic_click_info[page][pic][0] > 0:
                prob = float(dict_pic_click_info[page][pic][2])/dict_pic_click_info[page][pic][0]  # 这里控制排序方式
                temp_rank.append([round(prob, 4), pic])
            else:
                # 数据库中数据过滤了呈现<50的记录,所以该图片如果几天内没有出现在这一页,那么这一页上的呈现就为0
                pass
        temp_rank.sort(key=lambda x: x[0], reverse=True)
        for item in temp_rank:
            list_pic.append(item[1])
        dict_result[page] = list_pic
    return dict_result