#! /usr/bin/env python
# -*- coding=utf-8 -*-

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import MySQLdb
import time
import jieba
import jieba.posseg as pseg

# stop_key = [line.strip().decode('utf-8') for line in open('D:\\Python27\\stopword.txt').readlines()]
stop_key = []
jieba.add_word('问题分析',13,tag='drug')
print jieba.suggest_freq('问题分析')

def word_segmentation(str):
    # seg_list = jieba.cut(sentence=str,HMM=True)
    # print seg_list[0]
    # seg_list =
    # seg_list = jieba.cut_for_search(sentence=str,HMM=True)
    # print 'Remove stop words: ', ' / ' .join(list(list(seg_list) - list(stop_key)))
    # seg_list = jieba.cut(sentence=str, HMM=True)
    # print 'Contain stop words: ', ' / '.join(seg_list)
    # return ' / ' .join(list(set(seg_list) - set(stop_key)))

    words = pseg.cut(str)
    print '================================================================'
    words_list = []
    for word, tag in words:
        words_list.append(word + '/' + tag)
        # print word, flag
    print ' '.join(words_list)
    return ' '.join(words_list)


def get_data():
    engine = create_engine('mysql+mysqldb://root:962182@localhost:3306/graduation_screening_disease?charset=utf8')
    t0 = time.time()
    with engine.connect() as conn, conn.begin():
        # dataFrame = pd.read_sql_table(table_name='2016_q_reply', con=conn, index_col=None)
        dataFrame = pd.read_sql(sql='select * from 2016_q_reply limit 100;', con=conn,index_col='reply_id')
    # dataFrame = pd.read_sql_table(table_name='2016_doctor_url',
    #                               con='mysql+mysqldb://root:962182@localhost:3306/graduation_screening_disease?charset=utf8',
    #                               index_col='doctor_url',columns=None,chunksize=1000)
    print 'time:', time.time() - t0
    print dataFrame
    dataFrame.reply_body.apply(func=word_segmentation)
    # dataFrame.to_sql(name='test3', con=engine, if_exists='append', index=False)
    while True:
        try:
            data = dataFrame.next()
            print data
            data.to_sql(table='test3', engine=engine, if_exists='append')
        except Exception, e:
            print e.message
            break

get_data()