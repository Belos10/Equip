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
 #执行多条更新语句
def excuteupdata(sqls):
    if sqls is None or len(sqls) == 0:
        return False
    conn, cur = connectMySql()
    for sql in sqls:
       executeCommit(sql)
    cur.close()
    conn.close()







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
        if(len(data[key][0]) <= 1):
            continue
        else:
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
    if equipList is None:
        return resultList
    else:
        for equip in equipList:
            item = {}
            sql = "select equip_balance_id,Equip_ID from equipment_balance where year=%s and Equip_ID=%s"%(year,equip)
            result = selectOne(sql)
            if result is None:
                item['Equip_ID'] = equip
                item['Equip_Name'] = getEquipmentNameByID(equip)
                resultList.append(item.copy())
                item.clear()
                continue
            else:
                sql = "select Equip_Name from equip where Equip_ID=%s" % result['Equip_ID']
                item.update(selectOne(sql))
                sql = "select * from equipment_balance where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_quality_status where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_change_project where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_carry where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_stock where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_management where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_repair_time where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                sql = "select * from eb_production_year where equip_balance_id=%s" % result['equip_balance_id']
                item.update(selectOne(sql))
                resultList.append(item.copy())
                item.clear()
        return resultList


 #实力表中的内容初始化装备平衡表
def initEquipmentBalance(year):
    #保存插入装备平衡表的每一项的OrignalAuthorizedValue、authorizedValue、authorizedValueChange、originalValue
    itemDict = {}
    sqls = []
    item = {}


    sql = "select Equip_ID,Unit_ID,Work from strength where year=%s and equipYear='' "%(str(year))
    equipmentsWork = selectDateDict(sql)
    if(equipmentsWork is not None): #添加
        orderedEquipmentWork = sorted(equipmentsWork,key=operator.itemgetter('Equip_ID'))
        for workItem in orderedEquipmentWork:
            OrignalAuthorizedValue = int(workItem.get('Work',0))
            item['Equip_ID'] = workItem['Equip_ID']
            item['Unit_ID'] = workItem['Unit_ID']
            item['OrignalAuthorizedValue'] = OrignalAuthorizedValue
            item['authorizedValue'] = 0
            item['authorizedValueChange'] = 0
            item['originalValue'] = 0
            key = str(year) + item['Equip_ID'] + item['Unit_ID']
            itemDict[key] = item.copy()
            item.clear()

    sql = "select Equip_ID,Unit_ID,Strength from strength where year=%s and equipYear='' " % (str(int(year) - 1))
    equipmentsLastYearWork = selectDateDict(sql)
    if(equipmentsLastYearWork is not None):
        orderedEquipmentsLastYearWork = sorted(equipmentsLastYearWork,key=operator.itemgetter('Equip_ID'))
        for oldWork in orderedEquipmentsLastYearWork:
            originalValue = int(oldWork.get('Strength', 0))
            item['Equip_ID'] = oldWork['Equip_ID']
            item['Unit_ID'] = oldWork['Unit_ID']
            item['OrignalAuthorizedValue'] = 0
            item['authorizedValue'] = 0
            item['authorizedValueChange'] = 0
            item['originalValue'] = originalValue
            key = str(year) + item['Equip_ID'] + item['Unit_ID']
            equip = itemDict.get(key)
            if(equip is not None):
                equip['originalValue'] = originalValue
            else:
                itemDict[key] = item.copy()
            item.clear()


    sql = "select Equip_Id,Unit_Id,DisturbNum from disturbplan where Year=%s"%(str(year))
    disturbList = selectDateDict(sql)
    if(disturbList is not None):
        ordereddisturbList = sorted(disturbList,key=operator.itemgetter('Equip_Id'))
        for disturbItem in ordereddisturbList:
            if(disturbItem.get('DisturbNum',0) == 0 or disturbItem['DisturbNum'] is None or len(disturbItem['DisturbNum']) <= 1):
                disturbValue = 0
            else:
                disturbValue = int(disturbItem['DisturbNum'])
            item['Equip_ID'] = disturbItem['Equip_Id']
            item['Unit_ID'] = disturbItem['Unit_Id']
            item['OrignalAuthorizedValue'] = 0
            item['authorizedValue'] = 0
            item['authorizedValueChange'] = disturbValue
            item['originalValue'] = 0
            key = str(year) + item['Equip_ID'] + item['Unit_ID']
            equip = itemDict.get(key)
            if (equip is not None):
                equip['authorizedValueChange'] = disturbValue
                equip['authorizedValue'] = equip.get('authorizedValue') + disturbValue
            else:
                itemDict[key] = item.copy()
            item.clear()

    if len(itemDict) != 0:
        for key in itemDict.keys():
            tempItem = itemDict.get(key)
            equipKey = key
            sql = "insert into equipment_balance(equip_balance_id,Equip_ID,Unit_ID,year,original_authorized_value," \
                  "authorized_value,authorized_value_change,original_value) values (%s,%s,%s,%s,%d,%d,%d,%d)" % (
            equipKey, tempItem['Equip_ID'],tempItem['Unit_ID'],str(year), tempItem['OrignalAuthorizedValue'],
            tempItem['authorizedValue'],tempItem['authorizedValueChange'],tempItem['originalValue'],)
            sqls.append(sql)
            sql1 = "insert into eb_carry(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql1)
            sql2 = "insert into eb_change_project(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql2)
            sql3 = "insert into eb_management(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql3)
            sql4 = "insert into eb_production_year(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql4)
            sql5 = "insert into eb_quality_status(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql5)
            sql6 = "insert into eb_repair_time(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql6)
            sql7 = "insert into eb_stock(equip_balance_id) value(%s)" % equipKey
            sqls.append(sql7)
            excuteupdata(sqls)
            sqls.clear()



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
def getEquipmentIdByName(equipmentName):
    sql = "select Equip_ID from equip where Equip_Name='%s'"%equipmentName
    equipment = selectOne(sql)
    return equipment['Equip_ID']

def getEquipmentBalanceIdByEquipmentId(equipmentId,year):
    sql = "select equip_balance_id from equipment_balance where Equip_ID=%s and year=%s"%(equipmentId,year)
    data = selectOne(sql)
    if data is None:
        return None
    else:
        return data['equip_balance_id']

def update(tableName,fieldName,fieldVlaue,equipmentBalanceId):
    sql = "update %s set %s=%s where equip_balance_id=%s"%(tableName,fieldName,fieldVlaue,equipmentBalanceId)
    executeCommit(sql)


def saveEquipmentBalanceByRow(dataList,year):
    equipmentBalanceId = getEquipmentBalanceIdByEquipmentId(getEquipmentIdByName(dataList[0]),year)
    if equipmentBalanceId is not None:
        print(dataList)
        executeCommit("update eb_quality_status set issue_new_product=%s,issue_inferior_product=%s, issue_need_repaired=%s,"
                 "issue_need_retire=%s,report_new_product=%s,report_inferior_product=%s,report_need_repaired=%s,"
                 "report_need_retire=%s where equip_balance_id=%s " % (dataList[5],dataList[6],dataList[7],dataList[8],
                                                                       dataList[9],dataList[10],dataList[11],dataList[12],equipmentBalanceId))
        executeCommit("update equipment_balance set change_value=%s,existing_value=%s where equip_balance_id=%s " % (
        dataList[13], dataList[14],equipmentBalanceId))
        executeCommit("update eb_change_project set increase_count=%s,increase_superior_supplement=%s,increase_model_change=%s,"
                 "increase_missing_reports=%s,increase_self_purchase=%s,increase_transfer_in=%s,increase_other=%s,reduce_count=%s,"
                 "reduce_model_change=%s,reduce_callout=%s,reduce_train_consumption=%s,reduce_restatement=%s,reduce_retire=%s,"
                 "reduce_scrap=%s,reduce_other=%s where equip_balance_id=%s " % (
        dataList[15],dataList[16],dataList[17],dataList[18],dataList[19],dataList[20],dataList[21],dataList[22],dataList[23],dataList[24],
        dataList[25],dataList[26],dataList[27],dataList[28],dataList[29],equipmentBalanceId))
        executeCommit("update equipment_balance set unprepared_value=%s,unmatched_value=%s,uncutdown_value=%s where equip_balance_id=%s " % (
        dataList[30],dataList[31],dataList[32], equipmentBalanceId))
        executeCommit("update eb_carry set carry_count=%s,carry_new_product=%s,carry_inferior_product=%s,carry_need_repaired=%s,"
                 "carry_need_retire=%s,carry_unprepared_value=%s,carryUn_cutdown_value=%s where equip_balance_id=%s " % (
        dataList[33],dataList[34],dataList[35],dataList[36],dataList[37],dataList[38],dataList[39], equipmentBalanceId))
        executeCommit("update eb_stock set stock_count=%s,stock_new_product=%s,stock_inferior_product=%s,stock_need_repaired=%s,stock_need_retire=%s,"
                 "stock_unprepared_value=%s,stockUn_cutdown_value=%s where equip_balance_id=%s " % (
        dataList[40],dataList[41],dataList[42],dataList[43],dataList[44],dataList[45],dataList[46], equipmentBalanceId))
        executeCommit("update eb_management set authorized_rate=%s,instock_rate=%s,matched_rate=%s,prepared_rate=%s,intact_rate=%s where equip_balance_id=%s " % (
        dataList[47], dataList[48], dataList[49], dataList[50],dataList[51], equipmentBalanceId))
        executeCommit("update eb_repair_time set never_repair=%s,once=%s,twice=%s,three_times=%s,More_than_three=%s where equip_balance_id=%s " % (
        dataList[52],dataList[53],dataList[54],dataList[55],dataList[56], equipmentBalanceId))
        executeCommit(
        "update eb_production_year set before1970=%s,between1971and1975=%s,between1976and1980=%s,between1981and1985=%s,"
        "between1986and1990=%s,between1991and1995=%s,between1996and2000=%s,between2001and2005=%s,after2006=%s where equip_balance_id=%s " % (
           dataList[57], dataList[58], dataList[59], dataList[60], dataList[61],dataList[62],dataList[63],dataList[64],dataList[65], equipmentBalanceId))


if __name__ == "__main__":
    getEquipmentIdByName('装备')


