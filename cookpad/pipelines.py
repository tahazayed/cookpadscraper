# -*- coding: utf-8 -*-

import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

from cookpad.items import RecipeItem, RecipeURLItem
from cookpad.mssqlodal import MsSQLDAL


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

    def process_item(self, item, spider):

        for data in item:
            if not data:
                raise DropItem("Missing data!")

        if isinstance(item, RecipeItem):
            #temp_item = json.dumps(dict(item), ensure_ascii=False, sort_keys=True).replace('\r\n', '')
            temp_item = json.dumps(dict(item), ensure_ascii=False, sort_keys=True,indent=4).replace('\r\n', '')
            self.msSQLDAL.execute_none_query(query="exec USP_Recipes_upsert @json=N'%s'", sp_params=(temp_item),\
                                        app_name='MsSQLDBPipeline-' + spider.name)
            if settings['LOG_LEVEL'] == 'DEBUG':
               spider.logger.debug("{} added to MongoDB database!".format(item['rcpe_id']))
        elif isinstance(item, RecipeURLItem):
            self.msSQLDAL.execute_none_query(query="exec USP_RecipesSpider_upsert @url='%s'",sp_params=(item['url']),\
                                        app_name='MsSQLDBPipeline-'+spider.name)
        return item
    def open_spider(self, spider):
        self.msSQLDAL = MsSQLDAL()

    def close_spider(self, spider):
        self.msSQLDAL = None