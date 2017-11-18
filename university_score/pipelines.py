# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from university_score import settings
from university_score.items import UniversityItem
MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DB = settings.MYSQL_DB

# db = pymysql.connect("localhost","root","88888888","university")
db = pymysql.connect(host = MYSQL_HOSTS,user = MYSQL_USER,password = MYSQL_PASSWORD,database = MYSQL_DB)
cursor = db.cursor()

class Sql:
    @classmethod
    def insert_score(cls,score_id,school,position,type,batch,year,lowscore,avrscore):
        # db = pymysql.connect(host=MYSQL_HOSTS, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
        # cursor = db.cursor()
        sql = "INSERT INTO SCORE VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(score_id,school,position,type,batch,year,lowscore,avrscore)
        cursor.execute(sql)
        db.commit()


    @classmethod
    def select_id(cls,score_id):
        sql = "SELECT EXISTS(SELECT 1 FROM score WHERE score_id='%s')"% score_id
        value = {'score_id':score_id}
        cursor.execute(sql)
        return cursor.fetchall()[0]
############################################
class UniversityScorePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,UniversityItem):
            school_id = item['score_id']
            # print(type(id))
            ret = Sql.select_id(school_id)
            if ret[0] == 1:
                print('已经存在')
            else:
                print('准备插入')
                # school_id = item['score_id']
                school = item['school_name']
                year =item['year']
                avrscore = item['avrscore']
                lowscore=item['lowscore']
                batch=item['batch']
                position = item['position']
                type = item['type']
                Sql.insert_score(school_id,school,position,type,batch,year,lowscore,avrscore)
                return item



















