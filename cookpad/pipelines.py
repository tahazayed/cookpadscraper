# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import scrapy
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from cookpad.items import RecipeItem,RecipeURLItem
import pymssql

class MongoDBPipeline(object):

    def __init__(self):
        self.mongo_uri = "mongodb://%s:%s@%s:%s/%s" % (settings['MONGODB_USER'], settings['MONGODB_PASSWORD'], settings['MONGODB_SERVER'], settings['MONGODB_PORT'], settings['MONGODB_DB'])
        
        self.mongo_db = settings['MONGODB_DB']
        

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if isinstance(item, RecipeItem):      
           self.db[settings['MONGODB_COLLECTION_RECIPES']].update({'rcpe_id': item['rcpe_id']}, dict(item), upsert=True)
           if settings['LOG_LEVEL'] == 'DEBUG':
              spider.logger.debug("{} added to MongoDB database!".format(item['rcpe_id']))
        elif isinstance(item, RecipeURLItem):
            self.db[settings['MONGODB_COLLECTION_RECIPES_SPIDER']].update({'url': item['url']}, dict(item), upsert=True)

        return item
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
  
    
    def close_spider(self, spider):
        self.client.close()


class MsSQLDBPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if isinstance(item, RecipeItem):
            with self.client.cursor(as_dict=True) as cursor:
                print(dict(item))
                cursor.callproc("USP_GeneralLog_upsert",(dict(item),))
            if settings['LOG_LEVEL'] == 'DEBUG':
                spider.logger.debug("{} added to MongoDB database!".format(item['rcpe_id']))
        elif isinstance(item, RecipeURLItem):
            with self.client.cursor(as_dict=True) as cursor:
                cursor.callproc("UDP_RecipesSpider_upsert",(item['url'],))
        self.client.commit()
        return item

    def open_spider(self, spider):
        self.client = pymssql.connect(server=settings['MSSQL_SERVER'], user=settings['MSSQL_USER'], password=settings['MSSQL_PASSWORD'], database=settings['MSSQL_DB'])

    def close_spider(self, spider):
        self.client.close()