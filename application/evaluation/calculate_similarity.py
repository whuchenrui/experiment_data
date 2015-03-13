# coding=utf-8
__author__ = 'CRay'

import itertools
import math
from lib.Config import Config

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
        temp = float(concordant)/(concordant+discordant)
        similarity = round(temp, 4)
        return similarity
    else:
        return 0


def draw_chart(model_ranking, test_ranking):
    """
    先求2个ranking的交集Q, 保留这些Q在2个ranking中的相对位置, 用两个小的集合计算相似度, 降低算法运算过程
    :param model_ranking: training出来的排序结果
    :param test_ranking:  testing data上计算出来的所有图片, 按照click ratio排序
    :return:
    """
    result = []
    total = 0
    page_num = len(test_ranking)
    for page in test_ranking:
        page_ranking = test_ranking[page]
        intersection = set(model_ranking) & set(page_ranking)
        total += len(intersection)
        temp_main_ranking = []
        temp_second_ranking = []
        for pic in intersection:
            index_main = model_ranking.index(pic)
            temp_main_ranking.append([index_main, pic])
            index_test = page_ranking.index(pic)
            temp_second_ranking.append([index_test, pic])
        temp_main_ranking.sort(key=lambda x: x[0])
        temp_second_ranking.sort(key=lambda x: x[0])
        main_ranking = []
        second_ranking = []
        for item in temp_main_ranking:
            main_ranking.append(item[1])
        for item in temp_second_ranking:
            second_ranking.append(item[1])

        similarity = calculate_similarity(main_ranking, second_ranking)
        result.append([page, similarity])
        # print str(page), ' ', len(second_ranking)
    average_pic_num = total/page_num
    return result, average_pic_num


def ndcg_similarity(ideal_ranking, full_ranking):
    """
    计算ranking的ndcg值, 其中relevance划分为五个等级4,3,2,1,0. 分别对应真实数据20%.
    计算公式: http://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG
    """

    ideal_len = len(ideal_ranking)
    rel_1 = ideal_len/5         # 范围为[0, rel_1)
    rel_2 = ideal_len*2/5       # 范围为[rel_1, rel_2)
    rel_3 = ideal_len*3/5
    rel_4 = ideal_len*4/5
    IDCG = 0                    # rel1 = 4
    DCG = 0
    for i in range(0, ideal_len):
        pic = ideal_ranking[i]
        if pic not in full_ranking:
            continue
        if i < rel_1:
            rel = 12
        elif i < rel_2:
            rel = 8
        elif i < rel_3:
            rel = 4
        elif i < rel_4:
            rel = 2
        else:
            rel = 0
        rel_index = i + 1
        if rel_index == 1:
            IDCG += 4
        else:
            IDCG += float(rel)/math.log(rel_index, 2)
        index_full = full_ranking.index(pic) + 1
        if index_full == 1:
            DCG += 4
        else:
            DCG += float(rel)/math.log(index_full, 2)
    IDCG = round(IDCG, 4)
    DCG = round(DCG, 4)
    nDCG = round(DCG/IDCG, 4)
    return nDCG


def prepare_ndcg_data():
    cf_data = Config('data.conf')
    path = cf_data.get('path', 'dataset_path')
    fin = open(path+'four_ranking.txt', 'r')
    dict_train_ranking = {}
    while True:
        line = fin.readline()
        if not line:
            break
        if line == '\n':
            continue
        name, ranking = line.split('\t')
        name = name.strip(':')
        dict_train_ranking[name] = ranking
    fin.close()

    fin = open(path+'test_ranking.txt', 'r')
    line = fin.readline()
    dict_test_ranking = eval(line)
    fin.close()
    list_click = dict_train_ranking['rank_click']
    similarity_click = []
    for page in dict_test_ranking:
        ideal_ranking = dict_test_ranking[page]
        similarity = ndcg_similarity(ideal_ranking, list_click)
        similarity_click.append([page, similarity])
    similarity_click.sort(key=lambda x: x[0])
    print 'click'

    list_prob = dict_train_ranking['rank_prob']
    similarity_prob = []
    for page in dict_test_ranking:
        ideal_ranking = dict_test_ranking[page]
        similarity = ndcg_similarity(ideal_ranking, list_prob)
        similarity_prob.append([page, similarity])
    similarity_prob.sort(key=lambda x: x[0])
    print 'prob'

    list_pb = dict_train_ranking['rank_pb']
    similarity_pb = []
    for page in dict_test_ranking:
        ideal_ranking = dict_test_ranking[page]
        similarity = ndcg_similarity(ideal_ranking, list_pb)
        similarity_pb.append([page, similarity])
    similarity_pb.sort(key=lambda x: x[0])
    print 'pb'

    list_full = dict_train_ranking['rank_full']
    similarity_full = []
    for page in dict_test_ranking:
        ideal_ranking = dict_test_ranking[page]
        similarity = ndcg_similarity(ideal_ranking, list_full)
        similarity_full.append([page, similarity])
    similarity_full.sort(key=lambda x: x[0])
    print 'full'
    return similarity_click, similarity_prob, similarity_pb, similarity_full


if __name__ == '__main__':
    # St_time = '2014-11-07'
    # End_time = '2014-11-10'
    # Page_num = 30
    # Pic_group, Pic_click_info, Pic_page_ranking = get_pic_group(St_time, End_time, Page_num, Target_ranking)
    # draw_chart(Target_ranking, Pic_page_ranking)
    # print Pic_group
    prepare_ndcg_data()