# -*- coding: utf-8 -*-

import mysql.connector

def get_data(id):
    conn = mysql.connector.connect(user='root', passwd='root', db='eulampis')   

    cursor = conn.cursor()
    cursor.execute('select * from weibo where id=' + str(id))
    values = cursor.fetchall()

    cursor.close()
    conn.close()

    return values


if __name__ == '__main__':
    print(get_data(1)[0][1])