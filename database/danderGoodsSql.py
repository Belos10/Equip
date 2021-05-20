from pymysql.cursors import DictCursor
from database.connectAndDisSql import *
import operator


def selectData(sql):
    conn, cur = connectMySql()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def selectDateDict(sql):
    conn, cur = connectMySql()
    cur = conn.cursor(DictCursor)
    cur.execute(sql)
    dataDict = cur.fetchall()
    cur.close()
    conn.close()
    return dataDict
'''
    功能：
        执行查找一条数据的sql语句，以字典的形式返回结果
'''
def selectOne(sql):
    conn, cur = connectMySql()
    cur = conn.cursor(DictCursor)
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data


 #执行多条更新语句
def excuteupdata(sqls):
    if sqls is None or len(sqls) == 0:
        return False
    conn, cur = connectMySql()
    for sql in sqls:
       executeCommit(sql)
    cur.close()
    conn.close()
'''
    功能：
        执行查询语句，以元组的方式返回查询到的数据
'''
def executeSql(sql):
    """执行sql语句，针对读操作返回结果集

        args：
            sql  ：sql语句
    """
    conn, cur = connectMySql()
    try:
        cur.execute(sql)
        records = cur.fetchall()
        return records
    except pymysql.Error as e:
        error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
        print(error)

def executeCommit(sql=''):
    """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚

    """
    conn, cur = connectMySql()
    try:
        cur.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        conn.rollback()
        error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
        print("error:", error)
        return error

'''
    功能：
        根据unit表初始化防化危险品目录
'''
def initDanderGoodsUnitDirectory():
    sql = "select Unit_ID,Unit_Name,Unit_Uper from dangergoods_unit_directory where Unit_Name like '%基地%'"
    units = executeSql(sql)
    if units is not None or len(units) != 0:
        for unit in units:
            insertOneDateIntoUnitDirectory(unit[0], unit[1], unit[2])
    pass

'''
    功能：
        向防化危险品目录表中插入单挑数据
'''
def insertOneDateIntoUnitDirectory(Unit_ID,Unit_Name,Unit_Uper):
    if not exists('dangergoods_unit_directory','Unit_ID',Unit_ID):
        sql = "insert into posengin_unit_directory values (%s,'%s',%s)"%(Unit_ID,Unit_Name,Unit_Uper)
        executeCommit(sql)

'''
    功能：
        判断某条数据是否存在在表中
'''
def exists(tableName,fieldName,fieldItem):
    sql = "select exists(select %s from %s where %s=%s) as 'result' "%(fieldName,tableName,fieldName,fieldItem)
    result =selectOne(sql)
    if result['result'] is 0:
        return False
    else:
        return True
