__author__ = 'CRay'

import redis
from datetime import datetime, timedelta


def get_time_list(time_st, time_end):
    time_st = datetime.strptime(time_st, '%Y-%m-%d')
    time_end = datetime.strptime(time_end, '%Y-%m-%d')
    time3 = time_st
    time_len = (time_end - time_st).days + 1
    num = 0
    list_time = list()
    while num < time_len:
        t3 = time3.strftime('%Y-%m-%d')
        time3 += timedelta(days=1)
        list_time.append(t3)
        num += 1
    return list_time


def get_ranking(a, b, time_difference):
    list_time = get_time_list(a, b)
    cache = redis.Redis(host='localhost', port=6379, db=0)
    fout = open('ranking.txt', 'w')
    for day in list_time:
        for i in range(0, 24):
            hour = ''
            if i < 10:
                hour = '0'
            hour += str(i)
            temp = day + '#' + hour
            east_time = datetime.strptime(temp, '%Y-%m-%d#%H')
            west_time = east_time - timedelta(hours=time_difference)
            west_time = west_time.strftime('%Y-%m-%d#%H')
            redis_key = 'pp_ios7_hd_cn#hot#' + west_time
            try:
                str_pic_ranking = cache.get(redis_key)
                ranking_time = day + ':' + hour
                fout.write(ranking_time + '\t' + str_pic_ranking)
                fout.write('\n')
            except:
                print 'str_pic_ranking is missing!!!!!'
    fout.close()


def split_ranking(max_req):
    fin = open('ranking.txt', 'r')
    fout = open('output.txt', 'w')
    while True:
        line = fin.readline()
        if not line:
            break
        ranking_time, ranking = line.strip('\n').split('\t')
        list_ranking = ranking.strip('[]').split(', ')
        valid_ranking = list_ranking[0: max_req*36]
        str_ranking = ''
        for pic in valid_ranking:
            str_ranking += pic + ', '
        output = str_ranking.strip(', ')
        fout.write(ranking_time + '\t' + output + '\n')
    fout.close()
    fin.close()


if __name__ == '__main__':
    St = '2014-11-04'
    Et = '2014-12-14'
    Time_difference = 14
    get_ranking(St, Et, Time_difference)
    split_ranking(27)