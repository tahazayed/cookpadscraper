# -*- coding: utf-8 -*-

import scrapy
from time import sleep
from scrapy.selector import Selector
from cookpad.items import RecipeURLItem

class ExtractlinksSpider(scrapy.Spider):
    name = "extractLinks"
    allowed_domains = ["cookpad.com"]
    base_url = 'https://cookpad.com/eg/وصفات?page=%s'
    start_urls = [base_url % 1]
    pageid = 1

    

    def parse(self, response):
        recipes = Selector(response).xpath('//li[@class="recipe"]')

        for recipe in recipes:
            item = RecipeURLItem()

            item['url'] = 'https://cookpad.com' + recipe.xpath(
                'a[@class="media"]/@href').extract()[0]
            yield item
      
        if  len(recipes)>0:
            self.pageid = self.pageid + 1    
            next_page = self.base_url % self.pageid
            yield scrapy.Request(url=next_page, callback=self.parse,meta={'dont_merge_cookies': False},dont_filter=True,encoding='utf-8',errback=self.errback)    

    def errback(self, response):
        pass