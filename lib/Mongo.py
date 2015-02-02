# coding=utf-8
__author__ = 'CRay'

import pymongo


class Mongo():
    def __init__(self, database, collection):
        self.client = pymongo.Connection()
        self.conn = self.client[database]
        self.collection = self.conn[collection]

    def set_database(self, database):
        self.conn = self.client[database]

    def set_collection(self, collection):
        self.collection = self.conn[collection]

    def get_current_database_name(self):
        return self.conn.name

    def get_current_collection_name(self):
        return self.collection.name

    def close(self):
        self.client.close()