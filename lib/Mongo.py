# coding=utf-8
__author__ = 'CRay'

import pymongo


class Mongo():
    def __init__(self, database, collection):
        self.client = pymongo.Connection()
        self.conn = self.client[database]
        self.collection = self.conn[collection]

    def conn_database(self, database):
        self.conn = self.client[database]

    def conn_collection(self, collection):
        self.collection = self.conn[collection]

    def close(self):
        self.client.close()