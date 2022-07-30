import sqlite3
from datetime import *


class record:
    def __init__(self):
        # 创建或打开一个数据库
        # check_same_thread 属性用来规避多线程操作数据库的问题
        self.conn = sqlite3.connect("recordinfo.db", check_same_thread=False)
        # 创建游标
        self.cursor = self.conn.cursor()
        # 建表
        self.conn.execute('create table if not exists record_table('
                          'id integer primary key autoincrement,'
                          'name varchar(30) ,'
                          'record_time timestamp,'
                          'img blob,'
                          'shape varchar(100))')

        self.conn.execute('create table if not exists name_table('
                          'id integer primary key autoincrement,'
                          'name varchar(30),'
                          'record_time timestamp)')

    # 插入数据
    def insert_record(self, name, img, shape):
        self.conn.execute('insert into record_table values (null, ?, ?, ?, ?)',
                          (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), img, shape))
        self.conn.commit()

    def insert_name(self, name):
        self.conn.execute('insert into name_table values (null, ?, ?)',
                          (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    # 搜索用户名
    def query_name(self):
        self.cursor.execute("select name from name_table")
        results = self.cursor.fetchall()
        name_list = []
        for i in results:
            i = list(i)
            name_list += i

        return name_list

    def query_nametable(self):
        self.cursor.execute("select * from name_table")
        results = self.cursor.fetchall()
        return results

    def query_simple_record(self):
        self.cursor.execute('select id,name,record_time from record_table')
        results = self.cursor.fetchall()
        return results

    def query_record(self):
        self.cursor.execute('select * from record_table')
        results = self.cursor.fetchall()
        return results

    def del_name(self, sname):
        self.conn.execute("delete from name_table where name = '{}'".format(sname))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
