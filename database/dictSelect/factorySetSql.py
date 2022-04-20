from database.agentRoomSql import insertOneDataAgentRoom, findMaxId
from database.connectAndDisSql import *
def selectAllDataAboutFactory():
    sql = "select factory.ID, name, address, connect, tel1,agent_name,contact,phone_number,agent_id from factory  inner join agent_room on factory.agent_id = agent_room.id"
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

def updateInfoIntoFactory(ID, name, address, connect, tel1,agentRoomId):
    sql = "update factory set address = '%s', connect = '%s',tel1 = '%s',agent_id = '%d' where name = '%s'"%(address,connect,tel1,agentRoomId,name)
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e

    # sql = "update factory set Send_Connect = '" + connect + "', Send_Tel = '" \
    #       + tel1 + "' where Send_UnitName = '" + name + "'"
    # try:
    #     cur.execute(sql)
    #     conn.commit()
    #     return True
    # except Exception as e:
    #     return e

def addInfoIntoFactory(ID, name, address, connect, tel1, agentRoomId):
    sql = "insert into factory(ID, name, address, connect, tel1, agent_id) values('%s','%s','%s','%s','%s','%d')"%(ID,name,address,connect,tel1,agentRoomId)
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        return e

def delInfoFromFactory(ID):
    sql = "delete from factory where ID = '" + ID + "'"
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

def getFactoryById(id):
    sql = "select ID from factory where ID == '%s'"%id
    return executeSql(sql)
def getAgentRoomComboxDate():
    result = []
    sql = "select id,agent_name,contact,phone_number from agent_room order by id asc "
    data = executeSql(sql)
    if data != None:
        for item in data:
            result.append(item)
    return result

def insertOneDataFatorySet(lineInfo):
    try:
        insertOneDataAgentRoom(lineInfo[5])
        agentId = findMaxId()[0]
        factoryId = getFactoryById(lineInfo[0])
        if len(factoryId) > 0:
            updateInfoIntoFactory(lineInfo[0], lineInfo[1], lineInfo[2], lineInfo[3], lineInfo[4], agentId[0])
        else:
            addInfoIntoFactory(lineInfo[0], lineInfo[1], lineInfo[2], lineInfo[3], lineInfo[4],agentId[0])
        return True
    except Exception as e:
        print(e)
        return False