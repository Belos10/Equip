import pymysql
from database.connectAndDisSql import connectMySql, disconnectMySql

'''
    登录所涉及的表的sql
'''
'''
    功能：
        查询所有账号list
'''
def findAllLoginAccontList():
    conn, cur = connectMySql()
    sql = "select accont from login"

    cur.execute(sql)
    result = cur.fetchall()

    loginAccontList = []
    for accont in result:
        loginAccontList.append(accont[0])

    disconnectMySql(conn, cur)
    return loginAccontList

'''
    功能：
        根据账号返回用户信息
'''
def selectUserInfoByAccont(accont):
    conn, cur = connectMySql()
    sql = "select * from login where accont = '" + accont + "'"

    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)

    return result

'''
    功能：
        返回所有的登录用户信息
'''
def selectAllDataAboutLogin():
    conn, cur = connectMySql()
    sql = "select * from login "

    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)

    return result

def insertIntoLogin(accont, name, password, role, unitID):
    conn, cur = connectMySql()
    sql = "insert into login(accont,name,password,role,unitID) values " + \
          "('" + accont + "','" + name + "','" + password + \
          "','" + role + "','" + unitID + "')"
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

def delFromLogin(accont):
    conn, cur = connectMySql()
    sql = "delete from login where accont = '" + accont + "'"
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

def updateUserInfo(accont, name, password, role, unitID):
    conn, cur = connectMySql()
    sql = "update login set name = '" +  name + "', password = '" + password + "', role = '" + role\
          + "', unitID = '" + unitID + "' where accont = '" + accont + "'"
    print(sql)
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)