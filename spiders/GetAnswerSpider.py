#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BaseSpider import BaseSpider
from database.MysqlDatabaseClass import MySQLDatabaseClass


class GetAnswerSpider(BaseSpider):
    def __init__(self,url,timeout=100, try_number = 20):
        self.target_url = url
        self.timeout = timeout
        self.try_number = try_number

    def parse(self):
        pass

    def get_answer_list(self):
        sel = self.process_url_request(url=self.target_url,timeout=self.timeout,try_number=self.try_number,xpath_type=True)
        if sel != None:
            answer_content_list = sel.xpath('//div[@class="b_answerli"]')
            for answer_content in answer_content_list:
                answer = {}
                answer['post_url'] = self.target_url
                answer['answer_doctor'] = sel.xpath('//div[@class="b_answerli"]/div[1]/div/span/a/@href')[0]
                print answer_content.xpath('div[@class="b_acceptcont clears"]/div[@class="b_anscontc"]/div[1]/div[1]/p/text()')[0]

if __name__ == '__main__':
    answer = GetAnswerSpider(url='http://www.120ask.com/question/66781721.htm')
    answer.get_answer_list()