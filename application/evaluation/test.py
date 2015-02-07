__author__ = 'CRay'

import itertools
from application.evaluation import calculate_similarity
from lib.Config import Config

def a():
    fin = open('input.txt', 'r')
    fout = open('output.txt', 'w')
    output = []
    target = [8, 12, 16, 20, 24, 32]
    x = []
    while True:
        line = fin.readline()
        if not line:
            break
        dict_line = eval(line.strip('\r\n').strip(','))
        name = dict_line['name']
        data = dict_line['data']
        page = int(name.split(' ')[1])
        if page in target:
            x = []
            y = []
            for point in data:
                x.append(point[0])
                y.append(point[1])
            output.append(y)
    output.insert(0, x)
    fout.close()
    fin.close()
    for line in output:
        for num in line:
            print num,
        print


def b():
    cf = Config('data.conf')
    path = cf.get('path', 'dataset_path')
    name_data2 = '1104-1111_data2_pb'
    name_data3 = '1104-1111_data3_full_normal_turn'
    fin_data2 = open(path+name_data2+'.txt', 'r')
    line = fin_data2.read()
    list_data2 = line.split(',')
    data2 = list_data2[0: 2000]
    fin_data2.close()

    fin_data3 = open(path+name_data3+'.txt', 'r')
    line = fin_data3.read()
    list_data3 = line.split(',')
    data3 = list_data3[0: 2000]
    fin_data3.close()

    similiarity = calculate_similarity.calculate_similarity(data2, data3)
    print similiarity


if __name__ == '__main__':
    # a()
    b()
