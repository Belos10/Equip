from database.connectAndDisSql import *
def selectAllDataAboutFactory():
    sql = "select * from factory"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def haveFactoryName(name):
    sql = "select * from factory where name = '" + name + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def haveFactoryID(id):
    sql = "select * from factory where ID = '" + id + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def updateInfoIntoFactory(ID, name, address, connect, tel1, represent, tel2):
    sql = "update factory set address = '" + address + "', connect = '" \
          + connect + "', tel1 = '" + tel1 + "', represent = '" + represent + "', tel2 = '" + tel2\
          + "' where name = '" + name + "'"
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e

    sql = "update factory set Send_Connect = '" + connect + "', Send_Tel = '" \
          + tel1 + "' where Send_UnitName = '" + name + "'"
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e

def addInfoIntoFactory(ID, name, address, connect, tel1, represent, tel2):
    sql = "insert into factory(ID, name, address, connect, tel1, represent, tel2) values('" + ID + "', '" + name \
          + "', '" + address + "', '" + connect + "', '" + tel1 + "', '" + represent + "', '" + tel2 + "')"
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e

def selectAllNameAboutFactory():
    sql = "select name from factory"
    cur.execute(sql)
    result = cur.fetchall()
    resultList = []
    for resultInfo in result:
        resultList.append(resultInfo[0])
    return resultList