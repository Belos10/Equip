from database.connectAndDisSql import *
from database.SD_EquipmentBanlanceSql import updateOneEquipmentBalanceData, deleteByYear, getFomatEquipmentName

#new

'''
    实力分布所涉及的表的sql
'''
'''
    功能：
        找到某个单位的所有下级单位
        Unit_ID: 需要找的单位的ID号
        childUnitList：存放该单位所有下级单位，包括自己，自己在0位置
        cur：执行sql语句
'''
def findChildUnit(Unit_ID, childUnitList, space):
    unitInfo = selectUnitInfoByUnitID(Unit_ID)
    if unitInfo:
        unit = list(unitInfo)
        unit[1] = space + unit[1]
        childUnitList.append(unit)
    sql = "select * from unit where Unit_Uper = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        return e
    ID_tuple = cur.fetchall()
    space = space + "   "
    for ID in ID_tuple:
        findChildUnit(ID[0], childUnitList, space)
    return True


def findChildDisturbPlanUnit(Unit_ID, childUnitList, cur):
    childUnitList.append(Unit_ID)
    if Unit_ID != '':
        sql = "select Unit_ID from disturbplanunit where Unit_Uper = '" + Unit_ID + "'"
        cur.execute(sql)
        ID_tuple = cur.fetchall()
        for ID in ID_tuple:
            findChildDisturbPlanUnit(ID[0], childUnitList, cur)
    else:
        return

def selectPubilcEquipInfoByGroup(Unit_ID):
    sql = "select * from publicequip where Group_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

'''
    功能：
        查询编制表时找到某个单位的所有下级单位
        Unit_ID: 需要找的单位的ID号
        childUnitList：存放该单位所有下级单位，包括自己，自己在0位置
        cur：执行sql语句
'''
def findChildUnitByWeave(Unit_ID, childUnitList, space):
    isGroup = selectUnitIsGroup(Unit_ID)
    if isGroup:
        publicEquipInfo = selectPubilcEquipInfoByGroup(Unit_ID)
        if publicEquipInfo:
            unitInfo = selectUnitInfoByUnitID(Unit_ID)
            unit = list(unitInfo)
            childUnitList.append(unit)
            publicEquip = list(publicEquipInfo[0])
            publicEquip[1] = space + "  " + "公用装备"
            unit[1] = space + unit[1]
            childUnitList.append(publicEquip)
        else:
            unitInfo = selectUnitInfoByUnitID(Unit_ID)
            unit = list(unitInfo)
            unit[1] = space + unit[1]
            childUnitList.append(unit)
        sql = "select Unit_ID from unit where Unit_Uper = '" + Unit_ID + "'"
        cur.execute(sql)
        ID_tuple = cur.fetchall()
        space = space + "   "
        for ID in ID_tuple:
            findChildUnitByWeave(ID[0], childUnitList, space)


'''
    功能：
        找到某个装备的所有下级单位
        Unit_ID: 需要找的装备的ID号
        childUnitList：存放该单位所有下级装备，包括自己，自己在0位置
        cur：执行sql语句
'''
def findChildEquip(Equip_ID, childEquipList, space):
    equipInfo = selectEquipInfoByEquipID(Equip_ID)
    if equipInfo:
        equip = list(equipInfo[0])
        equip[1] = space + equip[1]
        childEquipList.append(equip)
    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        return e
    ID_tuple = cur.fetchall()
    space = space + "   "
    for ID in ID_tuple:
        findChildEquip(ID[0], childEquipList, space)
    return True

#找到所有子项的ID
def findChildEquipIDList(Equip_ID, childEquipList):

    childEquipList.append(Equip_ID)
    sql = "select Equip_ID from equip where Equip_Uper = '" + Equip_ID + "'"
    cur.execute(sql)
    ID_tuple = cur.fetchall()
    for ID in ID_tuple:
        findChildEquipIDList(ID[0], childEquipList)

#找到所有最子项
def findChildNodeEquipIDList(Equip_ID):
    childEquipList = []
    findChildEquipIDList(Equip_ID, childEquipList)

    nodeList = []
    for equipID in childEquipList:
        if selectEquipIsHaveChild(equipID):
            pass
        else:
            nodeList.append(equipID)
    return nodeList


# 找到所有子项的ID
def findChildUnitIDList(Unit_ID, childUnitList):
    childUnitList.append(Unit_ID)
    sql = "select Unit_ID from unit where Unit_Uper = '" + Unit_ID + "'"
    cur.execute(sql)
    ID_tuple = cur.fetchall()
    for ID in ID_tuple:
        findChildUnitIDList(ID[0], childUnitList)


# 找到所有最子项
def findChildNodeUnitIDList(Unit_ID):
    childUnitList = []
    findChildUnitIDList(Unit_ID, childUnitList)

    nodeList = []
    for unitID in childUnitList:
        if selectUnitIsHaveChild(unitID):
            pass
        else:
            nodeList.append(unitID)
    return nodeList
'''
    功能：
        通过单位号找到单位名字
        Unit_ID: 需要找的单位的ID号 
'''
def selectUnitNameByUnitID(Unit_ID):
    cur = conn.cursor()
    sql = "select Unit_Name from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    unitName = cur.fetchall()
    for name in unitName:
        return name[0]


'''
    功能：
        通过单位号找到装备名字
        Unit_ID: 需要找的装备的ID号 
'''
def selectEquipNameByEquipID(Equip_ID):
    cur = conn.cursor()
    sql = "select Equip_Name from equip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    equipName = cur.fetchall()
    for name in equipName:
        return name[0]


'''
    功能：
        判断装备是否是最底层装备
'''
def EquipNotHaveChild(Equip_ID):
    #conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    #cur = conn.cursor()
    # 插入的sql语句
    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return False
    else:
        return True


'''
    功能：
        判断单位是否是最底层单位
'''
def UnitNotHaveChild(Unit_ID):
    # 插入的sql语句
    sql = "select * from unit where Unit_Uper = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return False
    else:
        return True

'''
    功能：
        找到某个单位的一级上级单位
'''
def selectUnitDictByUper(Unit_Uper):
    sql = "select * from unit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
    data = cur.fetchall()
    return data


'''
    功能：
        增加装备目录
'''
def add_UnitDictEquip(Equip_ID, Equip_Name, Equip_Uper):
    # 插入的sql语句
    sql = "INSERT INTO equip (Equip_ID, Equip_Name, Equip_Uper) VALUES" \
          + "('" + Equip_ID + "','" + Equip_Name + "','" + Equip_Uper + "')"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()


# 更改装备目录
def update_Equip_Dict(Equip_ID, Equip_Name, Equip_Uper):
    # 插入的sql语句
    sql = "Update equip set Equip_Name = '" + Equip_Name + "', Equip_Uper = '" + Equip_Uper \
          + "' where Equip_ID = '" + Equip_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()


# 删除装备及子目录
def del_Equip_And_Child(Equip_ID, Equip_Uper):
    # 插入的sql语句
    sql = "delete from equip where Equip_ID = '" + Equip_ID + "'" + "and Equip_Uper = '" + Equip_Uper + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()


#根据Dept_Uper查询单位信息,并返回
def selectUnitInfoByDeptUper(Unit_Uper):
    sql = "select * from unit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


#根据Dept_Uper查询单位信息,并返回
def selectDisturbPlanUnitInfoByDeptUper(Unit_Uper):
    sql = "select * from disturbplanunit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 返回disturbplanunit单位表的所有数据
def selectAllDataAboutDisturbPlanUnit():
    sql = "select * from disturbplanunit order by Unit_ID"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 返回disturbplanunit单位表除机关外的所有数据
def selectAllDataAboutDisturbPlanUnitExceptFirst():
    sql = "select * from disturbplanunit where Unit_Uper != ''"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 返回unit单位表的所有数据
def selectAllDataAboutUnit(resultList):
    sql = "select * from unit order by Unit_ID"
    try:
        cur.execute(sql)
    except Exception as e:
        return e
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(resultInfo)
    return True


# 根据Equip_Uper查询单位信息,并返回
def selectEquipInfoByEquipUper(Equip_Uper):

    sql = "select * from equip where Equip_Uper = '" + Equip_Uper + "'"

    cur.execute(sql)
    result = cur.fetchall()
    return result
# 根据Equip_Uper查询信息,并返回
def selectSpecialEquipmentInfoByEquipUper(Equip_Uper):
    sql = "select * from equip where Equip_Uper = '%s' and Equip_Type = '专用装备'"%Equip_Uper
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectGeneralEquipmentInfoByEquipUper(Equip_Uper):
    sql = "select * from equip where Equip_Uper = '%s' and Equip_Type = '通用装备'"%Equip_Uper
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 返回publicequip的所有数据
def selectAllDataAboutPublicEquip():
    resultList = []
    sql = "select * from publicequip"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(resultInfo)
    return resultList

# 返回equip装备表的所有数据
def selectAllDataAboutEquip():
    resultList = []
    sql = "select * from equip"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(list(resultInfo))
    return resultList


def addDataIntoDisturbPlanUnit(Unit_ID, Unit_Name, Unit_Uper):
    sql = "INSERT INTO disturbplanunit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', '' ,Is_Group = '否')"
    cur.execute(sql)
    conn.commit()

# 读取分配计划年份
def selectYearListAboutDisturbPlan():
    yearList = []
    sql = "select * from disturbplanyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList



# 读取分配计划年份
def selectYearListAboutOrderPlan():
    yearList = []
    sql = "select * from orderallotplanyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


def selectYearListAboutRetirePlan():
    #conn, cur = connectMySql()
    yearList = []
    sql = "select * from retireplanyear order by year"

    cur.execute(sql)
    result = cur.fetchall()

    #disconnectMySql(conn, cur)
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 读取分配计划年份
def selectYearListAboutOrderRetirePlan():
    yearList = []
    sql = "select * from orderretireplanyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 读取订购调整计划年份
def selectYearListAboutOrderAdjust():
    yearList = []
    sql = "select * from orderadjustyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 往单位表unit中插入一条数据
def addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper, Unit_Alias, Is_Group):
    # 插入的sql语句
    sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', '" + Unit_Alias + "', '" + Is_Group + "')"
    # 执行sql语句，并发送给数据库
    try:
        cur.execute(sql)
    except Exception as e:
        return False

    sql = "INSERT INTO disturbplanunit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','"  + Unit_Uper + "', '" + Unit_Alias + "', '" + Is_Group + "')"

    try:
        cur.execute(sql)
    except Exception as e:
        return False
    equipInfoTuple = selectAllDataAboutEquip()
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    disturbplanYearInfoTuple = selectYearListAboutDisturbPlan()
    orderallotplanYearInfoTuple = selectYearListAboutOrderPlan()
    retireplanYearInfoTuple = selectYearListAboutRetirePlan()
    orderretireplanYearInfoTuple = selectYearListAboutOrderRetirePlan()
    for equipInfo in equipInfoTuple:
        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', 0," \
                                                                                                           " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                      strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + Unit_ID + "','" + equipInfo[0] + "','" + Unit_Name + "','" + equipInfo[
                      1] + "', 0, 0, 0, '" + strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            sql = "INSERT INTO strength_maintance (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Plan_Unhanded, year) VALUES" \
                  + "('" + Unit_ID + "','" + equipInfo[0] + "','" + Unit_Name + "','" + equipInfo[
                      1] + "', 0, '" + strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for disturbplanYearInfo in disturbplanYearInfoTuple:
            sql = "insert into disturbplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " \
                  + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + Unit_ID + \
                  "','" + Unit_Name + "','" + disturbplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for orderallotplanYearInfo in orderallotplanYearInfoTuple:
            sql = "insert into orderallotplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,OrderNum) values " \
                  + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + Unit_ID + \
                  "','" + Unit_Name + "','" + orderallotplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for retireplanYearInfo in retireplanYearInfoTuple:
            sql = "insert into retireplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " \
                  + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + Unit_ID + \
                  "','" + Unit_Name + "','" + retireplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for orderretireplanYearInfo in orderretireplanYearInfoTuple:
            sql = "insert into orderretireplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " \
                  + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + Unit_ID + \
                  "','" + Unit_Name + "','" + orderretireplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e
#往装备单位信息表插入一条数据
def addDataIntoEquipUnitInfo(Equip_ID, Equip_Unit_Info):
    sql = "INSERT INTO equip_unit_info (Equip_ID, Unit_Info) VALUES ('%s', '%s')"%(Equip_ID, Equip_Unit_Info)

    return executeCommit(sql)

# 往装备表equip中插入一条数据
def addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, Equip_Unit):
    # 插入的sql语句
    sql = "INSERT INTO equip (Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, unit) VALUES" \
          + "('" + Equip_ID + "','" + Equip_Name + "','" + Equip_Uper + "','" + Input_Type + "','" + Equip_Type + "', '"\
          + Equip_Unit + "')"
    # 执行sql语句，并发送给数据库
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    publicEquipInfoList = selectAllDataAboutPublicEquip()
    unitInfoTuple = []
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    selectSuccess = selectAllDataAboutUnit(unitInfoTuple)
    if selectSuccess != True:
        return selectSuccess
    disturbplanYearInfoTuple = selectYearListAboutDisturbPlan()
    orderallotplanYearInfoTuple = selectYearListAboutOrderPlan()
    retireplanYearInfoTuple = selectYearListAboutRetirePlan()
    orderretireplanYearInfoTuple = selectYearListAboutOrderRetirePlan()
    orderadjustYearInfoTuple = selectYearListAboutOrderAdjust()
    for publicEquip in publicEquipInfoList:
        for strengthYearInfo in strengthYearInfoTuple:

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + publicEquip[0] + "','" + Equip_ID + "','" + "公用装备" + "','" + Equip_Name + "', 0, 0, 0, '" + \
                  strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

    for unitInfo in unitInfoTuple:
        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
                      + " 0, 0, 0,0, 0, 0, 0, 0, 0, 0 " + ",'" + strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + Equip_ID + "','" + unitInfo[
                      1] + "','" + Equip_Name + "', 0, 0, 0, '" + \
                  strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            sql = "INSERT INTO strength_maintance (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Plan_Unhanded, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + Equip_ID + "','" + unitInfo[
                      1] + "','" + Equip_Name + "', 0,  '" + \
                  strengthYearInfo[1] + "')"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e


        for disturbplanYearInfo in disturbplanYearInfoTuple:
            sql = "insert into disturbplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " \
                  + "('" + Equip_ID + "','" + Equip_Name + "','" + unitInfo[0] +\
                  "','" + unitInfo[1] + "','"+ disturbplanYearInfo +"', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for orderallotplanYearInfo in orderallotplanYearInfoTuple:
            sql = "insert into orderallotplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,OrderNum) values " \
                  + "('" + Equip_ID + "','" + Equip_Name + "','" + unitInfo[0] + \
                  "','" + unitInfo[1] + "','" + orderallotplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for retireplanYearInfo in retireplanYearInfoTuple:
            sql = "insert into retireplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " \
                  + "('" + Equip_ID + "','" + Equip_Name + "','" + unitInfo[0] + \
                  "','" + unitInfo[1] + "','" + retireplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

        for orderretireplanYearInfo in orderretireplanYearInfoTuple:
            sql = "insert into orderretireplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " \
                  + "('" + Equip_ID + "','" + Equip_Name + "','" + unitInfo[0] + \
                  "','" + unitInfo[1] + "','" + orderretireplanYearInfo + "', '' )"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

    for disturbplanYearInfo in disturbplanYearInfoTuple:
        sql = "insert into disturbplannote (Equip_Id,Equip_Name,Year,Note) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "','" + disturbplanYearInfo + "', '' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "insert into allotschedule (Equip_Id,Equip_Name,army,allotconditionUper,rocketUper,year) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "', '','0','0','" + disturbplanYearInfo + "' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    for retireplanYearInfo in retireplanYearInfoTuple:
        sql = "insert into retireplannote (Equip_Id,Equip_Name,Year,Note) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "','" + retireplanYearInfo + "', '' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    for orderretireplanYearInfo in orderretireplanYearInfoTuple:
        sql = "insert into orderretireplannote (Equip_Id,Equip_Name,Year,Note) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "','" + orderretireplanYearInfo + "', '' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    for orderallotplanYearInfo in orderallotplanYearInfoTuple:
        sql = "insert into orderallotplannote (Equip_Id,Equip_Name,Year,Note) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "','" + orderallotplanYearInfo + "', '' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "insert into orderallotschedule (Equip_Id,Equip_Name,contract,allotconditionUper,rocketUper,year) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "', '','0','0','" + orderallotplanYearInfo + "' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    for orderadjustYearInfo in orderadjustYearInfoTuple:
        sql = "insert into orderAdjust(year,equip_id,equipName,equipUnit,costUnit,oneYear_LastNum,oneYear_NowNum," \
              "oneYear_NextNum,oneYear_Amount,twoYear_LastNum,twoYear_NowNum,twoYear_NextNum,twoYear_Amount," \
              "applicationUnit,supplierUnit,buyMode,manufacturer,adjustFactor,allotUnit,note) values " + \
              "('" + orderadjustYearInfo + "','" + Equip_ID + "','" + Equip_Name + "', '','','','','','','','','',''," \
                                                                           "'','','','','','','' ) "
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        sql = "insert into orderAdjustCont (year,equip_Id,equip_Name,contSource,makeProj1,bid2,approval3,status1," \
              "signContract2,finish3) values " \
              + "('" + orderadjustYearInfo + "','" + Equip_ID + "','" + Equip_Name + "','','0','0','0','0','','0' )"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e



#单位表unit中修改一条数据
def updateDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper, Unit_Alias):
    # 插入的sql语句
    sql = "Update unit set Unit_Name = '" + Unit_Name + "', Unit_Uper = '" + Unit_Uper + "', Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update strength set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update weave set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update disturbplan set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update disturbplanunit set Unit_Name = '" + Unit_Name + "', Unit_Uper = '" + Unit_Uper + "', Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update retireplan set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderallotplan set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderretireplan set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e

#查询装备信息单位表中单位信息
def selectEquipUnitInfo(Equip_ID):
    sql = "Select Unit_Info from equip_unit_info where Equip_ID = '%s'"%Equip_ID
    result =  executeSql(sql)
    if(len(result) < 1):
        return ''
    else:
        return result[0][0]

# 先装备信息表中修改一条数据
def updateDataIntoEquipUnitInfo(Equip_ID, Equip_Unit_Info):
    if len(selectEquipUnitInfo(Equip_ID)) > 0:
        sql = "Update equip_unit_info set Unit_Info = '%s' where Equip_ID = '%s'"%(Equip_ID, Equip_Unit_Info)
    else:
        sql = "Insert into equip_unit_info values ('%s', '%s')"%(Equip_ID, Equip_Unit_Info)
    return executeCommit(sql)

# 单位表equip中修改一条数据
def updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, unit):
    # 插入的sql语句
    sql = "Update equip set Equip_Name = '" + Equip_Name + "', Equip_Uper = '" + Equip_Uper + "', Input_Type = '" + Input_Type + \
          "', Equip_Type = '" + Equip_Type + "', unit ='" + unit + "' where Equip_ID = '" + Equip_ID + "'"
    # 执行sql语句，并发送给数据库
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update strength set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update weave set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update disturbplan set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update disturbplannote set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update allotschedule set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update armytransfer set Equip_Name = '" + Equip_Name  + "', Equip_Unit ='" + unit + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e
    sql = "Update rockettransfer set Equip_Name = '" + Equip_Name + "', Equip_Unit ='" + unit + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update retireplan set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update retireplannote set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderallotplan set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderallotplannote set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderretireplan set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderretireplannote set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderallotschedule set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderAdjust set equipName = '" + Equip_Name + "' where equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "Update orderAdjustCont set equip_Name = '" + Equip_Name + "' where equip_ID = '" + Equip_ID + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


# 找到某个旅团的公用装备信息
def findChildUnitForPublic(Unit_ID):
    sql = "select * from publicequip where Group_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def isHavePulicEquip(Unit_ID):
    sql = "select * from publicequip where Group_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

# 单位表disturbplanunit中删除一条数据
def delDataInDisturbPlanUnit(Unit_ID):
    # 插入的sql语句
    UnitIDList = []
    findChildDisturbPlanUnit(Unit_ID, UnitIDList, cur)
    for UnitID in UnitIDList:
        if UnitID != '':
            sql = "Delete from disturbplanunit where Unit_ID = '" + UnitID + "'"
            cur.execute(sql)
            sql = "Delete from disturbplan where Unit_ID = '" + UnitID + "'"
            cur.execute(sql)
        else:
            sql = "Delete from disturbplanunit where Unit_ID is null"
            cur.execute(sql)
            sql="Delete from disturbplan where Unit_ID is null"
            cur.execute(sql)


    conn.commit()

def selectStrength(UnitID, EquipID, year):
    sql = "select Strength from strength where Equip_ID = '" + EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result == None or len(result) < 1:
        return -1
    else:
        return result[0][0]

def selectAllChildEquipInfo(equipInfoList):
    sql = "select * from equip"
    try:
        cur.execute(sql)
    except Exception as e:
        return e
    equipInfoTuple = cur.fetchall()
    equipInfoList = []
    for equipInfo in equipInfoTuple:
        haveChild = selectEquipIsHaveChild(equipInfo[0])
        if haveChild:
            pass
        else:
            equipInfoList.append(equipInfo[0])
    return True

def selectAllChildUnitInfo():
    unitInfoList=[]
    selectAllDataAboutUnit(unitInfoList)
    unitList = []
    for unitInfo in unitInfoList:
        haveChild = selectUnitIsHaveChild(unitInfo[0])
        if haveChild:
            pass
        else:
            unitList.append(unitInfo[0])
    return unitList

def findAllUperByUnitID(unitID, uperList):
    findUper = []
    findUper.append(unitID)
    while findUper:
        unitID = findUper.pop(0)
        uperList.append(unitID)
        sql = "select Unit_Uper from unit where Unit_ID = '" + unitID + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            return e
        result = cur.fetchall()
        if result:
            findUper.append(result[0][0])
    return True

def findAllUperByEquipID(equipID, uperList):
    findUper = []
    findUper.append(equipID)
    while findUper:
        equipID = findUper.pop(0)
        uperList.append(equipID)
        sql = "select Equip_Uper from equip where Equip_ID = '" + equipID + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            return e
        result = cur.fetchall()
        if result:
            findUper.append(result[0][0])
    return True

# 单位表unit中删除一条数据
def delDataInUnit(Unit_ID):
    # 插入的sql语句
    UnitIDList = []
    #找到所有孩子节点
    findSuccess = findChildUnit(Unit_ID, UnitIDList, "")
    if findSuccess != True:
        return findSuccess
    #找到所有实力查询年份
    yearInfoList = selectAllDataAboutStrengthYear()
    equipInfoList = selectAllDataAboutEquip()
    findChildNode = []
    for unitID in UnitIDList:
        if selectUnitIsHaveChild(unitID[0]):
            pass
        else:
            findChildNode.append(unitID[0])
    endEquipList = selectAllEndEquip()
    for UnitID in findChildNode:
        #对于每一个最根节点找到所有上级节点
        for year in yearInfoList:
            for equip in endEquipList:
                inputInfoTuple = selectInputInfoByEquipUnit(UnitID, equip[0], year[1])
                for inputInfo in inputInfoTuple:
                    delSuccess = delFromInputInfo(UnitID, equip[0], inputInfo[2], inputInfo[3], inputInfo[4], inputInfo[10])
                    if delSuccess != True:
                        conn.rollback()
                        return delSuccess
        uperIDList = []
        findUnitUperIDList(UnitID, uperIDList)
        uperIDList.reverse()
        if uperIDList:
            for unitID in uperIDList[0: -1]:
                for strengthYear in yearInfoList:
                    for equipInfo in equipInfoList:
                        nodeStrengthInfo = selectStrengthInfo(UnitID, equipInfo[0], strengthYear[1])
                        nodeWeaveInfo = selectWeaveInfo(UnitID, equipInfo[0], strengthYear[1])
                        if nodeStrengthInfo:
                            sql = "update strength set strength = strength - " + str(nodeStrengthInfo[0][4]) +\
                          " where Equip_ID = '" + equipInfo[0] \
                          + "' and Unit_ID = '" + unitID + \
                          "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                            sql = "update weave set strength = strength - " + str(nodeStrengthInfo[0][4]) + \
                                  " where Equip_ID = '" + equipInfo[0] \
                                  + "' and Unit_ID = '" + unitID + \
                                  "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                        if nodeWeaveInfo:
                            sql = "update weave set Work = Work - " + str(nodeWeaveInfo[0][5]) +\
                          " where Equip_ID = '" + equipInfo[0] \
                          + "' and Unit_ID = '" + unitID + \
                          "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                            sql = "update strength set Work = Work - " + str(nodeWeaveInfo[0][5]) + \
                                  " where Equip_ID = '" + equipInfo[0] \
                                  + "' and Unit_ID = '" + unitID + \
                                  "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
    for UnitID in UnitIDList:
        sql = "Delete from unit where Unit_ID = '" + UnitID[0] + "'"
        # 执行sql语句，并发送给数据库
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from inputinfo where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from strength where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        publicInfo = findChildUnitForPublic(UnitID[0])
        for public in publicInfo:
            sql = "Delete from publicequip where Equip_ID = '" + public[0] + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return False

            sql = "Delete from weave where Unit_ID = '" + public[0] + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return False

        sql = "Delete from weave where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from disturbplan where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from disturbplanunit where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from retire where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from retireplan where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from orderallotplan where Unit_ID = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

        sql = "Delete from orderretireplan where Unit_Id = '" + UnitID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return False

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False


# 装备表equip中删除一条数据
def delDataInEquip(Equip_ID):
    # 插入的sql语句
    EquipIDList = []
    unitInfoList = []
    yearInfoList = []
    findSuccess = findChildEquip(Equip_ID, EquipIDList, "")
    if findSuccess != True:
        return findSuccess
    yearInfoList = selectAllDataAboutStrengthYear()
    findSuccess = selectAllDataAboutUnit(unitInfoList)
    if findSuccess != True:
        return findSuccess

    findChildNode = []
    for equipID in EquipIDList:
        if selectEquipIsHaveChild(equipID[0]):
            pass
        else:
            findChildNode.append(equipID[0])
    endUnitList = selectAllEndUnit()
    for equipID in findChildNode:
        for year in yearInfoList:
            for unit in endUnitList:
                inputInfoTuple = selectInputInfoByEquipUnit(unit[0], equipID, year[1])
                for inputInfo in inputInfoTuple:
                    delSuccess = delFromInputInfo(unit[0], equipID, inputInfo[2], inputInfo[3], inputInfo[4], inputInfo[10])
                    if delSuccess != True:
                        conn.rollback()
                        return delSuccess

        # 对于每一个最根节点找到所有上级节点
        uperIDList = []
        findEquipUperIDList(equipID, uperIDList)
        uperIDList.reverse()
        if uperIDList:
            for equipID in uperIDList[0: -1]:
                for strengthYear in yearInfoList:
                    for unitInfo in unitInfoList:
                        nodeStrengthInfo = selectStrengthInfo(unitInfo[0], uperIDList[-1], strengthYear[1])
                        nodeWeaveInfo = selectWeaveInfo(unitInfo[0], uperIDList[-1], strengthYear[1])
                        if nodeStrengthInfo:
                            sql = "update strength set strength = strength - " + str(nodeStrengthInfo[0][4]) + \
                              " where Equip_ID = '" + equipID \
                              + "' and Unit_ID = '" + unitInfo[0] + \
                              "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                            sql = "update weave set strength = strength - " + str(nodeStrengthInfo[0][4]) + \
                                  " where Equip_ID = '" + equipID \
                                  + "' and Unit_ID = '" + unitInfo[0] + \
                                  "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                        if nodeWeaveInfo:
                            sql = "update weave set Work = Work - " + str(nodeWeaveInfo[0][5]) + \
                              " where Equip_ID = '" + equipID \
                              + "' and Unit_ID = '" + unitInfo[0] + \
                              "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
                            sql = "update strength set Work = Work - " + str(nodeWeaveInfo[0][5]) + \
                                  " where Equip_ID = '" + equipID \
                                  + "' and Unit_ID = '" + unitInfo[0] + \
                                  "' and year = '" + strengthYear[1] + "'"
                            try:
                                cur.execute(sql)
                            except Exception as e:
                                conn.rollback()
                                return e
    for EquipID in EquipIDList:
        sql = "Delete from equip where Equip_ID = '" + EquipID[0] + "'"
        # 执行sql语句，并发送给数据库
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        sql = "Delete from equip_unit_info where Equip_ID = '" + EquipID[0] + "'"
        # 执行sql语句，并发送给数据库
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from inputinfo where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from strength where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from weave where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from disturbplan where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from disturbplannote where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from retireplan where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from retireplannote where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from allotschedule where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from retire where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from rockettransfer where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from armytransfer where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderallotplan where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderallotplannote where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderallotschedule where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderretireplan where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderretireplannote where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderAdjust where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

        sql = "Delete from orderAdjustCont where Equip_ID = '" + EquipID[0] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e

    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


def selectIfExistsStrengthYear(year):
    allYear = selectAllDataAboutStrengthYear()
    for i in allYear:
        if i[1] == str(year):
            return True
    return False


# 返回strengthyear表中所有信息
def selectAllDataAboutStrengthYear():
    yearInfoList = []
    sql = "select * from strengthyear order by year"
    cur.execute(sql)

    result = cur.fetchall()
    for resultInfo in result:
        yearInfoList.append(resultInfo)
    return yearInfoList


#按照单位编号，装备编号以及录入年份查找录入信息
def selectInfoAboutInput(Unit_ID, Equip_ID, inputYear, factoryYear, startFactoryYear, endFactorYear):
    resultList = []
    if factoryYear == "":
        sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" \
              + Equip_ID + "' and inputYear = '" + inputYear + "'"
    else:
        sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '"\
          + Equip_ID + "' and inputYear = '" + inputYear + "' and (year between '" + startFactoryYear + "' and '" + endFactorYear + "')"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(resultInfo)
    return resultList


# 判断当前是否为公用装备
def selectIsPublicEquip(Unit_ID):
    sql = "select * from publicequip where Equip_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


# 按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutWeaveByEquipShow(UnitList, EquipList, yearList):
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            # 查询当前装备ID的孩子序列
            EquipIDChildList = []
            findChildEquip(Equip_ID, EquipIDChildList, "")
            for childEquipID in EquipIDChildList:
                sql = "select * from weave where Unit_ID = '" + Unit_ID + \
                        "' and Equip_ID = '" + childEquipID[0] + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    weave = list(resultInfo)
                    weave[3] = childEquipID[1]
                    resultList.append(weave)
    return resultList

def isEquipUper(Equip_ID, Equip_Uper):
    sql = "select * from equip where Equip_ID = '" + Equip_ID + \
          "' and Equip_Uper = '" + Equip_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False
#按装备展开查询实力数和计划未移交量
def selectAboutStrengthMaintanceByEquipShow(UnitList, EquipList, year):
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            # 查询当前装备ID的孩子序列
            EquipIDChildList = []
            findChildEquip(Equip_ID, EquipIDChildList, "")
            for i, childEquipID in enumerate(EquipIDChildList):
                unitName = selectUnitNameByUnitID(Unit_ID)
                equipName = selectEquipNameByEquipID(childEquipID[0])
                strength = getStrengthNum(Unit_ID, Equip_ID, year)
                planUnhanded = selectPlanUnhandedNum(Unit_ID, Equip_ID, year)
                resultList.append([Unit_ID, unitName, Equip_ID, childEquipID[1], strength, planUnhanded])
    return resultList
#查询实力数和计划未移交量
def selectAboutStrengthMaintanceByUnitListAndEquipList(UnitList, EquipList, year):
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            unitName = selectUnitNameByUnitID(Unit_ID)
            equipName = selectEquipNameByEquipID(Equip_ID)
            strength = getStrengthNum(Unit_ID, Equip_ID, year)
            planUnhanded = selectPlanUnhandedNum(Unit_ID, Equip_ID, year)
            resultList.append([Unit_ID, unitName, Equip_ID, equipName, strength, planUnhanded, year])
    return resultList
#展开到末级查询实力数和计划未移交量
def selectAboutStrengthMaintanceByLast(UnitList, EquipList, year):
    resultList = []
    if UnitList:
        UnitID = UnitList[0]
    else:
        return
    if EquipList:
        EquipID = EquipList[0]
    else:
        return
    childEquip = []
    childUnit = []
    findSuccess = findChildEquip(EquipID, childEquip, "")
    if findSuccess != True:
        return []
    findSuccess = findChildUnit(UnitID, childUnit, "")
    if findSuccess != True:
        return []
    unitSpace = ""
    for UnitID in childUnit:
        for EquipID in childEquip:
            strengthNum = getStrengthNum(UnitID[0], EquipID[0], year)
            planUnhandedNum = selectPlanUnhandedNum(UnitID[0], EquipID[0], year)
            resultList.append([UnitID[0], UnitID[1], EquipID[0], EquipID[1], strengthNum, planUnhandedNum, year])
    return resultList
#按单位展开查询实力数和计划未移交量
def selectAboutStrengthMaintanceByUnitShow(UnitList, EquipList, year):
    resultList = []
    for Equip_ID in EquipList:
        for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
            UnitIDChildList = []
            findChildUnit(Unit_ID, UnitIDChildList, "")
            space = ""
            for childUnitID in UnitIDChildList:
                unitName = selectUnitNameByUnitID(childUnitID[0])
                equipName = selectEquipNameByEquipID(Equip_ID)
                strength = getStrengthNum(Unit_ID, Equip_ID, year)
                planUnhanded = selectPlanUnhandedNum(Unit_ID, Equip_ID, year)
                resultList.append([Unit_ID, childUnitID[1], Equip_ID, equipName, strength, planUnhanded, year])
    return resultList

# 按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByEquipShow(UnitList, EquipList, yearList,equipYear,startYear, endYear,flagValue0 = False):
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            # 查询当前装备ID的孩子序列
            EquipIDChildList = []
            findChildEquip(Equip_ID, EquipIDChildList, "")
            for i, childEquipID in enumerate(EquipIDChildList):
                unitName = selectUnitNameByUnitID(Unit_ID)
                equipName = selectEquipNameByEquipID(childEquipID[0])
                if equipYear == "":
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                        "' and Equip_ID = '" + childEquipID[0] + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    if flagValue0:
                        for resultInfo in result:
                            info = list(resultInfo)
                            if info[4] != 0:
                                info[7] = info[4] - info[6]
                                info[2] = childEquipID[1]
                                resultList.append(info)
                            break
                    else:
                        for resultInfo in result:
                            info = list(resultInfo)
                            info[7] = info[4] - info[6]
                            info[2] = childEquipID[1]
                            resultList.append(info)
                            break

                else:
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                          "' and Equip_ID = '" + childEquipID[0] + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result:
                        if flagValue0:
                            info = list(result[0])
                            if info[4] != 0:
                                childEquipList = findChildNodeEquipIDList(childEquipID[0])
                                childUnitList = findChildNodeUnitIDList(Unit_ID)
                                info[6] = 0
                                for unitID in childUnitList:
                                    for equipID in childEquipList:
                                        sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                              "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                              + "' and year between '" + startYear + "' and '" + endYear + "'"
                                        cur.execute(sql)
                                        result = cur.fetchall()
                                        for resultInfo in result:
                                            info[6] = info[6] + int(resultInfo[3])
                                info[7] = info[4] - info[6]
                                info[2] = childEquipID[1]
                                resultList.append(info)
                        else:
                            info = list(result[0])
                            childEquipList = findChildNodeEquipIDList(childEquipID[0])
                            childUnitList = findChildNodeUnitIDList(Unit_ID)
                            info[6] = 0
                            for unitID in childUnitList:
                                for equipID in childEquipList:
                                    sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                          "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                          + "' and year between '" + startYear + "' and '" + endYear + "'"
                                    cur.execute(sql)
                                    result = cur.fetchall()
                                    for resultInfo in result:
                                        info[6] = info[6] + int(resultInfo[3])
                            info[7] = info[4] - info[6]
                            info[2] = childEquipID[1]
                            resultList.append(info)
    return resultList


# 判断当前单位是否是旅团
def selectUnitIsGroup(Unit_ID):

    sql = "select * from unit where Is_Group = '是' and Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


# 按单位展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitShow(UnitList, EquipList, yearList):
    resultList = []
    for Equip_ID in EquipList:
        for Unit_ID in UnitList:
            # 查询当前单位ID的孩子序列
            UnitIDChildList = []
            findChildUnitByWeave(Unit_ID, UnitIDChildList, "")
            for childUnitID in UnitIDChildList:
                sql = "select * from weave where Unit_ID = '" + childUnitID[0] + \
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    weave = list(resultInfo)
                    weave[2] = childUnitID[1]
                    resultList.append(weave)
    return resultList

#实力查询展开到末级
def selectAboutStrengthByLast(UnitList, EquipList, year, equipYear, startFactoryYear, endFactoryYear,flagValue0 = False):
    resultList = []
    if UnitList:
        UnitID = UnitList[0]
    else:
        return
    if EquipList:
        EquipID = EquipList[0]
    else:
        return
    childEquip = []
    childUnit = []
    findSuccess = findChildEquip(EquipID, childEquip, "")
    if findSuccess != True:
        return []
    findSuccess = findChildUnit(UnitID, childUnit, "")
    if findSuccess != True:
        return []

    if equipYear == "":
        if flagValue0:
            unitSpace = ""
            for UnitID in childUnit:
                for EquipID in childEquip:
                    strengthInfo = selectStrengthInfo(UnitID[0], EquipID[0], year)
                    for strength in strengthInfo:
                        info = list(strength)
                        if info[4] != 0:
                            info[7] = info[4] - info[6]
                            info[2] = EquipID[1]
                            info[3] = UnitID[1]
                            resultList.append(info)
                        break
        else:
            unitSpace = ""
            for UnitID in childUnit:
                for EquipID in childEquip:
                    strengthInfo = selectStrengthInfo(UnitID[0], EquipID[0], year)
                    for strength in strengthInfo:
                        info = list(strength)
                        info[7] = info[4] - info[6]
                        info[2] = EquipID[1]
                        info[3] = UnitID[1]
                        resultList.append(info)
                        break
    return resultList

#判断是否是最小的实力年份
def selectIsMinStrengthYear(year):
    sql = "select min(year) from strengthyear"
    cur.execute(sql)
    result = cur.fetchall()

    for minyear in result:
        if minyear[0] == year:
            return True
        else:
            return False

#编制数查询展开到末级
def selectAboutWeaveByLast(UnitList, EquipList, year):
    resultList = []
    if UnitList:
        UnitID = UnitList[0]
    else:
        return
    if EquipList:
        EquipID = EquipList[0]
    else:
        return
    childEquip = []
    childUnit = []
    findSuccess = findChildEquip(EquipID, childEquip, "")
    if findSuccess != True:
        return []
    findChildUnitByWeave(UnitID, childUnit, "")
    for UnitID in childUnit:
        for EquipID in childEquip:
            weaveInfo = selectWeaveInfo(UnitID[0], EquipID[0], year)
            for weave in weaveInfo:
                info = list(weave)
                info[3] = EquipID[1]
                info[2] = UnitID[1]
                resultList.append(info)
                break

    return resultList

# 按单位展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitShow(UnitList, EquipList, yearList, equipYear, startFactoryYear, endFactoryYear,flagValue0 = False):
    resultList = []
    # 如果只查询某年的
    #if len(yearList) == 1:
        # 如果查询全部年的
    for Equip_ID in EquipList:
        for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
            UnitIDChildList = []
            findChildUnit(Unit_ID, UnitIDChildList, "")
            space = ""
            for childUnitID in UnitIDChildList:
                unitName = selectUnitNameByUnitID(childUnitID[0])
                equipName = selectEquipNameByEquipID(Equip_ID)
                if equipYear == "":
                    sql = "select * from strength where Unit_ID = '" + childUnitID[0] + \
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    if flagValue0:
                        for resultInfo in result:
                            info = list(resultInfo)
                            if info[4] != 0:
                                info[7] = info[4] - info[6]
                                info[3] = childUnitID[1]
                                resultList.append(info)
                    else:
                        for resultInfo in result:
                            info = list(resultInfo)
                            info[7] = info[4] - info[6]
                            info[3] = childUnitID[1]
                            resultList.append(info)
                else:
                    sql = "select * from strength where Unit_ID = '" + childUnitID[0] + \
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    if result:
                        if flagValue0:
                            info = list(result[0])
                            if info[4] != 0:
                                childEquipList = findChildNodeEquipIDList(Equip_ID)
                                childUnitList = findChildNodeUnitIDList(childUnitID[0])
                                info[6] = 0
                                for unitID in childUnitList:
                                    for equipID in childEquipList:
                                        sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                              "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                              + "' and year between '" + startFactoryYear + "' and '" + endFactoryYear + "'"
                                        cur.execute(sql)
                                        result = cur.fetchall()
                                        for resultInfo in result:
                                            info[6] = info[6] + int(resultInfo[3])
                                info[7] = info[4] - info[6]
                                info[3] = childUnitID[1]
                                resultList.append(info)
                        else:
                            info = list(result[0])
                            childEquipList = findChildNodeEquipIDList(Equip_ID)
                            childUnitList = findChildNodeUnitIDList(childUnitID[0])
                            info[6] = 0
                            for unitID in childUnitList:
                                for equipID in childEquipList:
                                    sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                  "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                  + "' and year between '" + startFactoryYear + "' and '" + endFactoryYear + "'"
                                    cur.execute(sql)
                                    result = cur.fetchall()
                                    for resultInfo in result:
                                        info[6] = info[6] + int(resultInfo[3])
                            info[7] = info[4] - info[6]
                            info[3] = childUnitID[1]
                            resultList.append(info)
                    else:
                        if not flagValue0:
                            info = [Equip_ID, childUnitID, equipName, unitName, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0,0]
                            info[3] = childUnitID[1]
                            resultList.append(info)
    return resultList



def selectDataFromStrengthByYear(year):
    sql = "select * from strength where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectDataFromInputByYear(year):
    sql = "select * from inputinfo where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectDataFromWeaveByYear(year):
    sql = "select * from weave where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

# def insertBeforYearIntoStrength(year):
#     beforYearStrengthInfo  = selectDataFromStrengthByYear(year - 1)
#     beforYearInputInfoTuple = selectDataFromInputByYear(year - 1)
#     weaveInfoTuple = selectDataFromWeaveByYear(year - 1)
#     equipList = selectAllDataAboutEquip()
#     unitList = selectAllDataAboutUnit()
#     #导入去年的数据
#     if beforYearStrengthInfo:
#         year = str(year)
#         result = selectAllStrengthYearInfo()
#         sql = "insert into strengthyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
#         cur.execute(sql)
#         for strengthInfo in beforYearStrengthInfo:
#             sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
#                   "NonStrength, Single, Arrive, year, equipYear) VALUES" \
#                   + "('" + strengthInfo[0] + "','" + strengthInfo[1] + "','" + strengthInfo[2] + "','" + strengthInfo[3] + "','" \
#                   + strengthInfo[4] + "','" + strengthInfo[5] + "','" + strengthInfo[6] + "','" + strengthInfo[7] + "','" + strengthInfo[8]\
#                   + "','" + strengthInfo[9] + "','" + strengthInfo[10] + "','" + strengthInfo[11] + "','" + strengthInfo[12] + "','" + strengthInfo[13]\
#                   + "','" + strengthInfo[15]  + "','" + year + "','" + strengthInfo[16] + "')"
#             cur.execute(sql)
#         if beforYearInputInfoTuple:
#             for inputInfo in beforYearInputInfoTuple:
#                 sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, inputYear) VALUES" \
#                   + "('" + inputInfo[0] + "','" + inputInfo[1] + "','" + inputInfo[2] + "', '" + inputInfo[3] + "', '" + inputInfo[4] + "', '"\
#                   + inputInfo[5] + "', '" + inputInfo[6] + \
#                   "', '" + inputInfo[7] + "', '" + inputInfo[8] + "', '" + inputInfo[9] + "', '" + year + "')"
#             cur.execute(sql)
#
#     #导入去年的编制数表记录
#     if weaveInfoTuple:
#         year = str(year)
#         for weaveInfo in weaveInfoTuple:
#             sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
#                   + "('" + weaveInfo[0] + "','" + weaveInfo[1] + "','" + weaveInfo[2] + "','" + weaveInfo[
#                       3] + "', '" + weaveInfo[4] + "', '" + weaveInfo[5] + "', '" + weaveInfo[6] + "','" + year + "')"
#             print(sql)
#             cur.execute(sql)
#
#     conn.commit()
#     return

#查询本年度本装备本单位是否存在该批次号
def selectIDWhetherExitFromInputInfo(EquipID, UnitID, strengthYear, ID):
    sql = "select ID from inputinfo where Equip_ID = '" + EquipID + "' and Unit_ID = '" + UnitID + "' and inputYear = '" + strengthYear + "' and ID = '" + ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def selectFromInputInfo(EquipID, UnitID, strengthYear):
    sql = "select * from inputinfo where Equip_ID = '" + EquipID + "' and Unit_ID = '" + UnitID + "' and inputYear = '" + strengthYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

'''
    新增一个实力查询年份
'''
def insertIntoStrengthYear(year):
    year = str(year)
    sql = "insert into strengthyear(ID, year) values ('" + year + "', '" + year + "')"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e
    publicEquipInfoList = selectAllDataAboutPublicEquip()
    equipList = selectAllDataAboutEquip()
    unitList = []
    selectAllDataAboutUnit(unitList)

    sql = "select * from strengthyear where year = '" + str(int(year) - 1) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        for equipInfo in equipList:
            for unitInfo in unitList:
                strengthInfo = selectStrengthInfo(unitInfo[0], equipInfo[0], str(int(year) - 1))
                if strengthInfo:
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year) VALUES" \
                          + "('" + strengthInfo[0][0] + "', '" + strengthInfo[0][1] + "', '" + strengthInfo[0][
                              2] + "', '" \
                          + strengthInfo[0][3] + "', " + str(strengthInfo[0][4]) + ", " + str(strengthInfo[0][5]) + ", " \
                          + str(strengthInfo[0][6]) + ", " + str(strengthInfo[0][7]) + ", " + str(
                        strengthInfo[0][8]) + ", " \
                          + str(strengthInfo[0][9]) + ", " + str(strengthInfo[0][10]) + ", " + str(
                        strengthInfo[0][11]) + ", " \
                          + str(strengthInfo[0][12]) + ", " + str(strengthInfo[0][13]) + ", " + str(
                        strengthInfo[0][14]) + ", '" + year + "')"

                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

                else:
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year) VALUES" \
                          + "('" + equipInfo[0] + "', '" + unitInfo[0] + "', '" + equipInfo[1] + "', '" \
                          + unitInfo[1] + "', " + str(0) + ", " + str(0) + ", " \
                          + str(0) + ", " + str(0) + ", " + str(0) + ", " \
                          + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + "," + str(0) + ", " + str(
                        0) + ", '" + year + "')"

                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                weaveInfo = selectWeaveInfo(unitInfo[0], equipInfo[0], str(int(year) - 1))

                if weaveInfo:
                    sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                          + "('" + unitInfo[0] + "','" + equipInfo[0] + "','" + unitInfo[1] + "','" + equipInfo[
                              1] + "'," + str(weaveInfo[0][4]) + "," + str(weaveInfo[0][5]) + "," + str(
                        weaveInfo[0][6]) + ", '" + year + "')"

                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                else:
                    sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                          + "('" + unitInfo[0] + "','" + equipInfo[0] + "','" + unitInfo[1] + "','" + equipInfo[
                              1] + "'," + str(0) + "," + str(0) + "," + str(0) + ", '" + year + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e



            for publiequip in publicEquipInfoList:

                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + equipInfo[0] + "', '" + publiequip[0] + "', '" + equipInfo[1] + "', '" \
                      + "公用装备" + "', " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + "," + str(0) + ", " + str(
                    0) + ", '" + year + "')"

                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                weaveInfo = selectWeaveInfo(publiequip[0], equipInfo[0], str(int(year) - 1))

                if weaveInfo:
                    sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + publiequip[0] + "','" + equipInfo[0] + "','" + "公用装备" + "','" + equipInfo[
                          1] + "'," + str(weaveInfo[0][4]) + "," + str(weaveInfo[0][5]) + "," + str(
                        weaveInfo[0][6]) + ", '" + year + "')"

                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                else:
                    sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + publiequip[0] + "','" + equipInfo[0] + "','" + "公用装备" + "','" + equipInfo[
                          1] + "'," + str(0) + "," + str(0) + "," + str(0) + ", '" + year + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
    else:
        for equipInfo in equipList:
            for unitInfo in unitList:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + equipInfo[0] + "', '" + unitInfo[0] + "', '" + equipInfo[1] + "', '" \
                      + unitInfo[1] + "', " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + "," + str(0) + ", " + str(
                    0) + ", '" + year + "')"

                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + unitInfo[0] + "','" + equipInfo[0] + "','" + unitInfo[1] + "','" + equipInfo[
                          1] + "'," + str(0) + "," + str(0) + "," + str(0) + ", '" + year + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
            for publiequip in publicEquipInfoList:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + equipInfo[0] + "', '" + publiequip[0] + "', '" + equipInfo[1] + "', '" \
                      + "公用装备" + "', " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " \
                      + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + "," + str(0) + ", " + str(
                    0) + ", '" + year + "')"

                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + publiequip[0] + "','" + equipInfo[0] + "','" + "公用装备" + "','" + equipInfo[
                          1] + "'," + str(0) + "," + str(0) + "," + str(0) + ", '" + year + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e

# 没有展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitListAndEquipList(UnitList, EquipList, yearList):
    resultList= []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            sql = "select * from weave where Unit_ID = '" + Unit_ID + \
                      "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
            cur.execute(sql)
            result = cur.fetchall()
            for resultInfo in result:
                resultList.append(resultInfo)
    return resultList

#没有展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, yearList, equipYear, startFactoryYear, endFactoryYear,flagValue0 = False):
    resultList = []
    #如果只查询某年的
    #if len(yearList) == 1:
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            unitName = selectUnitNameByUnitID(Unit_ID)
            equipName = selectEquipNameByEquipID(Equip_ID)
            if equipYear == "":
                sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                if flagValue0:
                    for resultInfo in result:
                        Info = list(resultInfo)
                        if Info[4] != 0:
                            Info[7] = Info[4] - Info[6]
                            resultList.append(Info)
                else:
                    for resultInfo in result:
                        Info = list(resultInfo)
                        Info[7] = Info[4] - Info[6]
                        resultList.append(Info)
            else:
                sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                      "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                if result:
                    if flagValue0:
                        info = list(result[0])
                        if info[4] != 0:
                            childEquipList = findChildNodeEquipIDList(Equip_ID)
                            childUnitList = findChildNodeUnitIDList(Unit_ID)
                            info[6] = 0
                            for unitID in childUnitList:
                                for equipID in childEquipList:
                                    sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                          "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                          + "' and year between '" + startFactoryYear + "' and '" + endFactoryYear + "'"
                                    cur.execute(sql)
                                    result = cur.fetchall()
                                    for resultInfo in result:
                                        info[6] = info[6] + int(resultInfo[3])
                            info[7] = info[4] - info[6]
                            resultList.append(info)
                    else:
                        info = list(result[0])
                        childEquipList = findChildNodeEquipIDList(Equip_ID)
                        childUnitList = findChildNodeUnitIDList(Unit_ID)
                        info[6] = 0
                        for unitID in childUnitList:
                            for equipID in childEquipList:
                                sql = "select * from inputinfo where Unit_ID = '" + unitID + \
                                      "' and Equip_ID = '" + equipID + "' and inputYear = '" + yearList \
                                      + "' and year between '" + startFactoryYear + "' and '" + endFactoryYear + "'"
                                cur.execute(sql)
                                result = cur.fetchall()
                                for resultInfo in result:
                                    info[6] = info[6] + int(resultInfo[3])
                        info[7] = info[4] - info[6]
                        resultList.append(info)
    return resultList


# 查看某单位是否有子单位
def selectUnitIsHaveChild(Unit_ID):

    sql = "select * from unit where Unit_Uper = '" + Unit_ID + "'"

    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


# 查看某装备是否有子装备
def selectEquipIsHaveChild(Equip_ID):
    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


# 返回装备是否是逐批录入
def selectEquipInputType(Equip_ID):

    sql = "select * from equip where Equip_ID = '" + Equip_ID + "'"

    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        if resultInfo[3] == '逐批录入':
            return True
        else:
            return False


# 查找某个单位的所有上级单位编号
def findUnitUperIDList(Unit_ID, UnitIDList):
    UnitIDList.append(Unit_ID)
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    uperIDTuple = cur.fetchall()
    for uperIDInfo in uperIDTuple:
        if uperIDInfo[0] != '':
            findUnitUperIDList(uperIDInfo[0], UnitIDList)


# 查找某个装备的所有上级单位编号
def findEquipUperIDList(Equip_ID, EquipIDList):
    EquipIDList.append(Equip_ID)
    sql = "select Equip_Uper from equip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    uperIDTuple = cur.fetchall()
    for uperIDInfo in uperIDTuple:
        if uperIDInfo[0] != '':
            findEquipUperIDList(uperIDInfo[0], EquipIDList)

# 通过单位号和装备号查找strength某条记录的实力数，现有数
def seletNumAboutStrength(Unit_ID, Equip_ID, year):
    sql = "select * from strength where Equip_ID = '" + Equip_ID \
          + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 通过单位号和装备号查找strength某条记录的编制数
def seletNumAboutWork(Unit_ID, Equip_ID, year):
    sql = "select Work from weave where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# def delWeaveYearByYear(year):
#     sql = "delete from weaveyear where year = '" + year + "'"
#     cur.execute(sql)
#
#     allUnitInfo = selectAllDataAboutUnit()
#     allEquipInfo = selectAllDataAboutEquip()
#     for unitInfo in allUnitInfo:
#         for equipInfo in allEquipInfo:
#             allWork = selectWorkNumFromWeave(unitInfo[0], equipInfo[0], '')
#             yearWork = selectWorkNumFromWeave(unitInfo[0], equipInfo[0], year)
#             newWork = str(int(allWork) - int(yearWork))
#             sql = "update weave set Work = '" + newWork + "' where Unit_ID = '" + unitInfo[0] +\
#             "' and Equip_ID = '" + equipInfo[0] + "' and year = ''"
#             cur.execute(sql)
#     sql = "delete from weave where year = '" + year + "'"
#     cur.execute(sql)
#     conn.commit()

def delFactoryYear(year):
    sql = "delete from factoryyear where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()

#查询某个装备某个单位某个年份的所有input信息
def selectInputInfoByEquipUnit(Unit_ID, Equip_ID, inputYear):
    sql = "select * from inputinfo where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and inputYear = '" + inputYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectInputInfoByIDAndUnitEquipYear(Unit_ID, Equip_ID, inputYear, ID):
    sql = "select * from inputinfo where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and inputYear = '" + inputYear + "' and ID = '" + ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result
# 删除某条录入信息
def delFromInputInfo(Unit_ID, Equip_ID, ID, num, year, inputYear):
    EquipIDList = []
    UnitIDList = []
    delNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    findLastYear = findBigOtherYear(inputYear)
    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            strengthAllYearInfo = seletNumAboutStrength(UnitID, EquipID, inputYear)
            if strengthAllYearInfo:
                nowAllNum = strengthAllYearInfo[0][6]
            else:
                nowAllNum = 0
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                       "NonStrength, Single, Arrive, year) VALUES" \
                       + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                  " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                       inputYear +  "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    return e
            changeAllNowNum = int(nowAllNum) - delNum

            sql = "Update strength set Now = " + str(changeAllNowNum) + " where Equip_ID = '" + \
                   EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + inputYear + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                return e

            sql = "update weave set Now = " + str(changeAllNowNum) + " where Unit_ID = '" \
                   + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + inputYear + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                return e
            for lastYear in findLastYear:
                if selectInputInfoByIDAndUnitEquipYear(Unit_ID, Equip_ID, lastYear, ID):
                    sql = "Update strength set Now = Now - " + str(delNum) + " where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        return e

                    sql = "update weave set Now = Now - " + str(delNum) + " where Unit_ID = '" \
                      + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        return e

    for lastYear in findLastYear:
        sql = "delete from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + \
              Equip_ID + "' and ID = '" + ID + "' and year = '" + year + "' and ID = '" + ID + "' and inputYear = '" + lastYear + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            return e
    sql = "delete from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" +\
          Equip_ID + "' and ID = '" + ID + "' and year = '" + year + "' and ID = '" + ID + "' and inputYear = '" + inputYear + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        return e
    try:
        conn.commit()
        return True
    except Exception as e:
        return e


# # 修改批量录入某条数据的数量
# def updateNumMutilInput(Unit_ID, Equip_ID, ID, num, orginNum, year, strengthYear):
#     EquipIDList = []
#     UnitIDList = []
#     updateNum = int(num)
#     findUnitUperIDList(Unit_ID, UnitIDList)
#     findEquipUperIDList(Equip_ID, EquipIDList)
#
#     for UnitID in UnitIDList:
#         for EquipID in EquipIDList:
#             strengthYearNum, nowYearNum = seletNumAboutStrength(UnitID, EquipID, strengthYear, year)
#             changeYearNowNum = int(nowYearNum) - int(orginNum) + updateNum
#             changeYearErrorNum = int(strengthYearNum) - changeYearNowNum
#             strengthAllNum, nowAllNum = seletNumAboutStrength(UnitID, EquipID, strengthYear, '')
#             changeAllNowNum = int(nowAllNum) - int(orginNum) + updateNum
#             changeAllErrorNum = int(strengthAllNum) - changeAllNowNum
#             sql = "Update strength set Now = '" + str(changeYearNowNum) + "', Error = '" + str(
#                 changeYearErrorNum) + "' where Equip_ID = '" + \
#                   EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear \
#                   + "' and equipYear = '" + year + "'"
#
#             cur.execute(sql)
#
#             sql = "Update weave set Now = '" + str(changeAllNowNum) + "' where Equip_ID = '" + \
#                   EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear + "'"
#
#             cur.execute(sql)
#             sql = "update strength set Now = '" + str(changeAllNowNum) + "', Error = '" + str(
#                 changeAllErrorNum) + "' where Unit_ID = '" \
#                   + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + strengthYear + "' and equipYear = ''"
#             # print(sql)
#             cur.execute(sql)
#
#     sql = "update inputinfo set num = '" + num + "' where Unit_ID = '" + Unit_ID + \
#           "' and Equip_ID = '" + Equip_ID + "' and ID = '" + ID + "' and year = '" + year + "'"
#     cur.execute(sql)
#     # print(sql)
#     cur.execute(sql)
#     conn.commit()

# 判断是否有当前出厂年份
def isHaveFactoryYear(year):
    sql = "select * from factoryyear where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

# def addNewFactoryYear(year):
#     result = selectAllDataAboutFactoryYear()
#     sql = "insert into factoryyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
#     print(sql)
#     cur.execute(sql)
#
#     equipList = selectAllDataAboutEquip()
#     unitList = selectAllDataAboutUnit()
#     strengthYearInfo = selectAllDataAboutStrengthYear()

#
#     for equipInfo in equipList:
#         for unitInfo in unitList:
#             for strengthYear in strengthYearInfo:
#                 sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
#                   "NonStrength, Single, Arrive, year, equipYear) VALUES" \
#                   + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[1] + "', '0'," \
#                                                                                                        " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
#                     strengthYear[1] + "', '" + year + "')"
#                 cur.execute(sql)
#
#     conn.commit()

# 往录入表inputinfo中插入一条数据
def addDataIntoInputInfo(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, strengthYear):
    EquipIDList = []
    UnitIDList = []
    addNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    lastOtherYear = findBigOtherYear(strengthYear)
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, inputYear) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "', '" + num + "', '" + year + "', '" + shop + "', '" + state +\
          "', '" + arrive + "', '" + confirm + "', '" + other + "', '" + strengthYear +  "')"
    try:
        cur.execute(sql)
    except Exception as e:
        return e

    for lastYear in lastOtherYear:
        sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, inputYear) VALUES" \
              + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "', '" + num + "', '" + year + "', '" + shop + "', '" + state + \
              "', '" + arrive + "', '" + confirm + "', '" + other + "', '" + lastYear + "')"
        try:
            cur.execute(sql)
        except Exception as e:
            return e
    # 执行sql语句，并发送给数据库
    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            unitName = selectUnitNameByUnitID(UnitID)
            equipName = selectEquipNameByEquipID(EquipID)
            strengthAllYearInfo = seletNumAboutStrength(UnitID, EquipID, strengthYear)
            if strengthAllYearInfo:
                nowAllNum = strengthAllYearInfo[0][6]
            else:
                strengthAllNum, nowAllNum = 0, 0
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                 " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                      strengthYear + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e

            changeAllNowNum = nowAllNum + addNum

            sql = "update strength set Now = " + str(changeAllNowNum) + " where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + strengthYear + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            weaveInfo = selectWeaveInfo(UnitID, EquipID, strengthYear)
            if weaveInfo:
                pass
            else:
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, " \
                      "year) VALUES" \
                      + "('" + UnitID + "','" + EquipID + "','" + unitName + "','" + \
                      equipName + "',0, 0, 0, '" + strengthYear + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e

            sql = "Update weave set Now = " + str(changeAllNowNum) + " where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear + "'"

            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e
            for lastYear in lastOtherYear:
                strengthAllYearInfo = seletNumAboutStrength(UnitID, EquipID, lastYear)
                if strengthAllYearInfo:
                    nowAllNum = strengthAllYearInfo[0][6]
                else:
                    strengthAllNum, nowAllNum = 0, 0
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year) VALUES" \
                          + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                     " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                          lastYear + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

                changeAllNowNum = nowAllNum + addNum

                sql = "update strength set Now = " + str(changeAllNowNum) + " where Unit_ID = '" \
                      + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + lastYear + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e

                weaveInfo = selectWeaveInfo(UnitID, EquipID, lastYear)
                if weaveInfo:
                    pass
                else:
                    sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, " \
                          "year) VALUES" \
                          + "('" + UnitID + "','" + EquipID + "','" + unitName + "','" + \
                          equipName + "',0, 0, 0, '" + lastYear + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

                sql = "Update weave set Now = " + str(changeAllNowNum) + " where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"

                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


# 根据单位号和装备号查询现有数和实力数
def selectNowNumAndStrengthNum(Unit_ID, Equip_ID, year, factoryYear):
    sql = "SELECT Now, Strength from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        return resultInfo[0], resultInfo[1]


# 修改当前编制数
def updateWeaveNum(Unit_ID, Equip_ID, weaveNum, orginWeave, year):
    lastOtherYear = findBigOtherYear(year)
    if selectIsPublicEquip(Unit_ID):
        Group_ID = selectEquipIDByPublicEquip(Unit_ID)
        UnitIDList = []
        UnitIDList.append(Unit_ID)
        EquipIDList = []
        findUnitUperIDList(Group_ID, UnitIDList)
        findEquipUperIDList(Equip_ID, EquipIDList)
        for UnitID in UnitIDList:
            for EquipID in EquipIDList:
                equipName = selectEquipNameByEquipID(EquipID)
                unitName = selectUnitNameByUnitID(UnitID)
                strengthInfo = selectWeaveInfo(UnitID, EquipID, year)  # 获取原有的实力数以及现有数
                if strengthInfo:
                    orginYearWorkNum = strengthInfo[0][5]
                else:
                    orginYearWorkNum = 0
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year) VALUES" \
                          + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                     " 0, 0,0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                          year + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                changeYearWorkNum = int(orginYearWorkNum) - int(orginWeave) + int(weaveNum)
                sql = "Update strength set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e

                sql = "Update weave set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                for lastYear in lastOtherYear:
                    sql = "Update strength set Work = Work - " + str(orginWeave) + " + " + str(
                        weaveNum) + " where Equip_ID = '" + \
                          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

                    sql = "Update weave set Work = Work - " + str(orginWeave) + " + " + str(
                        weaveNum) + " where Equip_ID = '" + \
                          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
        try:
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return e
    else:
        EquipIDList = []
        UnitIDList = []
        findUnitUperIDList(Unit_ID, UnitIDList)
        findEquipUperIDList(Equip_ID, EquipIDList)
        for UnitID in UnitIDList:
            for EquipID in EquipIDList:
                equipName = selectEquipNameByEquipID(EquipID)
                unitName = selectUnitNameByUnitID(UnitID)
                strengthInfo = selectWeaveInfo(UnitID, EquipID, year)  # 获取原有的实力数以及现有数

                if strengthInfo:
                    orginYearWorkNum = strengthInfo[0][5]
                else:
                    orginYearWorkNum = 0
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year) VALUES" \
                          + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                     " 0, 0,0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                          year +  "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                changeYearWorkNum = int(orginYearWorkNum) - int(orginWeave) + int(weaveNum)
                sql = "Update strength set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e

                sql = "Update weave set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                for lastYear in lastOtherYear:
                    sql = "Update strength set Work = Work - " + str(orginWeave) + " + " + str(weaveNum) + " where Equip_ID = '" + \
                          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

                    sql = "Update weave set Work = Work - " + str(orginWeave) + " + " + str(weaveNum) + " where Equip_ID = '" + \
                          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
        try:
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return e

def findBigOtherYear(year):
    sql = "select year from strengthyear where year   > '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    yearList = []
    for info in result:
        yearList.append(info[0])
    return yearList
# 根据单位号，装备号更新末年计划未移交量
def updatePlanUnhanded(Unit_ID, Equip_ID, year, newPlanUnhanded, orginPlanUnhanded):
    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    orginYearPlanUnhanded = 0
    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            planUnhandedNum = selectPlanUnhandedNum(UnitID, EquipID, year)
            if planUnhandedNum:
                orginYearPlanUnhanded = planUnhandedNum
            else:
                orginYearPlanUnhanded = 0
                sql = "INSERT INTO strength_maintance (Unit_ID, Equip_ID,Unit_Name, Equip_Name, Plan_Unhanded, year) VALUES" \
                      + "('" + UnitID + "','" + EquipID + "','" + unitName + "','" + equipName + "', 0,"  + "'" + year + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
            changeplanUnhandedNum = orginYearPlanUnhanded - int(orginYearPlanUnhanded) + int(newPlanUnhanded)
            sql = "Update strength_maintance set Plan_Unhanded = " + str(changeplanUnhandedNum) + " where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


# 根据单位号，装备号修改某年的实力数
def updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, strengthNum, orginStrengthNum):
    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    orginYearStrengthNum = 0
    LastYearList = findBigOtherYear(year)

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            strengthYearInfo = seletNumAboutStrength(UnitID, EquipID, year)
            if strengthYearInfo:
                orginYearStrengthNum = strengthYearInfo[0][4]
            else:
                orginYearStrengthNum = 0
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                           " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                      year+"')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
            changeYearStrengthNum = orginYearStrengthNum - int(orginStrengthNum) + int(strengthNum)
            sql = "Update strength set Strength = " + str(changeYearStrengthNum) + " where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            sql = "Update weave set Strength = " + str(changeYearStrengthNum) + " where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
            try:
                cur.execute(sql)
            except Exception as e:
                conn.rollback()
                return e

            for lastYear in LastYearList:
                strengthlastYearInfo = seletNumAboutStrength(UnitID, EquipID, lastYear)
                if strengthlastYearInfo:
                    orginLastYearStrengthNum = strengthlastYearInfo[0][4]
                else:
                    orginLastYearStrengthNum = 0
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                              "NonStrength, Single, Arrive, year) VALUES" \
                              + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', 0," \
                                                                                                         " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
                              lastYear + "')"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                changeLastYearStrengthNum = orginLastYearStrengthNum - int(orginStrengthNum) + int(strengthNum)

                sql = "Update strength set Strength = " + str(changeLastYearStrengthNum) + " where Equip_ID = '" + \
                        EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
                sql = "Update weave set Strength = " + str(changeYearStrengthNum) + " where Equip_ID = '" + \
                          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + lastYear + "'"

                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


# 查找所有末级装备
def selectAllEndEquip():
    resultList = []
    allEquipTuple = selectAllDataAboutEquip()
    for equipInfo in allEquipTuple:
        if selectEquipIsHaveChild(equipInfo[0]):
            pass
        else:
            resultList.append(equipInfo)
    return resultList

def selectAllEndUnit():
    resultList = []
    allEquipTuple = []
    selectAllDataAboutUnit(allEquipTuple)
    for unitInfo in allEquipTuple:
        if selectUnitIsHaveChild(unitInfo[0]):
            pass
        else:
            resultList.append(unitInfo)
    return resultList

# 查找实力查询所有年份名字
def selectAllStrengthYear():
    yearList = []
    sql = "SELECT * from strengthyear ORDER BY year"
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    for yearInfo in yearListTuple:
        yearList.append(yearInfo[1])
    return yearList



# 查找实力查询所有年份信息
def selectAllStrengthYearInfo():
    yearList = []
    sql = "SELECT * from strengthyear order by year"
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    return yearListTuple

def selectAllFromPulicEquipByUnit(UnitInfoList):
    resultList = []
    for UnitInfo in UnitInfoList:
        sql = "select * from publicequip where Group_ID = '" + UnitInfo[0] + "'"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            resultList.append(result[0])
    return resultList

# 获取公用装备信息
def selectAllFromPulicEquip():
    sql = "select * from publicequip"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectUnitInfoByUnitID(Unit_ID):
    sql = "select * from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for info in result:
        return info


def selectDisturbPlanUnitInfoByUnitID(Unit_ID):
    sql = "select * from disturbplanunit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for info in result:
        return info

def findUperIDByUnitID(Unit_ID):
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    unitUper = None
    result = cur.fetchall()
    for info in result:
        unitUper = info[0]
        break
    return unitUper

# 查找编制表中某个装备以及某个单位的编制数
def selectWorkNumFromWeave(Unit_ID, Equip_ID, year):
    sql = "select Work from weave where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return "0"


# 修改单位是否是旅团状态
def updateUnitIsGroupFromUnit(Unit_ID, Is_Group):
    if Is_Group == '否':
        uperUnitList = []
        findUnitUperIDList(Unit_ID, uperUnitList)
        equipInfoList = selectAllDataAboutEquip()
        publicEquipID = selectGroupIDByPublicEquip(Unit_ID)
        strengthYearList = selectAllDataAboutStrengthYear()
        sql = "update unit set Is_Group = '" + Is_Group + "' where Unit_ID = '" + Unit_ID + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        for uperUnitID in uperUnitList:
            for equipInfo in equipInfoList:
                for weaveYearInfo in strengthYearList:
                    orginYearWorkNum = selectWorkNumFromWeave(uperUnitID, equipInfo[0], weaveYearInfo[1])
                    delWorkYearNum = selectWorkNumFromWeave(publicEquipID, equipInfo[0], weaveYearInfo[1])
                    nowYearWorkNum = str(int(orginYearWorkNum) - int(delWorkYearNum))
                    sql = "update weave set Work = " + nowYearWorkNum + " where Equip_ID = '" + equipInfo[0] + \
                          "' and Unit_ID = '" + uperUnitID + "' and year = '" + weaveYearInfo[1] + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                    sql = "update strength set Work = " + nowYearWorkNum + " where Equip_ID = '" + equipInfo[0] + \
                          "' and Unit_ID = '" + uperUnitID + "' and year = '" + weaveYearInfo[1] + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e

        sql = "delete from publicequip where Group_ID = '" + Unit_ID + "'"

        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        sql = "delete from weave where Unit_ID = '" + publicEquipID + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
    else:
        result = selectAllFromPulicEquip()
        currentNum = len(result)
        sql = "update unit set Is_Group = '" + Is_Group + "' where Unit_ID = '" + Unit_ID + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        sql = "insert into publicequip (Equip_ID, Group_ID, work_Num) VALUES"\
              + "('"  + "gyzb" +  Unit_ID  + "', '" + Unit_ID + "', '0')"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
        equipInfoList = selectAllDataAboutEquip()
        weaveYearList = selectAllStrengthYearInfo()
        for equipInfo in equipInfoList:
            for weaveYearInfo in weaveYearList:
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + "gyzb" + Unit_ID + "','" + equipInfo[0] + "','公用装备','" + equipInfo[
                          1] + "', 0, 0, 0, '" + weaveYearInfo[1] + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    conn.rollback()
                    return e
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


# 查找某个旅团编号的公用装备编号
def selectGroupIDByPublicEquip(Group_ID):
    sql = "select Equip_ID from publicequip where Group_ID = '" + Group_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return "0"

def selectPubilcEquipInfoByGroupID(Group_ID):
    sql = "select * from publicequip where Group_ID = '" + Group_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        return resultInfo

# 查找某个公用装备编号所属的旅团编号
def selectEquipIDByPublicEquip(Equip_ID):
    sql = "select Group_ID from publicequip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return "0"


# 修改录入信息表的某个信息
def updateInputInfo(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    sql = "update inputinfo set year = '" + year + "', shop = '" + shop + "', state = '" \
          + state + "', arrive = '" + arrive + "', confirm = '" + confirm + "', other = '" + other + \
          "' where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and ID = '" + ID + "'"
    cur.execute(sql)
    conn.commit()
    return


# 获取某单位的所有子单位名称
def findUnitChildName(unitId):
    sql = "select Unit_Name from unit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result
    else:
        return []


def findDisturbPlanUnitChildInfo(unitId):
    sql = "select * from disturbplanunit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result
    else:
        return []



def findUnitChildInfo(unitId):
    sql = "select * from unit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result
    else:
        return []

#查询退休年份表
def selectAllRetirementYearInfo():
    sql = "select * from retireyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectLastYear():
    sql = "select ID from retireyear order by ID desc limit 1"
    cur.execute(sql)
    result = cur.fetchall()
    lastYear = -1
    if len(result) > 0:
        lastYear = result[0][0]
    return lastYear


def isHaveRecord(UnitID, EquipID, year):
    sql = "select * from retire where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


def selectEquipInfoByEquipID(EquipID):
    sql = "select * from equip where Equip_ID = '" + \
          EquipID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def isHaveEquipment(EquipID):
    sql = "select Equip_ID from equip where Equip_ID = '" + \
          EquipID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) != 0:
        return True
    else:
        return False

def findEquipInfo(equipId):
    sql = "select * from equip where Equip_ID = '" + equipId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result
    else:
        return []

# 查询编制信息
def selectWeaveInfo(UnitID, EquipID, year):
    sql = "select * from weave where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 插入退休表
def insertIntoRetire(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,strength,Weave, Num, Now, Super, Apply, Other, Unarrived, ProposedRetire, ProposedApply, year):
    sql = "insert into retire (ID, Unit_ID, Equip_ID, Equip_Name, Equip_Unit, Strenth, Weave, Num, Now, Super, Apply, Other,Unarrived , Proposed_retire, Proposed_apply , year) " \
          "VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s' , '%s')"%(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,strength,Weave, Num, Now, Super, Apply, Other, Unarrived, ProposedRetire, ProposedApply, year)
    executeCommit(sql)

# 查询退休信息
def selectInfoFromRetire(unitID, equipID, year):
    sql = "select * from retire where Unit_ID = '%s' and Equip_ID = '%s' and year = '%s'"%(unitID, equipID, year)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return list(result[0])
    else:
        return ''


def getStrengthNum(unitID, EquipID, year):
    sql = "select Strength from strength where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    num = 0
    if result != None and len(result) > 0:
        num = result[0][0]
    return num


# 查询实力信息
def selectStrengthInfo(unitID, EquipID, year):

    sql = "select * from strength where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectStrengthNum(unitID, EquipID, year):
    sql = "select Strength from strength where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectPlanUnhandedNum(unitID, EquipID, year):
    sql = "select Plan_Unhanded from strength_maintance where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    num = 0
    if result != None and len(result) > 0:
        num = result[0][0]
    return num

# 单位ID对应单位名
def findUnitNameFromID(UnitID):
    sql = "select Unit_Name from unit where Unit_ID = '" + UnitID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

# 查询前更新退休表
def selectUpdateIntoRetire(unitID, EquipID, year):
    weaveInfo = selectWeaveInfo(unitID, EquipID, year)
    strengthInfo = selectStrengthInfo(unitID, EquipID, year)
    if weaveInfo:
        weave = weaveInfo[0][5]
    else:
        weave = '0'
    if strengthInfo:
        strength = strengthInfo[0][4]
        now = strengthInfo[0][6]
    else:
        now = '0'
        strength = '0'

    super = str(int(now) - int(weave))
    sql = "update retire set Strenth='%s', Weave='%s',Now='%s',Super='%s' where Equip_ID='%s' and Unit_ID='%s' and year='%s'"%(strength, weave, now, super, EquipID, unitID, year)
    cur.execute(sql)


# 查询退休表
def selectAboutRetireByEquipShow(UnitList, EquipList, year):
    unitID = UnitList[0]
    result = []
    for EquipID in EquipList:
        m_isHaveRecord = isHaveRecord(unitID, EquipID, year)
        if m_isHaveRecord:
            selectUpdateIntoRetire(unitID, EquipID, year)
            currentResultInfo = selectInfoFromRetire(unitID, EquipID, year)
            result.append(currentResultInfo)
        else:
            currentResultInfo = []
            weaveInfo = selectWeaveInfo(unitID, EquipID, year)
            strengthInfo = selectStrengthInfo(unitID, EquipID, year)
            ID = unitID + EquipID + year
            equipInfo = selectEquipInfoByEquipID(EquipID)
            equipName = getFomatEquipmentName(equipInfo[0][0])
            equipUnit = equipInfo[0][5]
            if equipUnit:
                pass
            else:
                equipUnit = ""
            if weaveInfo:
                weave = weaveInfo[0][5]
            else:
                weave = '0'
            num = ''
            if strengthInfo:
                now = strengthInfo[0][6]
                strength = strengthInfo[0][4]
            else:
                strength = '0'
                now = '0'
            super = str(int(now) - int(weave))
            apply = ''
            other = ''
            haveChild = selectEquipIsHaveChild(EquipID)
            Unarrived = ''
            ProposedRetire = ''
            ProposedApply = ''
            insertIntoRetire(ID, unitID, EquipID, equipName, equipUnit, strength,weave, num, now, super, apply, other, Unarrived, ProposedRetire, ProposedApply,year)
            currentResultInfo = [ID, unitID, EquipID, equipName, equipUnit, strength,weave, num, now, super, apply, other, Unarrived, ProposedRetire, ProposedApply, year]
            result.append(currentResultInfo)
    return result

'''
    功能：
        得到对应装备号和单位号的武器的信号和现有数
'''
def findPlanToRetireItem(unitId,quipmentId,year):
    sql = "select ID,num from inputinfo where Unit_ID='%s' and Equip_ID='%s' and inputYear='%s'"%(unitId,quipmentId,year)
    result = selectDateDict(sql)
    if len(result) > 0:
        return result
    else:
        return None




# 查找某个装备的子目录
def selectChildEquip(Equip_ID):
    sql = "select * from equip where Equip_Uper = '" + \
          Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 判断是否为倒数第二级目录
def isSecondDict(EquipID):
    selfHaveChild = selectEquipIsHaveChild(EquipID)
    if selfHaveChild:
        child = selectChildEquip(EquipID)[0][0]
        selfHaveChild = selectEquipIsHaveChild(child)
        if selfHaveChild:
            return False
        else:
            return True
    else:
        return False


# 更新退休表
def updateRetireFromStrength(num, orginInfo):
    if orginInfo:
        sql = "update retire set Num = '" + num +  "' where Equip_ID = '" + orginInfo[2] + "' and Unit_ID = '" + orginInfo[1] + "' and year = '" + orginInfo[12] + "'"
    else:
        return
    cur.execute(sql)
    conn.commit()


#申请退役更新退休表
def updateRetire(num, apply, other, Unarrived, ProposedRetire, ProposedApply, orginInfo):
    if orginInfo:
        sql = "update retire set Num = '" + num + "', Apply = '" + apply + "', Other = '" + other + "', Unarrived = '" + Unarrived + "', Proposed_retire = '" + ProposedRetire + "', Proposed_apply = '" + ProposedApply +  \
              "' where Equip_ID = '" + orginInfo[2] + "' and Unit_ID = '" + orginInfo[1] + "' and year = '" + orginInfo[-2] + "'"
    else:
        return
    cur.execute(sql)
    conn.commit()


# 退役年份表中添加年份
def insertIntoRetireYear(year):
    result = selectAllRetirementYearInfo()
    sql = "insert into retireyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    cur.execute(sql)
    conn.commit()


# 删除某个退休年份
def delRetireYearByYear(year):
    sql = "delete from retireyear where year = '" + year + "'"
    cur.execute(sql)
    sql = "delete from retire where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()


# 删除退休表所有年份
def delRetireYearALLYear():
    sql = "delete from retireyear "
    cur.execute(sql)
    sql = "delete from retire "
    cur.execute(sql)
    conn.commit()

# def insertIntoWeaveYear(year):
#     allEquipList = selectAllDataAboutEquip()
#     allUnitList = selectAllDataAboutUnit()
#
#     result = selectAllDataAboutWeaveYear()
#     sql = "insert into weaveyear(ID, year) VALUES"\
#     + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
#     cur.execute(sql)
#
#     for equipInfo in allEquipList:
#         for unitInfo in allUnitList:
#             strengthInfo = selectStrengthInfo(equipInfo[0], unitInfo[0])
#             if strengthInfo:
#                 strength = strengthInfo[0][4]
#                 now = strengthInfo[0][6]
#             else:
#                 strength = "0"
#                 now = "0"
#             work = '0'
#             sql = "insert into weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
#                   + "('" + unitInfo[0] + "', '" + equipInfo[0] + "', '" + unitInfo[1] + "', '" + equipInfo[1] + "', '"\
#                   + strength + "', '" + work + "', '" + now + "','" + str(year) + "')"
#             print(sql)
#             cur.execute(sql)
#     conn.commit()


# 设置单位别名
def updateUnitAlias(Unit_Alias,Unit_ID):
    sql = "update unit set Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    sql = "update disturbplanunit set Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    conn.commit()


# 设置装备数量单位
def updateEquipUnit(unit, Equip_ID):
    sql = "update equip set unit = '" \
          + unit + "' where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    sql = "update retire set Equip_Unit = '" \
          + unit + "' where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    conn.commit()


#查找某个年份的所有inputinfo
def selectInputInfoByYear(year):
    sql = "select * from inputinfo where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


def delStrengthYearByYear(year):
    equipInfoList = selectAllDataAboutEquip()
    unitInfoList = []
    selectAllDataAboutUnit(unitInfoList)
    lastYearList = findBigOtherYear(year)
    for equipInfo in equipInfoList:
        for unitInfo in unitInfoList:
            strengthInfo = selectStrengthInfo(unitInfo[0], equipInfo[0], year)
            if strengthInfo:
                for lastYear in lastYearList:
                    sql = "update strength set Strength = Strength - " + str(strengthInfo[0][4]) \
                      + ", Work = Work - " + str(strengthInfo[0][5]) + ", Now = Now - " + str(strengthInfo[0][6]) + " where Equip_ID = '" + equipInfo[0]\
                      + "' and Unit_ID = '" + unitInfo[0] + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
                    sql = "update weave set Strength = Strength - " + str(strengthInfo[0][4]) \
                          + ", Work = Work - " + str(strengthInfo[0][5]) + ", Now = Now - " + str(strengthInfo[0][
                              6]) + " where Equip_ID = '" + equipInfo[0] \
                          + "' and Unit_ID = '" + unitInfo[0] + "' and year = '" + lastYear + "'"
                    try:
                        cur.execute(sql)
                    except Exception as e:
                        conn.rollback()
                        return e
    inputInfoTuple = selectInputInfoByYear(year)
    for inputInfo in inputInfoTuple:
        sql = "delete from inputinfo where ID = '" + inputInfo[2] + "'"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            return e
    sql = "delete from weave where year = '" + year + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "delete from strength where year = '" + year + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "delete from inputinfo where inputYear = '" + year + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e

    sql = "delete from strengthyear where year = '" + year + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return e
    deleteByYear(year)
    try:
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return e


def selectAllIDFromUnit():
    sql = "select Unit_ID from unit "
    cur.execute(sql)
    result = cur.fetchall()
    unitIDList = []
    for unitID in result:
        unitIDList.append(unitID[0])
    return unitIDList


def selectAllIDFromEquip():
    sql = "select Equip_ID from equip "
    cur.execute(sql)
    result = cur.fetchall()
    equipIDList = []
    for equipID in result:
        equipIDList.append(equipID[0])
    return equipIDList


#根据装备ID查找某个装备的单位
def findEquipUnitByEquipID(EquipID):
    sql = "select unit from equip where Equip_ID ='" + EquipID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


def findUperEquipIDByName(Equip_Name):
    sql = "select * from equip where Equip_Name ='" + Equip_Name + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


def selectUnitIfUppermost(Unit_Id):
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_Id + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result[0][0]== '':
        return True
    else:
        return False


def findUperInfoList(EquipID, UperList):
    if EquipID == "":
        return
    else:
        sql = "select Equip_Uper from equip where Equip_ID = '" + EquipID + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            UperList.append(resultInfo)
            if resultInfo:
                findUperInfoList(resultInfo[0], UperList)


def selectUperInfoByEquipID(EquipID):
    UperList = []
    findUperInfoList(EquipID, UperList)
    return UperList


#从excel中将数据导入unit
def inputIntoUnitFromExcel(unitInfoList):
    errorInfo = []
    equipInfoTuple = selectAllDataAboutEquip()
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    disturbplanYearInfoTuple = selectYearListAboutDisturbPlan()

    unitInfoList.insert(0, ['1', '火箭军', '', ''])
    for i, unitInfo in enumerate(unitInfoList):
        unitID = unitInfo[0]
        unitName = unitInfo[1]
        unitUper = unitInfo[2]
        unitAlias = unitInfo[3]
        isGroup = ''
        if unitID == "":
            error = "第 " + str(i) + " 行导入失败，单位编号不能为空"
            errorInfo.append(error)
            continue
        if selectUnitInfoByUnitID(unitID):
            error = "第 " + str(i) + " 行导入失败，单位编号重复"
            errorInfo.append(error)
            continue
        if unitName == '':
            error = "第 " + str(i) + " 行导入失败，单位名字不能为空"
            errorInfo.append(error)
            continue
        addDataIntoUnit(unitID, unitName, unitUper, unitAlias, isGroup)
    return True
    #     sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
    #       + "('" + unitID + "','" + unitName + "','" + unitUper + "', '" + unitAlias + "', '" + isGroup + "')"
    #     try:
    #         cur.execute(sql)
    #     except Exception as e:
    #         error = "第 " + str(i) + " 行导入失败, " + str(e)
    #         errorInfo.append(error)
    #         continue
    #     for equipInfo in equipInfoTuple:
    #         for strengthYearInfo in strengthYearInfoTuple:
    #             sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
    #                   "NonStrength, Single, Arrive, year) VALUES" \
    #                   + "('" + equipInfo[0] + "','" + unitID + "','" + equipInfo[1] + "','" + unitName + "', 0," \
    #                                                                                                        " 0, 0, 0,0, 0, 0, 0, 0, 0, 0," + "'" + \
    #                   strengthYearInfo[1] + "')"
    #             try:
    #                 cur.execute(sql)
    #             except Exception as e:
    #                 error = "第 " + str(i) + " 行导入失败, " + str(e)
    #                 conn.rollback()
    #                 errorInfo.append(error)
    #                 continue
    #
    #             sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
    #                   + "('" + unitID + "','" + equipInfo[0] + "','" + unitName + "','" + equipInfo[
    #                       1] + "', 0, 0, 0, '" + strengthYearInfo[1] + "')"
    #             try:
    #                 cur.execute(sql)
    #             except Exception as e:
    #                 error = "第 " + str(i) + " 行导入失败, " + str(e)
    #                 conn.rollback()
    #                 errorInfo.append(error)
    #                 continue
    # try:
    #     conn.commit()
    #     if errorInfo != []:
    #         return errorInfo
    #     else:
    #         return True
    # except Exception as e:
    #     error = "commit 失败"
    #     conn.rollback()
    #     errorInfo.append(error)
    #     return errorInfo


def isHaveStrengthYear(year):
    sql = "select * from strengthYear where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


def insertOneDataIntoStrenth(lineInfo):
    #['5', '10', 'A车', '六十一旅团一阵地', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2000']
    if selectIfExistsStrengthYear(lineInfo[-1]) == False:
        year = str(lineInfo[-1])
        sql = "insert into strengthyear(ID, year) values ('" + year + "', '" + year + "')"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()

    result = selectStrengthInfo(lineInfo[0], lineInfo[1], lineInfo[-1])
    if result == None or len(result) == 0:
        sql = "insert into strength values('%s','%s','%s','%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%s')"%(lineInfo[0], lineInfo[1], lineInfo[2],
        lineInfo[3], lineInfo[4], lineInfo[5], lineInfo[6], lineInfo[7], lineInfo[8], lineInfo[9], lineInfo[10], lineInfo[11], lineInfo[12], lineInfo[13],
        lineInfo[14], lineInfo[15])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    else:
        sql = "update strength set  Strength = '%d', Work = '%d', Now = '%d', Error = '%d', Retire = '%d', Delay = '%d', Pre = '%d', NonObject = '%d', NonStrength =" \
              " '%d', Single = '%d', Arrive = '%d' where Equip_ID = '%s' and Unit_ID = '%s'and year = '%s' " %(lineInfo[4],lineInfo[5], lineInfo[6], lineInfo[7], lineInfo[8], lineInfo[9], lineInfo[10], lineInfo[11], lineInfo[12], lineInfo[13],
        lineInfo[14], lineInfo[0], lineInfo[1], lineInfo[-1])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    try:
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def inputOneDataIntoStrenth(lineInfo):
    #['单位编号', '单位名称', '装备编号', '装备名称', '实力数'， ’年份‘]
    #['8', '六十一阵地', '5', 'A车', '1', '2001']
    if selectIfExistsStrengthYear(lineInfo[-1]) == False:
        year = str(lineInfo[-1])
        sql = "insert into strengthyear(ID, year) values ('" + year + "', '" + year + "')"
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()

    result = selectStrengthInfo(lineInfo[0], lineInfo[2], lineInfo[-1])
    if result == None or len(result) == 0:
        # ['5', '10', 'A车', '六十一旅团一阵地', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2000']
        #['单位编号', '单位名称', '装备编号', '装备名称', '实力数'， ’年份‘]
        #['8', '六十一阵地', '5', 'A车', '1', '2001']
        sql = "insert into strength values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        lineInfo[2], lineInfo[0], (lineInfo[3]).strip(),
        (lineInfo[1]).strip(), lineInfo[4], '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', lineInfo[-1])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    else:
        sql = "update strength set  Strength = '%s' where Equip_ID = '%s' and Unit_ID = '%s'  and year = '%s'" % (lineInfo[4], lineInfo[2], lineInfo[0], lineInfo[-1])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    try:
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def insertOneDataIntoRetire(lineInfo):
    # ['8102001', '8', '10', '    C车', '辆', 0, '2', '0', '0', '-2', '2', '3', '3', '3', '3', '2001', True]
    if selectIfExistsRetireYear(lineInfo[-2]) == False:
        year = str(lineInfo[-1])
        sql = "insert into retireyear(year) values ('%s')"%year
        try:
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
    result = selectInfoFromRetire(lineInfo[1], lineInfo[2], lineInfo[-2])
    if result == None or len(result) == 0:
        # ['8102001', '8', '10', '    C车', '辆', 0, '2', '0', '0', '-2', '2', '3', '3', '3', '3', '2001', True]
        sql = "insert into retire values('%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s', '%s','%s', '%s')" % (
        lineInfo[0], lineInfo[1], lineInfo[2],
        lineInfo[3], lineInfo[4], lineInfo[5], lineInfo[6], lineInfo[7], lineInfo[8], lineInfo[9], lineInfo[10],
        lineInfo[11], lineInfo[12], lineInfo[13], lineInfo[14], lineInfo[-2])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    else:
        # ['8102001', '8', '10', '    C车', '辆', 0, '2', '0', '0', '-2', '2', '3', '3', '3', '3', '2001', True]
        sql = "update retire set  Unit_ID = '%s', Equip_ID = '%s', Equip_Name = '%s', Equip_Unit = '%s', Strenth = '%d', Weave = '%s', Num = '%s', Now =" \
              " '%s', Super = '%s',Apply = '%s', Other = '%s', Unarrived = '%s', Proposed_retire = '%s', Proposed_apply = '%s', year = '%s' where ID = '%s'" % (
              lineInfo[1], lineInfo[2], lineInfo[3], lineInfo[4], lineInfo[5], lineInfo[6], lineInfo[7], lineInfo[8],
              lineInfo[9], lineInfo[10],
              lineInfo[11], lineInfo[12], lineInfo[13], lineInfo[14], lineInfo[15], lineInfo[0])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            conn.rollback()
    try:
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def selectIfExistsRetireYear(year):
    sql = "select year from strengthyear where year = %s"%year
    cur.execute(sql)
    result = cur.fetchall()
    if result == None or len(result) < 1:
        return False
    else:
        return True

if __name__ == '__main__':
    pass
