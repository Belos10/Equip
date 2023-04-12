from database.connectAndDisSql import *
import operator
def getResultFromAgentRoom(agentRoomName,manufacturerName):
    result = []
    sql = "select * from agent_room  "
    if len(agentRoomName) != 0 or len(manufacturerName) != 0:
        if len(agentRoomName) != 0:
            sql = sql + "where agent_name like '%s' "%('%' + agentRoomName + '%')
        if len(agentRoomName) != 0 and len(manufacturerName) != 0:
            sql = sql +"and manufactor_name like '%s' "%('%' + manufacturerName + '%')
        elif len(agentRoomName) == 0 and len(manufacturerName) != 0:
            sql = sql + "where manufactor_name like '%s' "%('%' + manufacturerName +'%')

    else:
        sql = sql + "order by id asc"
    data = executeSql(sql)
    if data != None:
        for item in data:
            result.append(item)
    return result

def updateOneData(rowData):
    sql = "update agent_room set bureau_name = '%s',  agent_name = '%s', manufactor_name = '%s', contact = '%s', phone_number = '%s', region = '%s' where id = '%d'"\
          %(rowData[1],rowData[2],rowData[3],rowData[4],rowData[5], rowData[6], rowData[0])
    return executeCommit(sql)


def deleteDataById(id):
    sqls = []
    sql = "delete from agent_room where id = '%d'"%id
    sqls.append(sql)
    sql = "delete from factory where agent_id = '%d'"%id
    sqls.append(sql)
    return excuteupdata(sqls)

def insertOneDataAgentRoom(rowDate):
    sql = "insert into agent_room(bureau_name,agent_name,manufactor_name,contact,phone_number,region) values ('%s', '%s','%s','%s','%s','%s')"\
          %(rowDate[0],rowDate[1],rowDate[2],rowDate[3],rowDate[4], rowDate[5])
    return executeCommit(sql)

def getResultByAgentId(agentId):
    sql = "select bureau_name, agent_name, manufactor_name, contact, phone_number, region from agent_room where id = '%d'"%agentId
    return executeSql(sql)

def findMaxId():
    sql = "select max(id) from agent_room"
    return executeSql(sql)

if __name__ == '__main__':
    print(getResultByAgentId(19))
    pass