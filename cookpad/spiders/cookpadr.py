# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from cookpad.items import RecipeItem, RecipeURLItem
from cookpad.mongodal import MongoDAL
from cookpad.mssqlodal import MsSQLDAL
import sys


class CookpadrSpider(scrapy.Spider):
    name = "cookpadr"

    def start_requests(self):
        urls = []

        if settings['IS_MSSQLDB']:
            self.msSQLDAL = MsSQLDAL()
            results = self.msSQLDAL.read(query="USP_RecipesSpider_readall",app_name=self.name)
        else:
            mongodal = MongoDAL()
            results = mongodal.read_mongo(collection="recipes_spider")

        for result in results:
            urls.append(result['url'])

        for i, url in enumerate(urls):
            yield scrapy.Request(url='https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA/' + url,
                                 meta={'dont_merge_cookies': False} \
                                 , callback=self.parse, dont_filter=True, encoding='utf-8', errback=self.errback)

    def parse(self, response):
        page = response.body.decode("utf-8")
        soup = BeautifulSoup(page, 'html.parser')

        recipe_likes = soup.find('span', attrs={'class': 'field-group__hide subtle'}).text.strip()
        self.logger.debug("recipe_likes"+recipe_likes)
        
        likes = 0
        try:
            likes = (0, int(recipe_likes.strip()))[len(recipe_likes.strip()) > 0]
        except:
            likes = 0

        if likes != 0:
        
            recipe_name = soup.find('h1', {'class': "recipe-show__title recipe-title strong field-group--no-container-xs"}).text.strip()
            self.logger.debug(recipe_name)
            
            author_name = soup.find('span', attrs={'itemprop': "author"}).text.strip().replace("'","-")
            self.logger.debug(author_name)
            
            author_url = soup.find('span', attrs={'itemprop': "author"}).parent['href']
            self.logger.debug(author_url)
            
            recipe_id = soup.find('div', attrs={'class': 'bookmark-button '})['id'].replace('bookmark_recipe_', '')
            self.logger.debug(recipe_id)
            
            try:
                recipe_image = [x['src'] for x in soup.findAll('img', {'alt': recipe_name})][0]
            except:
                recipe_image = ''
            desc = soup.find(attrs={'name': 'description'})['content']

            # recipe_image = recipe_image_div.find('a',{'data-target':'#modal'})["href"]
            recipe_ingredients = []
            index = 1
            for i in soup.find_all('li', {'class': 'ingredient'}):
                if i.text.strip() != '':
                    recipe_ingredients.append({'in': index, 'n': i.text.strip().replace("'","-")})
                    index = index + 1

            index = 1
            recipe_instructions = []
            for i in soup.find_all('li', {'class': 'step numbered-list__item card-sm'}):
                step = i.find('p').text.strip()
                try:
                    imageUrl = [x['src'] for x in i.findAll('img')][0]\
                        .replace('//global.cpcdn.com/en/assets/blank_step-17c926f7cd09f48ae848b5dfe68bcf26cf84cf2129001eee9513dc6c062d83bc.jpg','')
                except:
                    imageUrl = ''
                recipe_instructions.append({'in': index, 'txt': step.replace("'","-"), 'img': imageUrl})
                del step, imageUrl

                index = index + 1

            recipe_tags = []
            for i in soup.find_all('ul', {"class": 'list-inline'}):
                for x in i.find_all('a'):
                    if('/eg/search/' in x['href']):
                        recipe_tags.append(x.text.strip().replace("'","-"))


            recipe = RecipeItem()
            recipe["n"] = recipe_name.replace("'","-")
            recipe["src"] = response.url.replace('https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA/', '')
            recipe["rcpe_id"] = (recipe_id, int(recipe_id.strip()))[len(recipe_id.strip()) > 0]
            recipe["ingrd"] = recipe_ingredients
            recipe["instrct"] = recipe_instructions
            recipe["img"] = recipe_image
            recipe["auth"] = {'n': author_name, 'src': author_url}
            recipe["tags"] = recipe_tags
            recipe["likes"] = likes
            recipe["pub"] = datetime.utcnow().isoformat()
            # recipe["etag"] = response.headers.get(b'Etag').decode("utf-8")
            # recipe["desc"] = desc
            del page, soup, recipe_name, author_name, author_url, recipe_id, likes
            del recipe_image, recipe_likes, recipe_ingredients, index
            del recipe_tags, recipe_instructions
            
            self.logger.debug(recipe)

            return recipe
        else:
            del page, soup, recipe_likes, likes

            if(self.logger.isEnabledFor(10)):
                self.logger.debug("0 Likes")
            pass

    def errback(self, response):
        if settings['IS_MSSQLDB']:
            src = response.request.url.replace('https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA/', '')
            self.msSQLDAL.execute_none_query(query="exec USP_Recipes_NotFound_insert @src='%s'", sp_params=(src.replace('\r\n', '')), \
                                        app_name='MsSQLDBPipeline-' + self.name)
        pass


class ExtractlinksSpider(scrapy.Spider):
    name = "extractLinks"
    allowed_domains = ["cookpad.com"]
    base_url = 'https://cookpad.com/eg/وصفات?page=%s'
    start_urls = [base_url % 1]
    pageid = 1
    max_page_Id = 1020

    def parse(self, response):
        recipes = Selector(response).xpath('//div[@class="masonry__item"]/div/a[@class="link-unstyled"]/@href').extract()

        for recipe in recipes:
            item = RecipeURLItem()
            item['url'] = recipe.replace('/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA/', '')
            yield item

        #if len(recipes) > 0 :
        if len(recipes) > 0 and self.pageid < self.max_page_Id:
            self.pageid = self.pageid + 1
            next_page = self.base_url % self.pageid
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'dont_merge_cookies': False}, \
            dont_filter=True \
            , encoding='utf-8', errback=self.errback)

    def errback(self, response):
        pass


def notThreadSafe(x):
    """do something that isn't thread-safe"""
    pass


configure_logging()
project_settings = get_project_settings()

runner = CrawlerProcess(settings=project_settings)


@defer.inlineCallbacks
def crawl():
    #yield runner.crawl(ExtractlinksSpider)
    yield runner.crawl(CookpadrSpider)
    reactor.stop()


try:
    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished
except:
    pass
