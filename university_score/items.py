# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversityItem(scrapy.Item):
    # define the fields for your item here like:
    #uuid
    score_id = scrapy.Field()
    #学校名字
    school_name = scrapy.Field()
    #学校url
    school_url = scrapy.Field()
    #学校分数线url
    score_url = scrapy.Field()
    #省份
    position = scrapy.Field()
    #文理科，0：文科 1：理科
    type = scrapy.Field()
    #批次，0：本科一批，1：本科二批，2：本科三批，3：提前批，4：专科，5：高职高专，6：本科二三批
    batch = scrapy.Field()
    #年份
    year = scrapy.Field()
    #最低录取分数线
    lowscore = scrapy.Field()
    #平均录取分数线
    avrscore = scrapy.Field()

