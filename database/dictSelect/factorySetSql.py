from database.connectAndDisSql import *
def selectAllDataAboutFactory():
    sql = "select * from factory"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def haveFactoryID(id):
    sql = "select * from factory where ID = '" + id + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def addInfoIntoFactory(ID, name, address, connect, tel1, represent, tel2):
    sql = "insert into factory(ID, name, address, connect, tel1, represent, tel2) values('" + ID + "', '" + name \
          + "', '" + address + "', '" + connect + "', '" + tel1 + "', '" + represent + "', '" + tel2 + "')"
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e