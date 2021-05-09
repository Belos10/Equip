from pymysql.cursors import DictCursor

from database.connectAndDisSql import *
import operator
'''
执行sql语句，查询数据并以字典的形式保存
'''

def selectData(sql):
    conn, cur = connectMySql()
    cur.execute(sql)
    # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
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
def selectOne(sql):
    conn, cur = connectMySql()
    cur = conn.cursor(DictCursor)
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data





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
获取装备平衡表的年份并返回。
'''
def findYear():
    sql = "select year from equipment_balance group by year "
    data = selectData(sql)
    year = []
    for key in range(len(data)):
        year.append(data[key][0])

    return tuple(year)
'''
删除某一年度装备平衡表
'''
def deleteYear(year):
    sqlFindid = "select equip_balance_id from equipment_balance where year=%s"%year
    data = executeSql(sqlFindid)
    ids = []
    for key in range(len(data)):
        ids.append(data[key][0])
    for id in ids:
        sqlDelete = "delete from eb_quality_status where equip_balance_id=%s"%id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_change_project where equip_balance_id=%s"%id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_carry where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_stock where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_management where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_repair_time where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from equipment_balance where equip_balance_id=%s" % id
        executeCommit(sqlDelete)

def _dateSaveToList(dataDict):
    newDateList = []
    if dataDict is None or len(dataDict) is 0:
       pass
    else:
        for key in range(len(dataDict)):
            newDateList.append(dataDict[key][0])
    return newDateList




def getResultByYearAndEquip(year,equipList):
    resultList = []
    # print(equipList)
    if equipList is None:
        return resultList
    else:
        for equip in equipList:
            # print(equip)
            sql = "select equip_balance_id,Equip_ID from equipment_balance where year=%s and Equip_ID=%s"%(year,equip)
            result = selectDateDict(sql)
            # print(result)
            try:
                if len(result) is not 0:
                        for item in result:
                            itemDict = {}
                            sql = "select Equip_Name from equip where Equip_ID=%s"%item['Equip_ID']
                            itemDict.update(selectOne(sql))
                            sql = "select * from equipment_balance where equip_balance_id=%s"%item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_quality_status where equip_balance_id=%s"%item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_change_project where equip_balance_id=%s"%item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_carry where equip_balance_id=%s" % item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_stock where equip_balance_id=%s" % item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_management where equip_balance_id=%s" % item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_repair_time where equip_balance_id=%s" % item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            sql = "select * from eb_production_year where equip_balance_id=%s" % item['equip_balance_id']
                            itemDict.update(selectOne(sql))
                            resultList.append(itemDict)
                        return sorted(resultList,key=operator.itemgetter('Equip_ID'))

            except:
                return None


#根据年份、单位列表和装备列表定位申请退役表
def getDataByUnitIdAndEquipmentId(year,unitId,equipmentId):
    sql = "select apply_retirement_id,Equip_ID,Unit_ID,year,authorized_value,plan_to_retire,existing_value,apply_demand,note " \
          "from apply_retirement where year=%s and Unit_ID=%s and Equip_ID=%s"%(year, unitId, equipmentId)
    item = selectOne(sql)
    if(item is None or len(item) == 0):
        return None
    else:
        item['Equip_Name'] = getEquipmentNameByID(equipmentId)
        item['Unit_Name'] = getUnitNameByID(unitId)
        return item

def getEquipmentNameByID(equipmentId):
    if equipmentId is None:
        return None
    else:
        sql = "select Equip_Name from equip where Equip_ID=%s"%equipmentId
        data = selectOne(sql)
        if(data is not None):
            return data['Equip_Name']
        else:
            return None

def getEquipmentTypeByID(equipmentId):
    if equipmentId is None:
        return ''
    else:
        sql = "select Equip_Type from equip where Equip_ID=%s"%equipmentId
        data = selectOne(sql)
        if(data is None):
            return ''
        else:
            if (data['Equip_Type'] == '通用装备') :
                return '件'
            elif (data['Equip_Type'] == '专用装备'):
                return '辆'
            else:
                return ''

def getUnitNameByID(unitId):
    if unitId is None:
        return ''
    else:
        sql = "select Unit_Name from unit where Unit_ID=%s"%unitId
        data = selectOne(sql)
        if(data is None or len(data) == 0):
            return ''
        else:
            return data['Unit_Name']
















if __name__ == "__main__":
    unitList = ['3','4','5']
    equipList = ['1','2','3']

