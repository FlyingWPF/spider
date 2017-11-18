import scrapy
import re
import time
import uuid
from bs4 import BeautifulSoup
from scrapy.http import Request
from university_score.items import UniversityItem



class Myspider(scrapy.Spider):
    name = 'university'
    allowed_domains = ['www.gaokaopai.com']
    start_urls = ['http://www.gaokaopai.com/daxue-0-0-0-0-0-0-0--p-%s.html' %p for p in range(1,2)]  #(1,3055)
    headers1 = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Safari/537.36'}
    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url = url,headers=self.headers1,callback = self.parse1)
            print(url)
            time.sleep(1)
    #获取学校名字、链接，目前只能获取两个列表，自动对齐
    def parse1(self, response):
        names = response.xpath('//div[@class = "tit"]/h3/a/text()').extract()
        urls = response.xpath('//div[@class = "tit"]/h3/a/@href').extract()
        print(names)
        #无法使用，取不出名字
        # for school in response.xpath('//li[@class = "clearfix"]').extract():
        #     print('*')
        #     print(school)
        #     print(school.xpath('/div[@class = "tit"]/h3/a/text()').extract())
        #     print(school.xpath('/div[1]/h3/a/text()').extract())
        items = []
        for index in range(len(names)):
            university_item = UniversityItem()
            university_item['school_name'] = names[index]
            university_item['school_url'] = urls[index]
            university_item['score_url'] = urls[index].replace('jianjie','luquxian')
            # print(item)
            items.append(university_item)
            # 根据每个学校链接，发送Request请求，并传递item参数
        for item in items:
            formdata = {
                'cname': '23||黑龙江',
                'st': '2',
                'km': '2||理科',
            }
            cnames = ['11||北京',
                      # '12||天津', '13||河北','14||山西','15||内蒙古',
                      # '21||辽宁','21||辽宁', '23||黑龙江',
                      # '31||上海','32||江苏', '33||浙江','34||安徽','35||福建','36||江西','37||山东',
                      # '41||河南', '42||湖北', '43||湖南', '44||广东', '45||广西','46||海南',
                      # '50||重庆', '51||四川', '52||贵州', '53||云南', '54||西藏',
                      # '61||陕西', '62||甘肃', '63||青海', '64||宁夏', '65||新疆',
                      ]
            # majors = ['2||理科','1||文科']  #1:文科 2：理科
            majors = ['2||理科']  # 1:文科 2：理科
            for cname in cnames:
                formdata['cname'] = cname
                item['position'] = cname[4:]
                for major in majors:
                    formdata['km'] = major[:1]
                    formdata['st'] = major
                    if major == '1||文科':
                        item['type'] = '文科'
                    else:
                        item['type'] = '理科'
                    # print(formdata)
                    yield scrapy.FormRequest(url=item['score_url'], meta={'item': item}, formdata=formdata,headers=self.headers1,callback=self.parse2)
                    time.sleep(1)
    #解析学校页面，获取分数
    def parse2(self, response):
        university_item = response.meta['item']
        soup = BeautifulSoup(response.text, "lxml")
        # print(soup.title.text)
        tables = soup.find_all("table")
        score = tables[0].text.splitlines()
        score1 = []
        for str1 in score:
            if str1:
                score1.append(str1.strip())
        while '' in score1:
            score1.remove('')
        score = [score1[i:i + 6] for i in range(0, len(score1), 6)]
        for item in score[1:]:
            code = str(uuid.uuid1())
            university_item['score_id'] =code
            # print('----------'+university_item['score_id']+'------------------' )
            university_item['year'] = item[0]
            university_item['avrscore'] = item[1]
            university_item['lowscore'] = item[2]
            university_item['batch'] = item[5]
            # print(university_item)
            yield university_item


