#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
from BaseSpider import BaseSpider


class GetQuestionNumber(BaseSpider):
    def __init__(self,url,save_file,timeout=100,try_number=20):
        self.target_url = url
        self.timeout = timeout
        self.try_number = try_number
        self.save_file = save_file
        self.target_url_list = []
        for index in range(1, 58, 1):
            url = 'http://club.xywy.com/keshi/' + str(index) + '.html'
            self.target_url_list.append(url)

    def parse(self,all=False):
        file = open(name=self.save_file,mode='wb')
        writer = csv.writer(file)
        writer.writerow(['date','number'])
        if all == False:
            self.get_date_url(writer=writer)
        else:
            for url in self.target_url_list:
                self.get_date_url(writer=writer,url = url)
        file.close()

    def get_date_url(self,writer,url=None):
        if url == None:
            sel = self.process_url_request(url=self.target_url,timeout=self.timeout,try_number=self.try_number,xpath_type=True,encode_type='GBK')
        else:
            sel = self.process_url_request(url=url,timeout=self.timeout,try_number=self.try_number,xpath_type=True,encode_type='GBK')

        if sel != None:
            date_list = sel.xpath('//ul[@class="club_Date clearfix"]/li/a/text()')
            date_url_list = sel.xpath('//ul[@class="club_Date clearfix"]/li/a/@href')
            for index in range(0, len(date_url_list),1):
                date = date_list[index].replace('[','').replace(']','')
                number = self.get_question_number(date_url_list[index])
                writer.writerow([date,number])
        else:
            pass

    def get_question_number(self,url):
        sel = self.process_url_request(url=url,try_number=self.try_number,timeout=self.timeout,xpath_type=True,encode_type='GBK')
        mode = re.compile(r'\d+')
        if sel != None:
            print url
            try:
                number = sel.xpath('//div[@class="subFen"]/text()')[-1]
                number = mode.findall(number)[-1]
                print number
                return number
            except:
                return None
        else:
            return None

if __name__ == '__main__':
    save_file = 'C:/Users/Admin/Desktop/Research/date_question_number.csv'
    question = GetQuestionNumber(url='http://club.xywy.com/keshi/2016-12-30/1.html',save_file=save_file)
    question.parse(all=True)