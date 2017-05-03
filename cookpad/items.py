# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RecipeItem(Item):
    # define the fields for your item here like:
    n = Field()
    src = Field()
    rcpe_id = Field()
    ingrd = Field()
    instrct = Field()
    img = Field()
    auth = Field()
    tags = Field()
    likes = Field()
    pub = Field()
    etag = Field()
    desc = Field()
    pass

class RecipeURLItem(Item):
    # define the fields for your item here like:
    url = Field()
    title = Field()	
    pass