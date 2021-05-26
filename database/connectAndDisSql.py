import pymysql
from database.config import ConnectMySqlDict
import sqlite3
import os
'''
    功能：
        连接数据库，返回conn以及cur
'''
def connectMySql():
    host = ConnectMySqlDict.get('host')
    port = ConnectMySqlDict.get('port')
    user = ConnectMySqlDict.get('user')
    password = ConnectMySqlDict.get('password')
    db = ConnectMySqlDict.get('db')

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(os.path.join(BASE_DIR, 'NuclearManageSystem.db'))
    # cur = conn.cursor()
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
    cur = conn.cursor()

    return conn, cur
#new
'''
    功能：
        断开数据库的连接，需要传入conn以及cur
'''
def disconnectMySql(conn, cur):
    cur.close()
    conn.close()







'''
    功能：
        测试
'''
if __name__ == '__main__':
    conn, cur = connectMySql()
    disconnectMySql(conn, cur)
