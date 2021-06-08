import sqlite3
import os
import pymysql
from database.config import ConnectMySqlDict


#os.path.join(BASE_DIR ,'NuclearManageSystem.db')


try:
    # basepath = os.path.abspath(os.path.dirname(__file__))
    basepath = os.path.split(os.path.realpath(__file__))[0]
    # basepath = os.path.dirname(os.path.abspath(__file__))
    # basepath = os.path.dirname(os.path.realpath(__file__))
    # curpath = os.path.realpath(__file__)
    # basepath = os.path.dirname(curpath)
    # path = basepath + '\\NuclearManageSystem.db'
    # print('路径',path)
    # # conn = sqlite3.connect(path)
    conn = sqlite3.connect('NuclearManageSystem.db')
    cur = conn.cursor()
except sqlite3.OperationalError:
    # basepath = os.path.abspath(os.path.dirname(__file__))
    # # basepath = os.path.split(os.path.realpath(__file__))[0]
    # # basepath = os.path.dirname(os.path.abspath(__file__))
    # # basepath = os.path.dirname(os.path.realpath(__file__))
    # os.mkdir(basepath)
    print("异常")
finally:
    # assert os.path.exists(basepath)
    # path = basepath + 'database\\NuclearManageSystem.db'
    # # print(path)
    # conn = sqlite3.connect(path)
    # cur = conn.cursor()

    pass



# host = ConnectMySqlDict.get('host')
# port = ConnectMySqlDict.get('port')
# user = ConnectMySqlDict.get('user')
# password = ConnectMySqlDict.get('password')
# db = ConnectMySqlDict.get('db')
#
# conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
# cur = conn.cursor()

'''
    功能：
        连接数据库，返回conn以及cur
'''
def connectSqlite():
    return conn, cur

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
    try:
        for sql in sqls:
            cur.execute(sql)
        conn.commit()
        return True
    except sqlite3.Error as error:
        conn.rollback()
        print(error)
        return False

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
        conn.commit()
    except sqlite3.Error as error:
        conn.rollback()
        print(error)
        return error
#初始化
def initTables():
    pass
if __name__ == '__main__':
    # executeCommit("delete into equipment_balance(equip_balance_id) values('001')")
    pass