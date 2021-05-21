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
        通过单位号找到单位名字
        Unit_ID: 需要找的单位的ID号 
'''
def selectUnitNameByUnitID(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select Unit_Name from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    unitName = cur.fetchall()
    for name in unitName:
        return name[0]



'''
    功能获取单位表中各个单位的名字
'''
def getUnits():
    units = []
    sql = "select Unit_Name from posengin_unit_directory group by Unit_Name order by 'Unit_ID' desc "
    result = executeSql(sql)
    if result is not None or len(result) != 0:

        for unit in result:
            units.append(unit[0])
        return (units)
    else:
        return units

    pass
'''
    功能：
        从总的单位表中初始化阵地工程单位表，只包含基地一级以及下一级旅团。
'''
def initPosenginUnitDirectory():
    sql = "select Unit_ID,Unit_Name,Unit_Uper from unit where Unit_Name like '%基地%' or Unit_Name like '%旅团%' or Unit_Name like '%阵地%' "
    units = executeSql(sql)
    if units is not None or len(units) != 0:
        for unit in units:
            insertOneDateIntoUnitDirectory(unit[0],unit[1],unit[2])
'''
    功能：
        从总的装备表初始化阵地工程装备表，只选择专用装备及其附属装备。
'''
def initPosenginEquipmentDirectory():
    #一级目录
    sql = "select Equip_ID,Equip_Name,Equip_Uper,Input_Type,Equip_Type,unit from equip where Equip_Uper=''"
    specialEquipment = selectOne(sql)
    print(specialEquipment)
    if specialEquipment != None:
        insertOneDateIntoEquipmentDirectory(specialEquipment['Equip_ID'],specialEquipment['Equip_Name'],specialEquipment['Equip_Uper'],specialEquipment['Equip_Type'],specialEquipment['unit'])
        findChildEquipmenInsertIntoEquipmentDirectory(specialEquipment['Equip_ID'])


'''
    功能：
        寻找以某装备号作为上级装备的装备项
'''
def findChildEquipmenInsertIntoEquipmentDirectory(equipmentId):
    sql = "select Equip_ID,Equip_Name,Equip_Uper,Input_Type,Equip_Type,unit from equip where Equip_Uper=%s"%(equipmentId)
    findData = executeSql(sql)
    if findData != None:
        for data in findData:
            insertOneDateIntoEquipmentDirectory(data[0],data[1], data[2],data[3],data[4])
            findChildEquipmenInsertIntoEquipmentDirectory(data[0])

'''
    功能：
        向阵地工程目录表中插入单挑数据
'''
def insertOneDateIntoUnitDirectory(Unit_ID,Unit_Name,Unit_Uper):
    if not exists('posengin_unit_directory','Unit_ID',Unit_ID):
        sql = "insert into posengin_unit_directory values (%s,'%s',%s)"%(Unit_ID,Unit_Name,Unit_Uper)
        executeCommit(sql)

'''
    功能：
        向阵地工程装备表中插入一条记录
'''
def insertOneDateIntoEquipmentDirectory(Equip_ID,Equip_Name,Equip_Uper,Equip_Type,Unit_ID):
    if not exists('posengin_equipment_directory','Equip_ID',Equip_ID):
        sql = "insert into posengin_equipment_directory(Equip_ID,Equip_Name,Equip_Uper,Equip_Type,Unit_ID) values ('%s','%s','%s','%s','%s')"%(Equip_ID,Equip_Name,Equip_Uper,Equip_Type,Unit_ID)
        executeCommit(sql)
'''
    功能：
        查找某单位id所对应的单位数据
'''
def getUnitById(UnitID):
    sql = "select Unit_ID,Unit_Name,Unit_Uper from posengin_unit_directory where Unit_ID=%s"%UnitID
    return selectOne(sql)

def getUnitNameById(UnitID):
    sql = "select Unit_Name from posengin_unit_directory where Unit_ID=%s"%UnitID
    result = selectOne(sql)
    if result:
        return result['Unit_Name']
    else:
        return None

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
'''
    功能：
        根据基地、番号、阵地代号、装备到位情况进行筛选，返回符合记录
'''
def getResult(baseList,designationList,positionCodeLsit,prepareLsit):
    if len(baseList) == 0 and len(designationList) == 0 and len(positionCodeLsit) == 0 and len(prepareLsit) == 0:
        return findAllInstallactionData()
    elif  len(baseList) == 0 and (len(designationList) != 0 or len(positionCodeLsit) != 0 or len(prepareLsit) != 0):
        sql = "select installaction_Id,Unit_ID,official_designation,position_name,location,is_prepare,now_situation," \
              "installation_time,plan_time,count,prepare_situation,run_situation,notes from posengin_installation where "
        if len(designationList) != 0:
            sql = sql + "official_designation=%s "%(designationList[0])
        if len(positionCodeLsit)!= 0 and len(designationList) != 0 :
            sql = sql + "and position_name=%s "%positionCodeLsit[0]
        elif len(positionCodeLsit)!= 0 and len(designationList) == 0 :
            sql = sql + "position_name=%s " % positionCodeLsit[0]
        if len(prepareLsit) != 0 and (len(positionCodeLsit) + len(designationList)) >= 1:
            sql = sql + "and prepare_situation='%s'"%prepareLsit[0]
        else:
            sql = sql + "prepare_situation='%s'" % prepareLsit[0]

        return list(selectData(sql))
    elif len(baseList) != 0 and (len(designationList) != 0 or len(positionCodeLsit) != 0 or len(prepareLsit) != 0):
        data = []
        for base in  baseList:
            sql = "select installaction_Id,Unit_ID,official_designation,position_name,location,is_prepare,now_situation," \
                  "installation_time,plan_time,count,prepare_situation,run_situation,notes from posengin_installation where Unit_ID=%s "%base
            if len(designationList) != 0:
                sql = sql + "and official_designation='%s' " % (designationList[0])
            if len(positionCodeLsit)!= 0:
                sql = sql + "and position_name='%s' " % positionCodeLsit[0]
            if len(prepareLsit) != 0:
                sql = sql + "and prepare_situation='%s'" % prepareLsit[0]
            data.extend(list(selectData(sql)))
        return data
    elif len(baseList) != 0 and (len(designationList) + len(positionCodeLsit) + len(prepareLsit)) == 0:
        data = []
        for base in baseList:
            sql = "select installaction_Id,Unit_ID,official_designation,position_name,location,is_prepare,now_situation," \
                  "installation_time,plan_time,count,prepare_situation,run_situation,notes from posengin_installation where Unit_ID=%s " % base
            data.extend(list(selectData(sql)))
        return data


'''
    功能：
        获取阵地安装表所有记录
'''
def findAllInstallactionData():
    sql = "select installaction_Id,Unit_ID,official_designation,position_name,location,is_prepare,now_situation," \
          "installation_time,plan_time,count,prepare_situation,run_situation,notes from posengin_installation"
    return list(selectData(sql))
'''
    功能：
        根据单位名称获取对应单位id
'''
def getUnitIdbyName(unitName):
    sql = "select Unit_ID from posengin_unit_directory where Unit_Name='%s'"%unitName
    result = selectOne(sql)
    if result != None:
        return result['Unit_ID']
    else:
        return '-1'
'''
    功能：
        向表中插入一条数据
'''
def insertOneDataIntInstallation(rowData):
    sql = "insert into posengin_installation(Unit_ID,official_designation,position_name,location," \
          "is_prepare,now_situation,installation_time,plan_time,count,prepare_situation,run_situation,notes) " \
          "values('%s','%s','%s','%s',%d,'%s',%s,%s,%s,'%s','%s','%s')"%(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],
                                                          rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],
                                                          rowData[10],rowData[11])
    executeCommit(sql)
'''
    功能：
        根据序号更新安装表数据
'''
def updataOneDataIntInstallation(rowData):
    sql = "update posengin_installation set Unit_ID='%s',official_designation='%s',position_name='%s',location='%s'," \
          "is_prepare=%d,now_situation='%s',installation_time='%s',plan_time='%s',count=%s,prepare_situation='%s'," \
          "run_situation='%s',notes='%s' where installaction_Id='%s'"%(rowData[1],rowData[2],rowData[3],rowData[4],
                                                                       rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[12],rowData[0])
    executeCommit(sql)



'''
    功能：
        根据序号删除一行数据
'''
def deleteDataByInstallationId(installationId):
    sql = "delete from posengin_installation where installaction_Id='%s'" % installationId
    executeCommit(sql)



'''
    功能：
        根据装备id和单位id获取装备统计表中每条数据
'''
def getEquipmentStatisticsResultByUnitAndEquip(unit,equipment):
    sql = "select count,status from posengin_statistics where Unit_ID='%s' and Equip_ID='%s'"%(unit,equipment)
    data = executeSql(sql)
    #print("''''''''''''''", data)
    if data:
        return data[0]
    else:
        return None


#根据Dept_Uper查询单位信息,并返回
def selectUnitInfoByDeptUper(Unit_Uper):
    conn, cur = connectMySql()
    sql = "select * from posengin_unit_directory where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result

# 根据Equip_Uper查询单位信息,并返回
def selectEquipInfoByEquipUper(Equip_Uper):
    conn, cur = connectMySql()
    sql = "select * from posengin_equipment_directory where Equip_Uper = '" + Equip_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

#判断是否是基地
def isBase(unitId):
    sql = "select Unit_Name from posengin_unit_directory where Unit_ID='%s'"%unitId
    data = selectOne(sql)
    if data != None:
        unitName = data['Unit_Name']
        if '基地' in unitName:
            return True
        else:
            return False
    else:
        return False

    # 判断是否是旅团
def isBrigade(unitId):
    sql = "select Unit_Name from posengin_unit_directory where Unit_ID='%s'" % unitId
    data = selectOne(sql)
    if data != None:
        unitName = data['Unit_Name']
        if '旅团' in unitName:
            return True
        else:
            return False
    else:
        return False

   # 判断是否是阵地
def isPositions(unitId):
    sql = "select Unit_Name from posengin_unit_directory where Unit_ID='%s'" % unitId
    data = selectOne(sql)
    if data != None:
        unitName = data['Unit_Name']
        if '阵地' in unitName:
            return True
        else:
            return False
    else:
        return False

'''
    功能：
        判断单位的为几级单位
'''
def gradeOfUnit(UnitId):
    sql = "select Unit_Uper from posengin_unit_directory where Unit_ID='%s'"%UnitId
    data = selectOne(sql)
    if data != None:
        return gradeOfUnit(data['Unit_Uper']) + 1
    else:
        return 0

'''
    功能：
        找寻一个单位的上级单位
'''
def findUperUnit(unitId):
    sql =  "select Unit_Uper from posengin_unit_directory where Unit_ID='%s'"%unitId
    data = selectOne(sql)
    if data != None:
        return data['Unit_Uper']
    else:
        return None
'''
    功能：
        找寻一个单位的基地
'''
def findBase(unitID):
    if gradeOfUnit(unitID) < 3:
        pass
    elif gradeOfUnit(unitID) == 3 : #基地
        return unitID
    elif gradeOfUnit(unitID) == 4:  #旅团
        return  findUperUnit(unitID)
    elif gradeOfUnit(unitID) == 5:  #阵地
        uperId = findUperUnit(unitID)
        while gradeOfUnit(uperId) != 3:
            newUperId = findUperUnit(uperId)
            uperId = newUperId
        return  uperId
    elif gradeOfUnit(unitID) > 5:
        return None

'''
    功能：
        寻找一个单位的一级子单位
'''
def findChildUnit(unitId):

    sql = "select Unit_ID from posengin_unit_directory where Unit_Uper=%s"%unitId
    data = executeSql(sql)
    if data != None:
        result = []
        for item in data:
            result.append(item[0])
        if len(result) > 0:
            return result
        else:
            return None
    else:
        return None

'''
    功能：
        判断武器是否为最末级武器
'''

def isLastLevelEquipment(equipmentId):
    sql = "select Equip_ID from posengin_equipment_directory where Unit_ID='专用装备'  and Equip_Type='逐号录入' and Equip_ID=%s"%equipmentId
    result = executeSql(sql)
    if result != None:
        return True
    else:
        False

'''
    功能：
        根据装备Id获取装备名称
'''
def getEquipmentNameById(equipmentId):
    sql = "select Equip_Name from posengin_equipment_directory where Equip_ID='%s'"%equipmentId
    result = selectOne(sql)
    if result != None:
        return result['Equip_Name']

'''
    功能：
        得到装备的单位型号
'''
def getEquipmentUnitName(equipment):
    sql = "select unit from posengin_equipment_directory where Equip_ID='%s'"%equipment
    result = selectOne(sql)
    if result != None:
        return result['unit']

if __name__ == '__main__':
    data = ['3','003','钢铁雄心基地','xxxx',1,'准备到位','2020-06','2020-12',150,'未到位','未运行','无']
    print(initPosenginEquipmentDirectory())
    pass

