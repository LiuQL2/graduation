#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
用来抓取病例和心得里面帖子URL的类，该类首先将帖子的URL保存在一个csv文件中。
对于URL保存的文件，在开始的时候如果存在的话，需要删除。
"""

# Author: Liu Qianlong  <LiuQL2@163.com>
# Date: 2016.11.06

import csv
import re
import sys
import datetime
from database.MysqlDatabaseClass import MySQLDatabaseClass

from BaseSpider import BaseSpider

reload(sys)
sys.setdefaultencoding('utf-8')


class GetPostUrl(BaseSpider):
    def __init__(self,url,file_path,page_number = 200,try_number=20):
        """
        初始化一个实例，用来获取病例和心得下面的所有帖子的链接。
        :param post_url_path: 需要将帖子链接保存到的文件名及路径。
        """
        self.file_path = file_path
        self.try_number = try_number
        self.timeout = 100
        self.page_number = page_number
        self.target_url = url
        self.target_url_list = [url]
        for index in range(2, self.page_number+1,1):
            self.target_url_list.append(url + str(index) + '/')

    def get_post(self):
        mysql = MySQLDatabaseClass()
        for url in self.target_url_list:
            post_list = self.get_post_url(url=url)
            for post in post_list:
                print post
                mysql.insert(table='post',record=post)
        mysql.close()

    def get_post_url(self,url):
        post_list = []
        sel = self.process_url_request(url=url,timeout=self.timeout,try_number=self.try_number,xpath_type=True)
        post_content_list = sel.xpath('//ul[@class="clears h-ul3"]/li')
        for post_content in post_content_list:
            post = {}
            post['post_url'] =  post_content.xpath('div[1]/p/a[2]/@href')[0]
            post['post_status'] = post_content.xpath('div[2]/span[2]/text()')[0]
            post['disease'] = post_content.xpath('div[1]/p/a[1]/text()')[0]
            post_list.append(post)
        return post_list

    def update_post(self):
        mysql = MySQLDatabaseClass()
        post_list = mysql.select(table='post')
        for post in post_list:
            post = self.get_post_detail(post)
            mysql.update(table='post',record=post,primary_key={'post_url':post['post_url']})
        mysql.close()

    def get_post_detail(self,post):
        url = post['post_url']
        sel = self.process_url_request(url=url,try_number=self.try_number,timeout=self.timeout,xpath_type=True)
        if sel != None:
            post['post_title'] = sel.xpath('//h1[@id="d_askH1"]/text()')[0]
            patient_info_content = sel.xpath('//div[@class="b_askbox"]/div[1]/div/span/text()')
            mode = re.compile(r'\d+')
            # post['patient_gender'] = patient_info_content[0].split(' ')[0]
            # post['patient_age'] = mode.findall(patient_info_content[0])[0]
            # if len(patient_info_content) == 3:
            #     post['patient_come'] = None
            #     post['post_time'] = patient_info_content[1]
            #     post['answer_number'] = mode.findall(patient_info_content[2])[0]
            # elif len(patient_info_content) == 4:
            #     post['patient_come'] = patient_info_content[1].split('来自')[1]
            #     post['post_time'] = patient_info_content[2]
            #     post['answer_number'] = mode.findall(patient_info_content[3])[0]
            # else:
            #
            #     post['patient_come'] = patient_info_content[3].split('来自')[1]
            #     post['post_time'] = patient_info_content[4]
            #     post['answer_number'] = mode.findall(patient_info_content[5])[0]

            for index in range(0, len(patient_info_content), 1):
                if ' | ' in patient_info_content[index]:
                    post['patient_gender'] = patient_info_content[index].split(' ')[0]
                    post['patient_age'] = mode.findall(patient_info_content[index])[0]
                elif '来自' in patient_info_content[index]:
                    post['patient_come'] = patient_info_content[index].split('来自')[1]
                elif ':' in patient_info_content[index] and '-' in patient_info_content[index]:
                    post['post_time'] = patient_info_content[index]
                elif '回复' in patient_info_content[index]:
                    post['answer_number'] = mode.findall(patient_info_content[index])[0]
                elif '悬赏' in patient_info_content[index]:
                    xpath = '//div[@class="b_askbox"]/div[1]/div/span[' + str(index + 1) +']/em/text()'
                    post['reward'] = sel.xpath(xpath)[0] + patient_info_content[index + 1]

            post_content = sel.xpath('//div[@class="b_askbox"]/div[2]/p[@class="crazy_new"]')
            for content in post_content:
                if '描述' in content.xpath('span/text()')[0]:
                    describe = content.xpath('string(.)').replace('\n','').replace(' ','').replace('BR>','')
                    post['health_describe'] = describe
                elif '帮助' in content.xpath('span/text()')[0]:
                    post['want_help'] = (content.xpath('text()')[1]).replace(' ', '')
            try:
                post['patient_id'] = sel.xpath('//div[@class="b_askbox"]/div[3]/span/var/text()')[0]
            except IndexError:
                patient_id_content = sel.xpath('//div[@class="b_askbox"]/div[3]/span')[0]
                patient_id = patient_id_content.xpath('string(.)').replace(' ', '').replace('\t', '').split('：')[1]
                patient_id = patient_id.replace('投诉', '').replace('\n', '')
                post['patient_id'] = patient_id
            except:
                pass
            post['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            pass
        return post


if __name__ == '__main__':
    file_path = 'D:/Qianlong/PyCharmProjects/Crawler_xywy_doctor_communication/data/'
    post = GetPostUrl(url='http://www.120ask.com/list/tangniaobing/over/',file_path=file_path)
    # post.get_post()
    # post.update_post()
    post.get_post_detail(post={'post_url':'http://www.120ask.com/question/3153008.htm'})



