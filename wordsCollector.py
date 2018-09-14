# Author Simon
# description: count the frequency and translate of the words that front of english_exam2

# -*- encoding=utf-8 -*-

import os
import re
import requests
import db
from collections import Counter


def words_read(filename):
    with open(filename, 'r', errors='ignore') as f:
        var_words = f.read()
        low_words = var_words.lower()
        words = re.findall('[a-z]+', low_words)
    return words


def words_filter(words, except_list):
    new_words = []
    lenth = len(words)
    for index, word in enumerate(words):
        wordlen = len(word)
        if word not in except_list and len(word) > 1:
            new_words.append(word)
        else:
            pass
    print(lenth, len(new_words))
    return new_words


def words_count(words):
    c = Counter(words)
    words_dic = c.most_common(8000)
    # print(words_dic)
    return words_dic


def words_trans(word):
    url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&word=' + word
    try:
        req = requests.get(url)
        req.raise_for_status()
        info = req.json()
        data = info['baesInfo']['symbols'][0]
        #print(data['ph_am'] and data['ph_en'], data['parts'][0]['part'])
        assert info['baesInfo']['symbols'][0]
        assert data['ph_am'] and data['ph_en']
        assert data['parts'][0]['part']
    except:
        return 'none', 'none'
    ph_en = '英[' + data['ph_en'] + ']'
    ph_am = '美[' + data['ph_am'] + ']'
    ex = ''
    for part in data['parts']:
        ex += part['part'] + ';'.join(part['means']) + ';'
    return ph_en + ph_am, ex
