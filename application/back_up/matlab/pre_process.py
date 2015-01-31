__author__ = 'tangj_000'
from datetime import datetime, timedelta
import traceback
import random


def pre_process():
    raw_data_file = open('dataset_2014-11-18_small.txt', 'r')
    train_output_file = open('result_2014-11-18_small.txt', 'w')
    cnt = 0
    while True:
        line = raw_data_file.readline()
        if not line:
            break
        cnt += 1
        # print 'creating index\t' + str(cnt)
        dic_data = eval(line)
        pic = dic_data['pid']
        tags = dic_data['tags']

        if pic not in pic_index:
            pic_index.append(pic)

        for i in range(0, len(tags)):
            if tags[i] not in tag_index:
                tag_index.append(tags[i])

    len_tags = len(tag_index)
    len_ctime = len(RECENCY_RANGE.split(',')) + 1
    len_itime = 24
    len_pos = MAX_POS

    M = len_tags + len_ctime + len_itime + len_pos
    N = cnt
    print M, N
    train_output_file.write(str(M) + '\n')

    train_output_file.close()
    raw_data_file.close()
    return


def deal_ctime(str_ctime):
    recency_range = RECENCY_RANGE.split(',')
    # str -> datetime
    ctime = datetime.strptime(str_ctime, "%Y-%m-%d %H:%M:%S").date()
    nowtime = datetime.now().date()   #  改成itime 更合适
    timespan = nowtime - ctime
    # datetime -> int(timespan)
    timespan_num = timespan.days
    list_range = []
    # transfer range into list
    for range_item in recency_range:
        [range_num, range_type] = range_item.split('-')
        range_num = int(range_num)
        factor = 0
        if range_type == 'd':
            factor = 1
        elif range_type == 'w':
            factor = 7
        elif range_type == 'm':
            factor = 30
        elif range_type == 'y':
            factor = 365
        else:
            print 'invalid input!'
        list_range.append(range_num * factor)
    # append timespan and sort
    list_range.append(timespan_num)
    list_range.sort()
    # find the index of timespan
    ind = list_range.index(timespan_num)
    # print list_range, ind
    return ind


def process():
    raw_data_file = open('dataset_2014-11-18_small.txt', 'r')
    train_output_file = open('result_2014-11-18_small.txt', 'a')
    # test_output_file = open('test_data', 'w')
    cnt1 = 0

    # deal the left index, pos + pip + ctime + itime + tags
    lindex_pos = 0
    lindex_pip = lindex_pos + MAX_POS
    #lindex_ctime = lindex_pip + PIC_IN_PAGE
    lindex_ctime = lindex_pos + MAX_POS
    lindex_itime = lindex_ctime + len(RECENCY_RANGE.split(',')) + 1
    lindex_tags = lindex_itime + 24

    dic_processed_data = dict()

    while True:
        try:

            line = raw_data_file.readline()
            #print line
            if not line:
                break
            cnt1 += 1
            #print 'processing data\t' + str(cnt)
            # read data from file
            dic_data = eval(line)
            pid = dic_data['pid']
            uid = dic_data['uid']
            tags = dic_data['tags']
            ctime = dic_data['ctime']
            itime = dic_data['itime']
            pos = dic_data['pos']
            click = dic_data['click']

            vec_feature = []
            vec_result = []
            # deal pos
            if int(pos) <= MAX_POS:
                f_pos = int(pos) - 1
                vec_feature.append(lindex_pos + f_pos)

            # deal ctime
            f_ctime = deal_ctime(ctime)
            vec_feature.append(lindex_ctime + f_ctime)

            # deal itime
            itime_hour = datetime.strptime(itime, "%Y-%m-%d %H:%M:%S").hour
            vec_feature.append(lindex_itime + itime_hour)

            # deal tags
            list_tags = []
            for t in tags:
                ind = tag_index.index(t)
                list_tags.append(ind + lindex_tags)
                #print ind,
            vec_tags = sorted(list_tags)
            vec_feature += vec_tags

            # deal pid
            f_pid = pic_index.index(pid)
            vec_feature.append(f_pid)

            # deal click
            f_click = int(click)
            vec_result.append(f_click)
            #print vec_feature
            str_feature = ''
            str_feature += str(len(vec_feature) - 1) + ' '
            for i in vec_feature:
                str_feature += str(i)+' '
            print str_feature, str(f_click)

            if str_feature not in dic_processed_data:
                dic_processed_data[str_feature] = [f_click, 1]
            else:
                dic_processed_data[str_feature][0] += f_click
                dic_processed_data[str_feature][1] += 1

        except Exception:
            print traceback.format_exc()
            continue

    #print dic_processed_data
    train_output_file.write(str(len(dic_processed_data.items())) + '\n')
    print len(dic_processed_data.items())
    cnt = 0
    for k, v in dic_processed_data.items():
        str_output = ''
        str_output += str(v[0]/float(v[1])) + ' '
        str_output += k
        if '0.0' not in str_output:
            cnt += 1
        str_output += '\n'
        train_output_file.write(str_output)
    print cnt

    raw_data_file.close()
    train_output_file.close()
    #test_output_file.close()


if '__main__' == __name__:
    start_time = datetime.now()

    # set threshold value
    MAX_POS = 200
    PIC_IN_PAGE = 9
    RECENCY_RANGE = '1-w,1-m,3-m,6-m,1-y'

    tag_index = list()
    pic_index = list()

    pre_process()

    end_time1 = datetime.now()
    print 'pre_process finish!'
    print 'Used: ' + str(end_time1 - start_time)

    start_time1 = datetime.now()

    process()

    end_time = datetime.now()
    print 'process finish!'
    print 'Used: ' + str(end_time - start_time1)
    print 'Total Used: ' + str(end_time - start_time)
