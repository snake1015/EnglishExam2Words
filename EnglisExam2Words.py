import os
import db
import csv
import wordsCollector


def words_insert(new_words, dbcxn, tableName):
    i = raw = 0
    for word, times in new_words:
        word_query = dbcxn.query(tableName).filter(tableName.wordname == word).count()
        #print(word_query)
        raw += 1
        #print(raw)
        if word_query < 1:
            wordRaw = tableName(wordname=word, times=times)
            dbcxn.add(wordRaw)
            dbcxn.flush()
            i += 1
            if i == 1000:
                dbcxn.commit()  # 每一千行提交一次
                i = 0
            else:
                continue
        else:
            pass


def words_Query(dbcxn, tableName):

    word_query = word_query = dbcxn.query(tableName).filter(tableName.is_valid != 0).all()
    for row in word_query:
        res = []
        for i in [row.wordname, row.times, row.phonogram, row.exp]:
            print(i)
            res.append(i)
        yield res


def wordsToCsv(res):

    with open('words.csv', 'a+', errors='ignore', newline='') as f:
        csvwrite = csv.writer(f)
        csvwrite.writerows(res)


def words_update(value, dbcxn, tableName):
    #print(value[0])
    word_query = dbcxn.query(tableName).filter(tableName.wordname == value[0]).one()
    #print(word_query.wordname, word_query.times)
    if not word_query.exp or not word_query.phonogram:
        word_query.exp = value[2]
        word_query.phonogram = value[3]
        if value[2] != 'none':
            word_query.is_valid = 1
        else:
            word_query.is_valid = 0
        dbcxn.flush()
    elif tableName.exp == 'none':
        print(word_query.wordname, word_query.times, word_query.exp)
    else:
        pass
        #print(word_query.wordname, word_query.times, word_query.exp)


def main():
    ''''''
    words = []
    wordRaws = 0
    except_list = ['we', 'you', 'she', 'he', 'am', 'is', 'are', 'was', 'were', 'your', 'may', 'can', 'and', 'or']
    filepath = 'E:\Data\englishexam2'
    filelist = os.listdir(filepath)
    for file in filelist:
        filename = os.path.join(filepath, file)
        words = words + wordsCollector.words_read(filename)
    words_filted = wordsCollector.words_filter(words, except_list)
    print(len(words), len(words_filted))
    words_times = wordsCollector.words_count(words_filted)
    if not os.path.isfile('words.db'):
        db.db_init()
    else:
        pass
    words = db.Words
    dbcxn = db.DBSession()
    #words_insert(words_times, dbcxn, words)   # 将分析出来的单词插入数据库
    for word, fre in words_times:
        phonogram, exp = wordsCollector.words_trans(word)
        #print(phonogram, exp)
        up_value = [word, fre, exp, phonogram]
        words_update(up_value, dbcxn, words)  # 更新查找到的单词解释
        wordRaws += 1
        if wordRaws == 1000:
            #print(wordRaws)
            dbcxn.commit()
            wordRaws = 0
        else:
            continue
    row = words_Query(dbcxn, words)
    count = 1
    wordsToCsv(['单词', '出现次数', '音标', '单词解释'])
    while True:
        try:
            #print(row)
            wordsToCsv(row)
        except:
            break
        count += 1
    dbcxn.close()


if __name__ == '__main__':
    main()
