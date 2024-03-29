from database.connectAndDisSql import *
import operator

'''
    功能：
        根据unit表初始化防化危险品目录
'''
def initDanderGoodsUnitDirectory():
    sql = "select Unit_ID,Unit_Name,Unit_Uper from unit where Unit_Name like '%基地'"
    units = executeSql(sql)
    if units is not None or len(units) != 0:
        for unit in units:
            insertOneDateIntoUnitDirectory(unit[0], unit[1], unit[2])
    pass

'''
    功能：
        向防化危险品目录表中插入单挑数据
'''
def insertOneDateIntoUnitDirectory(Unit_ID,Unit_Name,Unit_Uper):
    if not exists('dangergoods_unit_directory','Unit_ID',Unit_ID):
        sql = "insert into dangergoods_unit_directory values (%s,'%s',%s)"%(Unit_ID,Unit_Name,Unit_Uper)
        executeCommit(sql)



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

#根据Dept_Uper查询单位信息,并返回
def selectUnitInfoByDeptUper(Unit_Uper):
    if gradeInUnit(Unit_Uper) < 3:
        conn, cur = connectSqlite()
        sql = "select * from unit where Unit_Uper = '" + Unit_Uper + "'"
        cur.execute(sql)
        result = cur.fetchall()
        # 测试结果
        # print(result)
        return result
    else:
        return []




'''
    功能：
        判断单位的为几级单位
'''
def gradeInUnit(UnitId):
    sql = "select Unit_Uper from unit where Unit_ID='%s'"%UnitId
    data = selectOne(sql)
    if data != None:
        return gradeInUnit(data['Unit_Uper']) + 1
    else:
        return 0
'''
    功能：
        根据单位Id从dangergoods表获取数据
'''
def getDataByUnit(unit):
    sql = "select * from dangergoods where Unit_ID='%s'"%unit
    data = executeSql(sql)
    if data != None:
        return data
    else:
        return None

def getUnitNameById(UnitID):
    sql = "select Unit_Name from unit where Unit_ID=%s"%UnitID
    result = selectOne(sql)
    if result != None :
        return result['Unit_Name']
    else:
        return None

'''
    功能：
        根据单位和类型返回数据
'''
def getDataByUnitAndType(unit,type):
    sql = "select * from dangergoods where Unit_ID='%s' and type='%s'"%(unit,type)
    result = executeSql(sql)
    if result != None:
        return result
    else:
        return None
'''
    功能：
        获取某单位的数据条数
'''
def getCountOfUnit(unitId):
    sql = "select count(*) from dangergoods where Unit_ID='%s'"%unitId
    result = selectOne(sql)
    if result != None or len(result) != 0:
        return result['count(*)']
    else:
        return None

'''
    功能：
        根据序号更新安装表数据
'''
def updataOneDataInDangerGood(rowData):
    print(rowData)
    sql = "update dangergoods set name = '%s', unit='%s',count='%s',subtotal = '%s'," \
          "new_product='%s',waste_product='%s',delivery_time='%s',storage_time='%s',source='%s',radioactivity='%s'," \
          "notes='%s' where goods_Id='%d'"%(rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[0])

    return executeCommit(sql)
'''
    功能：
        向表中插入一条数据
'''
def insertOneDataIntDangerGoods(rowData):
    print(rowData)
    sql = "insert into dangergoods(Unit_ID,type,name,unit,count,subtotal," \
          "new_product,waste_product,delivery_time,storage_time,source,radioactivity,notes) " \
          "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],
                                                          rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],
                                                          rowData[10],rowData[11],rowData[12])

    return  executeCommit(sql)
'''
    功能：
        删除表中一条数据
'''
def deleteByDangerGoodsId(dangerGoodsId):
    sql = "delete from dangergoods where goods_Id='%s'"%dangerGoodsId
    executeCommit(sql)
    return True
'''
    获取某基地所属的旅团
'''
def getBrigadesByBaseId(baseId):
    children = findChildUnit(baseId)
    brigades = []
    for child in children:
        if gradeInUnit(child) == 4:
            temp = getUnit(child)
            if len(temp) > 1:
                brigades.append(temp.copy())
    return brigades

'''
    功能：
        寻找一个单位的一级子单位
'''
def findChildUnit(unitId):
    result = []
    sql = "select Unit_ID from unit where Unit_Uper=%s"%unitId
    data = executeSql(sql)
    if data != None:
        for item in data:
            result.append(item[0])
    return result

'''
    功能：
        根据单位号返回单位的信息
'''
def getUnit(unitId):
    result = {}
    sql = "select Unit_ID,Unit_Name from unit where Unit_ID='%s'"%unitId
    data =selectOne(sql)
    if data != None:
        result['Unit_ID'] = data['Unit_ID']
        result['Unit_Name'] = data['Unit_Name']
    return result
'''
    功能：
        返回某个旅团的所有阵地
'''
def getpositionsByPositionId(PositionId):
    children = findChildUnit(PositionId)
    Positions = []
    for child in children:
        if gradeInUnit(child) == 5:
            temp = getUnit(child)
            if len(temp) > 1:
                Positions.append(temp.copy())
    return Positions

    pass

if __name__ == '__main__':
    print(getpositionsByPositionId('6'))
    pass