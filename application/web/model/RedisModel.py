#coding: utf-8
__author__ = 'CRay'

import redis
import ConfigParser


class RedisModel():
    redis_key = None

    def __init__(self, db_name):
        cf = ConfigParser.ConfigParser()
        cf.read('../../config/redis.conf')
        redis_host = cf.get(db_name, 'host')
        redis_port = cf.get(db_name, 'port')
        redis_db = cf.get(db_name, 'db')
        self.cache = redis.Redis(host=redis_host, port=int(redis_port), db=int(redis_db))

    def set_redis_key(self, key_name):
        self.redis_key = key_name

    def get_redis_key(self):
        return self.redis_key

    def get_pic_ranking(self):
        """
        :return  particular ranking in list structure
        """
        str_pic_ranking = self.cache.get(self.redis_key)
        if str_pic_ranking:
            list_pic_ranking = str_pic_ranking.strip('[]').split(',')
            for i in range(0, len(list_pic_ranking)):
                list_pic_ranking[i] = list_pic_ranking[i].strip(' ')
            return list_pic_ranking
        else:
            return ''