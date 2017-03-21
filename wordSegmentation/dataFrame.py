#! /usr/bin/env python
# -*- coding=utf-8 -*-

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import MySQLdb
import time
import chardet
import jieba
import jieba.posseg as pseg


def load_stop_words(stop_words_file):
    """
    Load stop words.
    :param stop_words_file: the path of file that contains stop words, on word for each line.
    :return: dictionary of stop words, key: word, value: word.
    """
    stop_words = [line.strip().decode('utf-8') for line in open(stop_words_file).readlines()]
    temp_dict = {}
    for word in stop_words:
        # print type(word),word, chardet.detect(word.encode(encoding='utf8'))['encoding']
        temp_dict[word] = word
    return temp_dict


def add_percentages_integer():
    for index in range(1, 101, 1):
        jieba.add_word(str(index) + '%', tag='percentage')
        jieba.add_word(str(index), tag='number')


# Load stop words.
stop_words = load_stop_words('./../resource/stopwords.txt')
jieba.load_userdict('./../resource/total_dict.txt')
# Add percentage and integer.
add_percentages_integer()


def word_segmentation(str):
    """
    Word segmentation and remove stop words from the result.
    :param str: Sentence needs to be split.
    :return: list of words in the sentence, no stop words.
    """

    # Word segmentation.
    words = pseg.cut(str)
    words_list = []
    for word, tag in words:
        # Remove stop words.
        if word in stop_words:
            pass
        else:
            # words_list.append(word + '/' + tag) # add tag after word
            words_list.append(word) # No tag after word.
        # words_list.append(word + '/' + tag)
    print '================================================================'
    print ' '.join(words_list)
    return ' '.join(words_list)


def get_data():
    engine = create_engine('mysql+mysqldb://root:962182@localhost:3306/graduation_screening_disease?charset=utf8')
    t0 = time.time()
    with engine.connect() as conn, conn.begin():
        # dataFrame = pd.read_sql_table(table_name='2016_q_reply', con=conn, index_col=None)
        dataFrame = pd.read_sql(sql='select reply_id, reply_body from 2016_q_reply;', con=conn,index_col='reply_id')
    print 'time:', time.time() - t0

    dataFrame['words'] =dataFrame.reply_body.apply(func=word_segmentation)
    dataFrame.to_csv('D:/reply_words_1.csv',sep=',',header=True,index=True,encoding='utf8')
    # dataFrame.to_sql(name='test3', con=engine, if_exists='append', index=False)
    while True:
        try:
            data = dataFrame.next()
            print data
            data.to_sql(table='test3', engine=engine, if_exists='append')
        except Exception, e:
            print e.message
            break


t0 = time.time()

get_data()
print 'total time:', time.time() - t0