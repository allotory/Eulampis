# -*- coding: utf-8 -*-

import mysql.connector

def get_data():
    conn = mysql.connector.connect(user='root', passwd='root', db='eulampis')   

    cursor = conn.cursor()
    cursor.execute('select wb_index from weibo_index where id=1')
    index = cursor.fetchall()
    print(index[0][0])

    cursor = conn.cursor()
    cursor.execute('select * from weibo where id=' + str(index[0][0]))
    values = cursor.fetchall()

    cursor = conn.cursor()
    cursor.execute('update weibo_index set wb_index=' + str(index[0][0] + 1))

    cursor.close()
    conn.commit()
    conn.close()

    return values


if __name__ == '__main__':
    print(get_data()[0][1])