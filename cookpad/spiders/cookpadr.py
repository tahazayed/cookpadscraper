# -*- coding: utf-8 -*-
import scrapy
from cookpad.items import RecipeItem
from bs4 import BeautifulSoup
from datetime import datetime
from cookpad.mongodal import MongoDAL

class CookpadrSpider(scrapy.Spider):
    name = "cookpadr"

    def start_requests(self):
        urls = []
        mongodal = MongoDAL()
        results = mongodal.read_mongo(collection="recipes_spider")
        for result in results:
            urls.append(result['url'])
            
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url.replace('\n',''),meta={'dont_merge_cookies': False}\
            ,callback=self.parse,dont_filter=True,encoding='utf-8',errback=self.errback)

                    
    def parse(self, response):
        page=response.body.decode("utf-8")
        soup = BeautifulSoup(page, 'html.parser')
        recipi_name = soup.find('h1',{'class':"recipe-show__title recipe-title strong field-group--no-container-xs"}).text.strip()
        author_name = soup.find('span', attrs={'itemprop':"author"}).text.strip()
        author_url = 'https://cookpad.com' + soup.find('span', attrs={'itemprop':"author"}).parent['href']
        recipi_id = soup.find('div', attrs={'class':'bookmark-button '})['id'].replace('bookmark_recipe_','')
        try:
                recipi_image = [x['src'] for x in soup.findAll('img',{'alt':'Photo'})][0]
        except:
                recipi_image = ''
        
        recipi_likes = soup.find('span', attrs={'class':'field-group__hide subtle'}).text.strip()
        desc = soup.find(attrs={'name':'description'})['content']

        
        #recipi_image = recipi_image_div.find('a',{'data-target':'#modal'})["href"]
        recipi_ingredients = []
        index = 1
        for i in soup.find_all('li',{'class':'ingredient '}):
                if i.text.strip() != '':
                        recipi_ingredients.append({'in':index, 'n':i.text.strip()})
                        index = index + 1
                
        index = 1
        recipi_instructions = []
        for i in soup.find_all('li',{'class':'step numbered-list__item card-sm'}):
                step = i.find('p').text.strip()
                try:
                        imageUrl = [x['src'] for x in i.findAll('img')][0]
                except:
                        imageUrl = ''        
                recipi_instructions.append({'in':index,'txt':step,'img':imageUrl})
                del step
                del imageUrl
                index = index + 1 
                
        recipi_tags = []        
        for i in soup.find_all('ul',{"class":'list-inline'}):
                for x in i.find_all('a'):
                        recipi_tags.append(x.text.strip())
                break 
        likes=0
        try:
                likes = (0, int(recipi_likes.strip()))[len(recipi_likes.strip())>0]
        except:
                likes = 0
        recipe = RecipeItem()
        recipe["n"] = recipi_name
        recipe["src"] = response.url
        recipe["rcpe_id"] = (recipi_id, long(recipi_id.strip()))[len(recipi_id.strip())>0]
        recipe["ingrd"] = recipi_ingredients
        recipe["instrct"] = recipi_instructions
        recipe["img"] = recipi_image
        recipe["auth"] = {'n':author_name,'src':author_url} 
        recipe["tags"] = recipi_tags
        recipe["likes"] = likes
        recipe["pub"] = datetime.utcnow().isoformat()
        recipe["etag"] = response.headers.get(b'Etag').decode("utf-8")
        recipe["desc"] = desc 
        del  page, soup, recipi_name, author_name, author_url, recipi_id, likes
        del recipi_image, recipi_likes, recipi_ingredients, index
        del recipi_tags, recipi_instructions
        
        return recipe
        
    def errback(self, response):
       pass
