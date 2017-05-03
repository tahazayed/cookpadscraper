# -*- coding: utf-8 -*-


import pymongo
from scrapy.conf import settings

class MongoDAL:
    
    def __init__(self):
        self.mongo_uri = "mongodb://%s:%s@%s:%s/%s" % (settings['MONGODB_USER'], settings['MONGODB_PASSWORD'], settings['MONGODB_SERVER'], settings['MONGODB_PORT'], settings['MONGODB_DB'])
        
        self.mongo_db = settings['MONGODB_DB']
        
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
                
                
    def _open_connection(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
                
                
    def _close_connection(self):
        self.client.close()  

                
    def read_mongo(self, collection, query={}, projection=None,distinct=None):
        """ Read from Mongo and Store into DataFrame """

        # Connect to MongoDB
        self._open_connection()
        if projection == None:
            if distinct == None:
                cursor = self.db[collection].find(query)
            else:
                cursor = self.db[collection].find(query).distinct(distinct)
                
        elif projection != None and distinct == None:
            cursor = self.db[collection].find(query, projection)
                
        elif projection != None and distinct != None:
            cursor = self.db[collection].find(query, projection).distinct(distinct)
                

        return list(cursor)
        
        #close connection
        self._close_connection()


