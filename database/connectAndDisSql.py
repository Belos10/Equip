import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR ,'NuclearManageSystem.db'))
cur = conn.cursor()

'''
    功能：
        连接数据库，返回conn以及cur
'''
def connectSqlite():
    return conn, cur
#new
'''
    功能：
        断开数据库的连接，需要传入conn以及cur
'''
def disconnectSqlite():
    cur.close()
    conn.commit()
    conn.close()
    return

def selectData(sql):
    conn, cur = connectSqlite()
    cur.execute(sql)
    data = cur.fetchall()
    return data

def selectDateDict(sql):
    conn, cur = connectSqlite()
    data = cur.execute(sql)
    description = cur.description  # 获得游标所在表的信息 包含列名。
    column_name_list = []
    dataDict = []
    for i in description:
        column_name_list.append(i[0])
    for item in data:
        itemDict = {}
        for index in range(0, len(column_name_list)):
            # print(employee[index])
            itemDict[column_name_list[index]] = item[index]
        # print(employee_dict)
        dataDict.append(itemDict)
    return dataDict
'''
    功能：
        执行查找一条数据的sql语句，以字典的形式返回结果
'''
def selectOne(sql):
    data = selectDateDict(sql)
    if len(data) == 1:
        return data[0]
    else:
        return None


 #执行多条更新语句
def excuteupdata(sqls):
    if sqls is None or len(sqls) == 0:
        return False
    conn, cur = connectSqlite()
    for sql in sqls:
       executeCommit(sql)

'''
    功能：
        执行查询语句，以元组的方式返回查询到的数据
'''
def executeSql(sql):
    """执行sql语句，针对读操作返回结果集

        args：
            sql  ：sql语句
    """
    conn, cur = connectSqlite()
    try:
        cur.execute(sql)
        records = cur.fetchall()
        return records
    except sqlite3.Error as error:
        print(error)

def executeCommit(sql=''):
    """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚

    """
    conn, cur = connectSqlite()
    try:
        cur.execute(sql)
    except sqlite3.Error as error:
        conn.rollback()
        print(error)
        return error