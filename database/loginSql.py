import pymysql
from database.connectAndDisSql import *

'''
    登录所涉及的表的sql
'''
'''
    功能：
        查询所有账号list
'''
def findAllLoginAccontList():
    sql = "select accont from login"

    cur.execute(sql)
    result = cur.fetchall()

    loginAccontList = []
    for accont in result:
        loginAccontList.append(accont[0])
    return loginAccontList

'''
    功能：
        根据账号返回用户信息
'''
def selectUserInfoByAccont(accont):
    sql = "select * from login where accont = '" + accont + "'"

    cur.execute(sql)
    result = cur.fetchall()

    return result

'''
    功能：
        返回所有的登录用户信息
'''
def selectAllDataAboutLogin():
    sql = "select * from login "

    cur.execute(sql)
    result = cur.fetchall()

    return result

def insertIntoLogin(accont, name, password, role, unitID):
    sql = "insert into login(accont,name,password,role,unitID) values " + \
          "('" + accont + "','" + name + "','" + password + \
          "','" + role + "','" + unitID + "')"
    cur.execute(sql)

    conn.commit()

def delFromLogin(accont):
    sql = "delete from login where accont = '" + accont + "'"
    cur.execute(sql)

    conn.commit()

def updateUserInfo(accont, name, password, role, unitID):
    sql = "update login set name = '" +  name + "', password = '" + password + "', role = '" + role\
          + "', unitID = '" + unitID + "' where accont = '" + accont + "'"
    print(sql)
    cur.execute(sql)

    conn.commit()