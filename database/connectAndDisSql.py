import pymysql
from database.config import ConnectMySqlDict

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

    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
    cur = conn.cursor()

    return conn, cur

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
