from database.connectAndDisSql import *
import operator
def getResultFromRegularManage(name):
    result = []
    if len(name) != 0:
        sql = "select id,name, type,path,data from regular_manage where name like '%s' order by id asc"%('%' + name + '%')
    else:
        sql = "select id,name,type,path,data from regular_manage order by id asc"
    data = executeSql(sql)
    if data != None:
        for item in data:
            result.append(item)
    return result
def getCount():
    sql = "select count(*) from regular_manage"
    data  = executeSql(sql)
    if data != None:
        return data[0][0]
    else:
        return 0
def savaFile(name,type,dirctorPath,data):
    id = getCount()
    print(id)
    sql = "insert into regular_manage(id,name,type ,path,data) values ('%d','%s','%s','%s','%s')"%(id,name,type,dirctorPath,data)
    return executeCommit(sql)

def deleteFile(id):
    sql = "delete from regular_manage where id = '%d'"%id
    return executeCommit(sql)

if __name__ == '__main__':
    print(getCount())