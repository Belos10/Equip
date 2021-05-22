import pymysql
from database.connectAndDisSql import connectMySql, disconnectMySql
from database.SD_EquipmentBanlanceSql import updateOneEquipmentBalanceData
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
def findChildUnit(Unit_ID, childUnitList, cur):
    childUnitList.append(Unit_ID)
    sql = "select Unit_ID from unit where Unit_Uper = '" + Unit_ID + "'"
    cur.execute(sql)
    ID_tuple = cur.fetchall()
    for ID in ID_tuple:
        findChildUnit(ID[0], childUnitList, cur)


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


'''
    功能：
        查询编制表时找到某个单位的所有下级单位
        Unit_ID: 需要找的单位的ID号
        childUnitList：存放该单位所有下级单位，包括自己，自己在0位置
        cur：执行sql语句
'''
def findChildUnitByWeave(Unit_ID, childUnitList, cur):
    childUnitList.append(Unit_ID)
    isGroup = selectUnitIsGroup(Unit_ID)
    if isGroup:
        publicEquipID = selectGroupIDByPublicEquip(Unit_ID)
        childUnitList.append(publicEquipID)
    sql = "select Unit_ID from unit where Unit_Uper = '" + Unit_ID + "'"
    cur.execute(sql)
    ID_tuple = cur.fetchall()
    for ID in ID_tuple:
        findChildUnitByWeave(ID[0], childUnitList, cur)


'''
    功能：
        找到某个装备的所有下级单位
        Unit_ID: 需要找的装备的ID号
        childUnitList：存放该单位所有下级装备，包括自己，自己在0位置
        cur：执行sql语句
'''
def findChildEquip(Equip_ID, childEquipList, cur):
    childEquipList.append(Equip_ID)
    sql = "select Equip_ID from equip where Equip_Uper = '" + Equip_ID + "'"
    cur.execute(sql)
    Equip_tuple = cur.fetchall()
    for equip in Equip_tuple:
        findChildEquip(equip[0], childEquipList, cur)


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
    功能：
        通过单位号找到装备名字
        Unit_ID: 需要找的装备的ID号 
'''
def selectEquipNameByEquipID(Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select Equip_Name from equip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    equipName = cur.fetchall()
    for name in equipName:
        return name[0]


'''
    功能：
        通过单位号找到该单位的所有下级单位，以及下级单位的下级单位
        例如：001->002->003
            则存储为：[[001, 002, 003], [002, 003], [003]]
        Unit_ID: 需要找的单位的ID号 
        UnitList：存储该单位以及其下级单位的结构，结果为二维嵌套列表
        cur：执行sql语句
'''
def findUnitList(UnitID, UnitList, cur):
    childUnitList = []
    findChildUnit(UnitID, childUnitList, cur)
    UnitList.append(childUnitList)
    sql = "select Unit_ID from unit where Unit_Uper = '" + UnitID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for data in result:
        findUnitList(data[0], UnitList, cur)


'''
    功能：
        通过装备号找到该装备的所有下级装备，以及下级装备的下级单位
        例如：001->002->003
            则存储为：[[001, 002, 003], [002, 003], [003]]
        Equip_ID: 需要找的装备的ID号 
        UnitList：存储该装备以及其下级装备的结构，结果为二维嵌套列表
        cur：执行sql语句
'''
def findEquipList(EquipID, EquipList, cur):
    childEquipList = []
    findChildEquip(EquipID, childEquipList, cur)
    EquipList.append(childEquipList)
    sql = "select Equip_ID from equip where Equip_Uper = '" + EquipID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for data in result:
        findEquipList(data[0], EquipList, cur)


'''
    功能：
        判断装备是否是最底层装备
'''
def EquipNotHaveChild(Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        return False
    else:
        return True


'''
    功能：
        判断单位是否是最底层单位
'''
def UnitNotHaveChild(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "select * from unit where Unit_Uper = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        return False
    else:
        return True

'''
    功能：
        找到某个单位的一级上级单位
'''
def selectUnitDictByUper(Unit_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select * from unit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


'''
    功能：
        增加装备目录
'''
def add_UnitDictEquip(Equip_ID, Equip_Name, Equip_Uper):
    # print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO equip (Equip_ID, Equip_Name, Equip_Uper) VALUES" \
          + "('" + Equip_ID + "','" + Equip_Name + "','" + Equip_Uper + "')"
    # print(sql)
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 更改装备目录
def update_Equip_Dict(Equip_ID, Equip_Name, Equip_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "Update equip set Equip_Name = '" + Equip_Name + "', Equip_Uper = '" + Equip_Uper \
          + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 删除装备及子目录
def del_Equip_And_Child(Equip_ID, Equip_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from equip where Equip_ID = '" + Equip_ID + "'" + "and Equip_Uper = '" + Equip_Uper + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 删除装备目录
def del_Equip_Dict(Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from equip where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

#根据Dept_Uper查询单位信息,并返回
def selectUnitInfoByDeptUper(Unit_Uper):
    conn, cur = connectMySql()
    sql = "select * from unit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


#根据Dept_Uper查询单位信息,并返回
def selectDisturbPlanUnitInfoByDeptUper(Unit_Uper):
    conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_Uper = '" + Unit_Uper + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


# 返回disturbplanunit单位表的所有数据
def selectAllDataAboutDisturbPlanUnit():
    conn, cur = connectMySql()
    sql = "select * from disturbplanunit order by Unit_ID"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


# 返回disturbplanunit单位表除机关外的所有数据
def selectAllDataAboutDisturbPlanUnitExceptFirst():
    conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_Uper != ''"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


# 返回unit单位表的所有数据
def selectAllDataAboutUnit():
    conn, cur = connectMySql()

    sql = "select * from unit order by Unit_ID"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    #print("单位表所有数据result",result)

    return result


# 根据Equip_Uper查询单位信息,并返回
def selectEquipInfoByEquipUper(Equip_Uper):
    conn, cur = connectMySql()

    sql = "select * from equip where Equip_Uper = '" + Equip_Uper + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result




# 返回equip装备表的所有数据
def selectAllDataAboutEquip():
    conn, cur = connectMySql()

    sql = "select * from equip"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#查询所有出厂年份
def selectAllDataAboutFactoryYear():
    conn, cur = connectMySql()

    sql = "select * from factoryyear order By year"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result




# 查找所有的编制年份
def selectAllDataAboutWeaveYear():
    conn, cur = connectMySql()

    sql = "select * from weaveyear"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result



def selectAllDataAboutDisturbPlan():
    conn, cur = connectMySql()
    sql = "select * from disturbplanyear"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

def addDataIntoDisturbPlanUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    sql = "INSERT INTO disturbplanunit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', '' ,Is_Group = '否')"
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

# 往单位表unit中插入一条数据
def addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', '' ,Is_Group = '否')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    sql = "INSERT INTO disturbplanunit (Unit_ID, Unit_Name, Unit_Uper,Unit_Alias, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', '', Is_Group = '否')"
    cur.execute(sql)


    equipInfoTuple = selectAllDataAboutEquip()
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    factoryYearInfoTuple = selectAllDataAboutFactoryYear()
    disturbplanYearInfoTuple = selectAllDataAboutDisturbPlan()

    for equipInfo in equipInfoTuple:
        for strengthYearInfo in strengthYearInfoTuple:
            for factoryYearInfo in factoryYearInfoTuple:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
                                                                                                           " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      strengthYearInfo[1] + "', '" + factoryYearInfo[1] + "')"
                cur.execute(sql)

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + Unit_ID + "','" + equipInfo[0] + "','" + Unit_Name + "','" + equipInfo[
                      1] + "', '0', '0', '0', '" + strengthYearInfo[1] + "')"
            cur.execute(sql)

            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
                                                                                                       " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                  strengthYearInfo[1] + "', '" + "" + "')"
            cur.execute(sql)

        for disturbplanYearInfo in disturbplanYearInfoTuple:
            sql = "insert into disturbplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " \
                  + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + Unit_ID +\
                  "','" + Unit_Name + "','"+ disturbplanYearInfo[1] +"', '' )"
            cur.execute(sql)


    conn.commit()
    disconnectMySql(conn, cur)


# 往装备表equip中插入一条数据
def addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "INSERT INTO equip (Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, unit) VALUES" \
          + "('" + Equip_ID + "','" + Equip_Name + "','" + Equip_Uper + "','" + Input_Type + "','" + Equip_Type + "', '')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    unitInfoTuple = selectAllDataAboutUnit()
    factoryYearInfoTuple = selectAllDataAboutFactoryYear()
    disturbplanYearInfoTuple = selectAllDataAboutDisturbPlan()

    # print(unitInfoTuple)
    for unitInfo in unitInfoTuple:
        for strengthYearInfo in strengthYearInfoTuple:
            for factoryYearInfo in factoryYearInfoTuple:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
                      + " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'" + ",'" + strengthYearInfo[1] + "', '" + \
                      factoryYearInfo[1] + "')"
                cur.execute(sql)

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + Equip_ID + "','" + unitInfo[
                      1] + "','" + Equip_Name + "', '0', '0', '0', '" + \
                  strengthYearInfo[1] + "')"
            cur.execute(sql)

            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
                  + " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'" + ",'" + strengthYearInfo[1] + "', '" + \
                  "" + "')"
            # print(sql)
            cur.execute(sql)

        for disturbplanYearInfo in disturbplanYearInfoTuple:
            sql = "insert into disturbplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " \
                  + "('" + Equip_ID + "','" + Equip_Name + "','" + unitInfo[0] +\
                  "','" + unitInfo[1] + "','"+ disturbplanYearInfo[1] +"', '' )"
            cur.execute(sql)
    for disturbplanYearInfo in disturbplanYearInfoTuple:
        sql = "insert into disturbplannote (Equip_Id,Equip_Name,Year,Note) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "','" + disturbplanYearInfo[1] + "', '' )"
        cur.execute(sql)
        sql = "insert into allotschedule (Equip_Id,Equip_Name,army,allotcondition,rocket,finish,year) values " \
              + "('" + Equip_ID + "','" + Equip_Name + "', '0','0','0','0','" + disturbplanYearInfo[1] + "' )"
        cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 单位表disturbplanunit中修改一条数据
def updateDataIntoDisturbPlanUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    sql = "Update disturbplanunit set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


#单位表unit中修改一条数据
def updateDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "Update unit set Unit_Name = '" + Unit_Name + "', Unit_Uper = '" + Unit_Uper + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    sql = "Update strength set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update weave set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update disturbplan set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update disturbplanunit set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)


    conn.commit()
    disconnectMySql(conn, cur)


# 单位表equip中修改一条数据
def updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "Update equip set Equip_Name = '" + Equip_Name + "', Equip_Uper = '" + Equip_Uper + "', Input_Type = '" + Input_Type + \
          "', Equip_Type = '" + Equip_Type + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    sql = "Update strength set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update weave set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update disturbplan set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update disturbplannote set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    cur.execute(sql)

    sql = "Update allotschedule set Equip_Name = '" + Equip_Name + "' where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 找到某个旅团的公用装备信息
def findChildUnitForPublic(Unit_ID):
    conn, cur = connectMySql()
    sql = "select * from pubilcequip where Group_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 单位表disturbplanunit中删除一条数据
def delDataInDisturbPlanUnit(Unit_ID):
    conn, cur = connectMySql()
    # 插入的sql语句
    UnitIDList = []
    findChildDisturbPlanUnit(Unit_ID, UnitIDList, cur)
    print(UnitIDList)
    for UnitID in UnitIDList:
        if UnitID != '':
            sql = "Delete from disturbplanunit where Unit_ID = '" + UnitID + "'"
            cur.execute(sql)
            sql = "Delete from disturbplan where Unit_ID = '" + UnitID + "'"
            cur.execute(sql)
            # print(sql)
        else:
            sql = "Delete from disturbplanunit where Unit_ID is null"
            cur.execute(sql)
            sql="Delete from disturbplan where Unit_ID is null"
            cur.execute(sql)


    conn.commit()
    disconnectMySql(conn, cur)



# 单位表unit中删除一条数据
def delDataInUnit(Unit_ID):
    conn, cur = connectMySql()
    # 插入的sql语句
    UnitIDList = []
    findChildUnit(Unit_ID, UnitIDList, cur)

    for UnitID in UnitIDList:
        sql = "Delete from unit where Unit_ID = '" + UnitID + "'"
        # print(sql)
        # 执行sql语句，并发送给数据库
        cur.execute(sql)

        sql = "Delete from inputinfo where Unit_ID = '" + UnitID + "'"
        cur.execute(sql)

        sql = "Delete from strength where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)

        publicInfo = findChildUnitForPublic(UnitID)
        for public in publicInfo:
            sql = "Delete from pubilcequip where Equip_ID = '" + public[0] + "'"
            # print(sql)
            cur.execute(sql)

            sql = "Delete from weave where Unit_ID = '" + public[0] + "'"
            # print(sql)
            cur.execute(sql)

        sql = "Delete from weave where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from disturbplan where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from disturbplanunit where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from retire where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)


    conn.commit()
    disconnectMySql(conn, cur)


# 装备表equip中删除一条数据
def delDataInEquip(Equip_ID):
    conn, cur = connectMySql()
    # 插入的sql语句
    EquipIDList = []
    findChildEquip(Equip_ID, EquipIDList, cur)

    for EquipID in EquipIDList:
        sql = "Delete from equip where Equip_ID = '" + EquipID + "'"
        # print(sql)
        # 执行sql语句，并发送给数据库
        cur.execute(sql)

        sql = "Delete from inputinfo where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from strength where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)
        # print(sql)

        sql = "Delete from weave where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from disturbplan where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from disturbplannote where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from allotschedule where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from retire where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from rockettransfer where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

        sql = "Delete from armytransfer where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 返回strengthyear表中所有信息
def selectAllDataAboutStrengthYear():
    conn, cur = connectMySql()

    sql = "select * from strengthyear order by year"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#按照单位编号，装备编号以及录入年份查找录入信息
def selectInfoAboutInput(Unit_ID, Equip_ID, inputYear, factoryYear):
    conn, cur = connectMySql()

    resultList = []
    if factoryYear == "":
        sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" \
              + Equip_ID + "' and inputYear = '" + inputYear + "'"
    else:
        sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '"\
          + Equip_ID + "' and inputYear = '" + inputYear + "' and year = '" + factoryYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(resultInfo)

    disconnectMySql(conn, cur)
    return resultList


# 判断当前是否为公用装备
def selectIsPublicEquip(Unit_ID):
    conn, cur = connectMySql()

    sql = "select * from pubilcequip where Equip_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    if result:
        return True
    else:
        return False


# 按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutWeaveByEquipShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            # 查询当前装备ID的孩子序列
            EquipIDChildList = []
            findChildEquip(Equip_ID, EquipIDChildList, cur)
            for childEquipID in EquipIDChildList:
                sql = "select * from weave where Unit_ID = '" + Unit_ID + \
                        "' and Equip_ID = '" + childEquipID + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    resultList.append(resultInfo)
    disconnectMySql(conn, cur)
    return resultList


# 按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByEquipShow(UnitList, EquipList, yearList,equipYear,startYear, endYear):
    conn, cur = connectMySql()
    resultList = []
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            # 查询当前装备ID的孩子序列
            EquipIDChildList = []
            findChildEquip(Equip_ID, EquipIDChildList, cur)
            for childEquipID in EquipIDChildList:
                unitName = selectUnitNameByUnitID(Unit_ID)
                equipName = selectEquipNameByEquipID(childEquipID)
                if equipYear == "":
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                        "' and Equip_ID = '" + childEquipID + "' and year = '" + yearList + "' and equipYear = '" + equipYear + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        info = list(resultInfo)
                        info[7] = str(int(info[4]) - int(info[6]))
                        resultList.append(info)
                else:
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                          "' and Equip_ID = '" + childEquipID + "' and year = '" + yearList + "' and equipYear between '" \
                          + startYear + "' and '" + endYear + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    #print(result, "+++++++++++++++++++")
                    if result:
                        info = list(result[0])
                        for resultInfo in result[1:]:
                            info[6] = str(int(info[6]) + int(resultInfo[6]))

                        info[7] = str(int(info[4]) - int(info[6]))
                        resultList.append(info)
                    else:
                        info = []
                        info.append(childEquipID, Unit_ID, equipName, unitName, "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0")
                        resultList.append(info)
    disconnectMySql(conn, cur)
    return resultList


# 判断当前单位是否是旅团
def selectUnitIsGroup(Unit_ID):
    conn, cur = connectMySql()

    sql = "select * from unit where Is_Group = '是' and Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    if result:
        return True
    else:
        return False


# 按单位展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    # if len(yearList) == 1:
    # 如果查询全部年的

    if yearList == '全部':
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                # 查询当前单位ID的孩子序列
                UnitIDChildList = []
                findChildUnitByWeave(Unit_ID, UnitIDChildList, cur)
                for childUnitID in UnitIDChildList:
                    sql = "select * from weave where Unit_ID = '" + childUnitID + "' and Equip_ID = '" + Equip_ID + "' and year = ''"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    # 如果查询某一年的
    else:
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                # 查询当前单位ID的孩子序列
                UnitIDChildList = []
                findChildUnitByWeave(Unit_ID, UnitIDChildList, cur)
                for childUnitID in UnitIDChildList:
                    sql = "select * from weave where Unit_ID = '" + childUnitID + \
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)

    disconnectMySql(conn, cur)
    return resultList

# 按单位展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitShow(UnitList, EquipList, yearList, equipYear, startFactoryYear, endFactoryYear):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    #if len(yearList) == 1:
        # 如果查询全部年的
    for Equip_ID in EquipList:
        for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
            UnitIDChildList = []
            findChildUnit(Unit_ID, UnitIDChildList, cur)
            for childUnitID in UnitIDChildList:
                unitName = selectUnitNameByUnitID(childUnitID)
                equipName = selectEquipNameByEquipID(Equip_ID)
                if equipYear == "":
                    sql = "select * from strength where Unit_ID = '" + childUnitID + \
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "' and equipYear = '" + equipYear + "'"
                    cur.execute(sql)
                    print(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        info = list(resultInfo)
                        info[7] = str(int(info[4]) - int(info[6]))
                        resultList.append(info)
                else:
                    sql = "select * from strength where Unit_ID = '" + childUnitID + \
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + \
                          "' and equipYear between '" + startFactoryYear + "' and '" + endFactoryYear + "'"
                    cur.execute(sql)
                    print(sql)
                    result = cur.fetchall()
                    if result:
                        info = list(result[0])
                        for resultInfo in result[1:]:
                            info[6] = str(int(info[6]) + int(resultInfo[6]))
                        info[7] = str(int(info[4]) - int(info[6]))
                        resultList.append(info)
                    else:
                        info = []
                        info.append(Equip_ID, childUnitID, equipName, unitName, "0", '0', '0', '0',
                                    '0', '0', '0', '0', '0', '0', '0', '0', '0')

    disconnectMySql(conn, cur)
    return resultList


def insertIntoStrengthYear(year):
    conn, cur = connectMySql()
    year = str(year)
    result = selectAllStrengthYearInfo()
    sql = "insert into strengthyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
    print(sql)
    cur.execute(sql)

    equipList = selectAllDataAboutEquip()
    unitList = selectAllDataAboutUnit()
    factoryYearInfo = selectAllDataAboutFactoryYear()

    for equipInfo in equipList:
        for unitInfo in unitList:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[
                      1] + "', '0'," \
                           " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                  year + "', '" + '' + "')"
            cur.execute(sql)

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + equipInfo[0] + "','" + unitInfo[1] + "','" + equipInfo[
                      1] + "', '0', '0', '0', '" + year + "')"
            print(sql)
            cur.execute(sql)

            for factoryYear in factoryYearInfo:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[
                          1] + "', '0'," \
                               " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      year + "', '" + factoryYear[1] + "')"
                cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

def selectDataFromStrengthByYear(year):
    conn, cur = connectMySql()
    sql = "select * from strength where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectDataFromInputByYear(year):
    conn, cur = connectMySql()
    sql = "select * from inputinfo where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def selectDataFromWeaveByYear(year):
    conn, cur = connectMySql()
    sql = "select * from weave where year = '" + str(year) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

def insertBeforYearIntoStrength(year):
    conn, cur = connectMySql()
    beforYearStrengthInfo  = selectDataFromStrengthByYear(year - 1)
    beforYearInputInfoTuple = selectDataFromInputByYear(year - 1)
    weaveInfoTuple = selectDataFromWeaveByYear(year - 1)
    equipList = selectAllDataAboutEquip()
    unitList = selectAllDataAboutUnit()
    #导入去年的数据
    if beforYearStrengthInfo:
        year = str(year)
        result = selectAllStrengthYearInfo()
        sql = "insert into strengthyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
        cur.execute(sql)
        for strengthInfo in beforYearStrengthInfo:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + strengthInfo[0] + "','" + strengthInfo[1] + "','" + strengthInfo[2] + "','" + strengthInfo[3] + "','" \
                  + strengthInfo[4] + "','" + strengthInfo[5] + "','" + strengthInfo[6] + "','" + strengthInfo[7] + "','" + strengthInfo[8]\
                  + "','" + strengthInfo[9] + "','" + strengthInfo[10] + "','" + strengthInfo[11] + "','" + strengthInfo[12] + "','" + strengthInfo[13]\
                  + "','" + strengthInfo[15]  + "','" + year + "','" + strengthInfo[16] + "')"
            cur.execute(sql)
        if beforYearInputInfoTuple:
            for inputInfo in beforYearInputInfoTuple:
                sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, inputYear) VALUES" \
                  + "('" + inputInfo[0] + "','" + inputInfo[1] + "','" + inputInfo[2] + "', '" + inputInfo[3] + "', '" + inputInfo[4] + "', '"\
                  + inputInfo[5] + "', '" + inputInfo[6] + \
                  "', '" + inputInfo[7] + "', '" + inputInfo[8] + "', '" + inputInfo[9] + "', '" + year + "')"
            cur.execute(sql)

    #导入去年的编制数表记录
    if weaveInfoTuple:
        year = str(year)
        for weaveInfo in weaveInfoTuple:
            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + weaveInfo[0] + "','" + weaveInfo[1] + "','" + weaveInfo[2] + "','" + weaveInfo[
                      3] + "', '" + weaveInfo[4] + "', '" + weaveInfo[5] + "', '" + weaveInfo[6] + "','" + year + "')"
            print(sql)
            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)
    return

def selectIDFromInputInfo(EquipID, UnitID, strengthYear):
    conn, cur = connectMySql()
    sql = "select ID from inputinfo where Equip_ID = '" + EquipID + "' and Unit_ID = '" + UnitID + "' and inputYear = '" + strengthYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

'''
    新增一个实力查询年份
'''
def insertIntoStrengthYear(year):
    conn, cur = connectMySql()
    year = str(year)
    result = selectAllStrengthYearInfo()
    sql = "insert into strengthyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
    #print(sql)
    cur.execute(sql)

    equipList = selectAllDataAboutEquip()
    unitList = selectAllDataAboutUnit()
    factoryYearInfo = selectAllDataAboutFactoryYear()

    for equipInfo in equipList:
        for unitInfo in unitList:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[
                      1] + "', '0'," \
                           " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                  year + "', '" + '' + "')"
            cur.execute(sql)

            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + equipInfo[0] + "','" + unitInfo[1] + "','" + equipInfo[
                      1] + "', '0', '0', '0', '" + year + "')"
            print(sql)
            cur.execute(sql)

            for factoryYear in factoryYearInfo:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[
                          1] + "', '0'," \
                               " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      year + "', '" + factoryYear[1] + "')"
                cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

# 没有展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitListAndEquipList(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    # print(UnitList, EquipList)
    temp = ['Unit_ID', 'Equip_ID', 'Unit_Name', 'Equip_Name', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    # if len(yearList) == 1:
    # 如果查询全部年的
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            sql = "select * from weave where Unit_ID = '" + Unit_ID + \
                      "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
            print(sql)
            cur.execute(sql)
            result = cur.fetchall()
            for resultInfo in result:
                resultList.append(resultInfo)
    disconnectMySql(conn, cur)
    return resultList

#没有展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, yearList, equipYear, startFactoryYear, endFactoryYear):
    conn, cur = connectMySql()
    # print(UnitList, EquipList)
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    #如果只查询某年的
    #if len(yearList) == 1:
    for Unit_ID in UnitList:
        for Equip_ID in EquipList:
            unitName = selectUnitNameByUnitID(Unit_ID)
            equipName = selectEquipNameByEquipID(Equip_ID)
            if equipYear == "":
                sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "' and equipYear ='" + equipYear + "'"
                #print(sql)
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    Info = list(resultInfo)
                    Info[7] = str(int(Info[4]) - int(Info[6]))
                    resultList.append(Info)
            else:
                sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                      "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList \
                      + "' and equipYear between '" +  startFactoryYear + "' and '" + endFactoryYear + "'"
                cur.execute(sql)
                result = cur.fetchall()
                #print("result*****************", result)
                if result:
                    info = list(result[0])
                    for resultInfo in result[1:]:
                        info[6] = str(int(info[6]) + int(resultInfo[6]))
                    info[7] = str(int(info[4]) - int(info[6]))
                    resultList.append(info)
                else:
                    info = []
                    info.append(Equip_ID, Unit_ID, equipName, unitName, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0')
                    resultList.append(info)

    disconnectMySql(conn, cur)
    # print(resultList)
    return resultList


# 查看某单位是否有子单位
def selectUnitIsHaveChild(Unit_ID):
    conn, cur = connectMySql()

    sql = "select * from unit where Unit_Uper = '" + Unit_ID + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    if result:
        return True
    else:
        return False


# 查看某装备是否有子装备
def selectEquipIsHaveChild(Equip_ID):
    conn, cur = connectMySql()

    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    if result:
        return True
    else:
        return False


# 返回装备是否是逐批录入
def selectEquipInputType(Equip_ID):
    conn, cur = connectMySql()

    sql = "select * from equip where Equip_ID = '" + Equip_ID + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    for resultInfo in result:
        if resultInfo[3] == '逐批录入':
            return True
        else:
            return False


# 查找某个单位的所有上级单位编号
def findUnitUperIDList(Unit_ID, UnitIDList):
    UnitIDList.append(Unit_ID)
    conn, cur = connectMySql()
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    uperIDTuple = cur.fetchall()
    for uperIDInfo in uperIDTuple:
        if uperIDInfo[0] != '':
            findUnitUperIDList(uperIDInfo[0], UnitIDList)
    disconnectMySql(conn, cur)


# 查找某个装备的所有上级单位编号
def findEquipUperIDList(Equip_ID, EquipIDList):
    EquipIDList.append(Equip_ID)
    conn, cur = connectMySql()
    sql = "select Equip_Uper from equip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    uperIDTuple = cur.fetchall()
    for uperIDInfo in uperIDTuple:
        if uperIDInfo[0] != '':
            findEquipUperIDList(uperIDInfo[0], EquipIDList)
    disconnectMySql(conn, cur)

# 通过单位号和装备号查找strength某条记录的实力数，现有数
def seletNumAboutStrength(Unit_ID, Equip_ID, year, equipYear):
    conn, cur = connectMySql()
    sql = "select * from strength where Equip_ID = '" + Equip_ID \
          + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "' and equipYear = '" + equipYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result


# 通过单位号和装备号查找strength某条记录的编制数
def seletNumAboutWork(Unit_ID, Equip_ID, year):
    conn, cur = connectMySql()
    sql = "select Work from weave where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result


def delWeaveYearByYear(year):
    conn, cur = connectMySql()
    sql = "delete from weaveyear where year = '" + year + "'"
    cur.execute(sql)

    allUnitInfo = selectAllDataAboutUnit()
    allEquipInfo = selectAllDataAboutEquip()
    for unitInfo in allUnitInfo:
        for equipInfo in allEquipInfo:
            allWork = selectWorkNumFromWeave(unitInfo[0], equipInfo[0], '')
            yearWork = selectWorkNumFromWeave(unitInfo[0], equipInfo[0], year)
            newWork = str(int(allWork) - int(yearWork))
            sql = "update weave set Work = '" + newWork + "' where Unit_ID = '" + unitInfo[0] +\
            "' and Equip_ID = '" + equipInfo[0] + "' and year = ''"
            cur.execute(sql)
    sql = "delete from weave where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

def delFactoryYear(year):
    conn, cur = connectMySql()
    sql = "delete from factoryyear where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)
# 删除某条录入信息
def delFromInputInfo(Unit_ID, Equip_ID, ID, num, year, inputYear):
    conn, cur = connectMySql()
    EquipIDList = []
    UnitIDList = []
    delNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            strengthAllYearInfo = seletNumAboutStrength(UnitID, EquipID, inputYear, "")
            if strengthAllYearInfo:
                nowAllNum = strengthAllYearInfo[0][6]
            else:
                nowAllNum = "0"
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                       "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                       + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                  " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                       inputYear + "', '" + "" + "')"
                cur.execute(sql)
            changeAllNowNum = int(nowAllNum) - delNum

            sql = "Update strength set Now = '" + str(changeAllNowNum) + "' where Equip_ID = '" + \
                   EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + inputYear + "' and equipYear = '" + "" + "'"
            cur.execute(sql)

            sql = "update weave set Now = '" + str(changeAllNowNum) + "' where Unit_ID = '" \
                   + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + inputYear + "'"
             # print(sql)
            cur.execute(sql)

            strengthYearInfo = seletNumAboutStrength(UnitID, EquipID, inputYear, year)
            if strengthYearInfo:
                nowYearNum = strengthYearInfo[0][6]
            else:
                nowYearNum = "0"
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                 " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      inputYear + "', '" + year + "')"
                cur.execute(sql)

            changeYearNowNum = int(nowYearNum) - delNum

            sql = "update strength set Now = '" + str(changeAllNowNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + inputYear + "' and equipYear = '" + year + "'"
            # print(sql)
            cur.execute(sql)


    sql = "delete from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" +\
          Equip_ID + "' and ID = '" + ID + "' and year = '" + year + "' and ID = '" + ID + "'"
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

def selectDataFromInputByYear(year):
    conn, cur = connectMySql()
    sql = "select * from inputinfo where year = '" + str(year) +"'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

# 修改批量录入某条数据的数量
def updateNumMutilInput(Unit_ID, Equip_ID, ID, num, orginNum, year, strengthYear):
    conn, cur = connectMySql()
    EquipIDList = []
    UnitIDList = []
    updateNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            strengthYearNum, nowYearNum = seletNumAboutStrength(UnitID, EquipID, strengthYear, year)
            changeYearNowNum = int(nowYearNum) - int(orginNum) + updateNum
            changeYearErrorNum = int(strengthYearNum) - changeYearNowNum
            strengthAllNum, nowAllNum = seletNumAboutStrength(UnitID, EquipID, strengthYear, '')
            changeAllNowNum = int(nowAllNum) - int(orginNum) + updateNum
            changeAllErrorNum = int(strengthAllNum) - changeAllNowNum
            sql = "Update strength set Now = '" + str(changeYearNowNum) + "', Error = '" + str(
                changeYearErrorNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear \
                  + "' and equipYear = '" + year + "'"

            cur.execute(sql)

            sql = "Update weave set Now = '" + str(changeAllNowNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear + "'"

            cur.execute(sql)
            sql = "update strength set Now = '" + str(changeAllNowNum) + "', Error = '" + str(
                changeAllErrorNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + strengthYear + "' and equipYear = ''"
            # print(sql)
            cur.execute(sql)

    sql = "update inputinfo set num = '" + num + "' where Unit_ID = '" + Unit_ID + \
          "' and Equip_ID = '" + Equip_ID + "' and ID = '" + ID + "' and year = '" + year + "'"
    cur.execute(sql)
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

# 判断是否有当前出厂年份
def isHaveFactoryYear(year):
    conn, cur = connectMySql()
    sql = "select * from factoryyear where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def addNewFactoryYear(year):
    conn, cur = connectMySql()
    result = selectAllDataAboutFactoryYear()
    sql = "insert into factoryyear(ID, year) values ('" + str(len(result) + 1) + "', '" + year + "')"
    print(sql)
    cur.execute(sql)

    equipList = selectAllDataAboutEquip()
    unitList = selectAllDataAboutUnit()
    strengthYearInfo = selectAllDataAboutStrengthYear()

    for equipInfo in equipList:
        for unitInfo in unitList:
            for strengthYear in strengthYearInfo:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                  + "('" + equipInfo[0] + "','" + unitInfo[0] + "','" + equipInfo[1] + "','" + unitInfo[1] + "', '0'," \
                                                                                                       " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                    strengthYear[1] + "', '" + year + "')"
                cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

# 往录入表inputinfo中插入一条数据
def addDataIntoInputInfo(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, strengthYear):
    print("====================", strengthYear, year)
    conn, cur = connectMySql()
    EquipIDList = []
    UnitIDList = []
    addNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)

    haveFactory = isHaveFactoryYear(year)
    if haveFactory:
        pass
    else:
        addNewFactoryYear(year)
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other, inputYear) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "', '" + num + "', '" + year + "', '" + shop + "', '" + state +\
          "', '" + arrive + "', '" + confirm + "', '" + other + "', '" + strengthYear +  "')"
    cur.execute(sql)
    # print(sql)
    # 执行sql语句，并发送给数据库

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            unitName = selectUnitNameByUnitID(UnitID)
            equipName = selectEquipNameByEquipID(EquipID)
            strengthAllYearInfo = seletNumAboutStrength(UnitID, EquipID, strengthYear, '')
            if strengthAllYearInfo:
                nowAllNum = strengthAllYearInfo[0][6]
            else:
                strengthAllNum, nowAllNum = "0", "0"
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                 " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      strengthYear + "', '" + "" + "')"
                cur.execute(sql)

            changeAllNowNum = int(nowAllNum) + addNum

            sql = "update strength set Now = '" + str(changeAllNowNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = '" + strengthYear + "' and equipYear = ''"
            cur.execute(sql)

            weaveInfo = selectWeaveInfo(UnitID, EquipID, strengthYear)
            if weaveInfo:
                pass
            else:
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, " \
                      "year) VALUES" \
                      + "('" + UnitID + "','" + EquipID + "','" + unitName + "','" + equipName + "','0', '0', '0', '')"
                cur.execute(sql)

            sql = "Update weave set Now = '" + str(changeAllNowNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear + "'"

            cur.execute(sql)

            strengthInfo = seletNumAboutStrength(UnitID, EquipID,strengthYear, year)
            if strengthInfo:
                nowYearNum = strengthInfo[0][6]
            else:
                nowYearNum = "0"
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                           " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      strengthYear + "', '" + year + "')"
                cur.execute(sql)

            changeYearNowNum = int(nowYearNum) + addNum
            sql = "Update strength set Now = '" + str(changeYearNowNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + strengthYear + "' and equipYear = '" + year + "'"

            cur.execute(sql)


    conn.commit()
    disconnectMySql(conn, cur)


# 根据单位号和装备号查询现有数和实力数
def selectNowNumAndStrengthNum(Unit_ID, Equip_ID, year, factoryYear):
    conn, cur = connectMySql()
    sql = "SELECT Now, Strength from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = '" + year + "' and equipYear = '" + factoryYear + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        return resultInfo[0], resultInfo[1]


# 修改当前编制数
def updateWeaveNum(Unit_ID, Equip_ID, weaveNum, orginWeave, year):
    #print("weavechange:", Unit_ID, Equip_ID, weaveNum, orginWeave, year)
    conn, cur = connectMySql()
    if selectIsPublicEquip(Unit_ID):
        Group_ID = selectEquipIDByPublicEquip(Unit_ID)
        UnitIDList = []
        UnitIDList.append(Unit_ID)
        EquipIDList = []
        findUnitUperIDList(Group_ID, UnitIDList)
        findEquipUperIDList(Equip_ID, EquipIDList)
        #print("unit and equip:", UnitIDList, EquipIDList)
        for UnitID in UnitIDList:
            for EquipID in EquipIDList:
                equipName = selectEquipNameByEquipID(EquipID)
                unitName = selectUnitNameByUnitID(UnitID)
                strengthInfo = seletNumAboutStrength(UnitID, EquipID, year, '')  # 获取原有的实力数以及现有数

                if strengthInfo:
                    orginYearWorkNum = strengthInfo[0][5]
                else:
                    orginYearWorkNum = "0"
                    if unitName == None:
                        unitName = "公用装备"
                    print("test==================", EquipID, UnitID, equipName, unitName, year)
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                          + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                     " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                          year + "', '" + "" + "')"
                    cur.execute(sql)

                changeYearWorkNum = int(orginYearWorkNum) - int(orginWeave) + int(weaveNum)
                sql = "Update strength set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                cur.execute(sql)

                sql = "Update weave set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                cur.execute(sql)
    else:
        EquipIDList = []
        UnitIDList = []
        findUnitUperIDList(Unit_ID, UnitIDList)
        findEquipUperIDList(Equip_ID, EquipIDList)
        print("unit and equip:", UnitIDList, EquipIDList)
        for UnitID in UnitIDList:
            for EquipID in EquipIDList:
                equipName = selectEquipNameByEquipID(EquipID)
                unitName = selectUnitNameByUnitID(UnitID)
                strengthInfo = seletNumAboutStrength(UnitID, EquipID, year, '')  # 获取原有的实力数以及现有数

                if strengthInfo:
                    orginYearWorkNum = strengthInfo[0][5]
                else:
                    orginYearWorkNum = "0"
                    sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                          "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                          + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                     " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                          year + "', '" + "" + "')"
                    cur.execute(sql)
                changeYearWorkNum = int(orginYearWorkNum) - int(orginWeave) + int(weaveNum)
                sql = "Update strength set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                cur.execute(sql)

                sql = "Update weave set Work = '" + str(changeYearWorkNum) + "' where Equip_ID = '" + \
                      EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
                cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

# 根据单位号，装备号修改某年的实力数，strengthNum为修改后的实力数，orginStrengthNum为原来的实力数
def updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, strengthNum, orginStrengthNum):
    conn, cur = connectMySql()

    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    factoryYearInfo = selectAllDataAboutFactoryYear()

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            strengthYearInfo = seletNumAboutStrength(UnitID, EquipID, year, '')
            if strengthYearInfo:
                orginYearStrengthNum  = strengthYearInfo[0][4]
            else:
                sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                      "NonStrength, Single, Arrive, year, equipYear) VALUES" \
                      + "('" + EquipID + "','" + UnitID + "','" + equipName + "','" + unitName + "', '0'," \
                                                                                                           " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + \
                      year + "', '" + "" + "')"
                cur.execute(sql)

            changeYearStrengthNum = int(orginYearStrengthNum) - int(orginStrengthNum) + int(strengthNum)
            sql = "Update strength set Strength = '" + str(changeYearStrengthNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
            cur.execute(sql)

            sql = "Update weave set Strength = '" + str(changeYearStrengthNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)


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


# 查找实力查询所有年份名字
def selectAllStrengthYear():
    yearList = []
    conn, cur = connectMySql()
    sql = "SELECT * from strengthyear ORDER BY year"
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    for yearInfo in yearListTuple:
        yearList.append(yearInfo[1])

    return yearList


# 查找实力查询所有年份信息
def selectAllStrengthYearInfo():
    yearList = []
    conn, cur = connectMySql()
    sql = "SELECT * from strengthyear order by year"
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    return yearListTuple

def selectAllFromPulicEquipByUnit(UnitInfoList):
    conn, cur = connectMySql()
    resultList = []
    for UnitInfo in UnitInfoList:
        sql = "select * from pubilcequip where Group_ID = '" + UnitInfo[0] + "'"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            resultList.append(result[0])
    disconnectMySql(conn, cur)
    return resultList

# 获取公用装备信息
def selectAllFromPulicEquip():
    conn, cur = connectMySql()
    sql = "select * from pubilcequip"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

def selectUnitInfoByUnitID(Unit_ID):
    conn, cur = connectMySql()
    sql = "select * from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for info in result:
        disconnectMySql(conn, cur)
        return info


def selectDisturbPlanUnitInfoByUnitID(Unit_ID):
    conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for info in result:
        disconnectMySql(conn, cur)
        return info

def findUperIDByUnitID(Unit_ID):
    conn, cur = connectMySql()
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    unitUper = None
    result = cur.fetchall()
    for info in result:
        unitUper = info[0]
        break
    disconnectMySql(conn, cur)
    return unitUper

# 查找编制表中某个装备以及某个单位的编制数
def selectWorkNumFromWeave(Unit_ID, Equip_ID, year):
    conn, cur = connectMySql()
    sql = "select Work from weave where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    if result:
        return result[0][0]
    else:
        return "0"


# 修改单位是否是旅团状态
def updateUnitIsGroupFromUnit(Unit_ID, Is_Group):
    conn, cur = connectMySql()
    if Is_Group == '否':
        uperUnitList = []
        findUnitUperIDList(Unit_ID, uperUnitList)
        equipInfoList = selectAllDataAboutEquip()
        publicEquipID = selectGroupIDByPublicEquip(Unit_ID)
        strengthYearList = selectAllDataAboutWeaveYear()
        sql = "update unit set Is_Group = '" + Is_Group + "' where Unit_ID = '" + Unit_ID + "'"
        cur.execute(sql)
        for uperUnitID in uperUnitList:
            for equipInfo in equipInfoList:
                orginAllWorkNum = selectWorkNumFromWeave(uperUnitID, equipInfo[0], "")
                delWorkAllNum = selectWorkNumFromWeave(publicEquipID, equipInfo[0], "")
                nowAllWorkNum = str(int(orginAllWorkNum) - int(delWorkAllNum))
                sql = "update weave set Work = '" + nowAllWorkNum + "' where Equip_ID = '" + equipInfo[0] + \
                      "' and Unit_ID = '" + uperUnitID + "' and year = ''"
                cur.execute(sql)

                for weaveYearInfo in strengthYearList:
                    orginYearWorkNum = selectWorkNumFromWeave(uperUnitID, equipInfo[0], weaveYearInfo[1])
                    delWorkYearNum = selectWorkNumFromWeave(publicEquipID, equipInfo[0], weaveYearInfo[1])
                    nowYearWorkNum = str(int(orginYearWorkNum) - int(delWorkYearNum))
                    sql = "update weave set Work = '" + nowYearWorkNum + "' where Equip_ID = '" + equipInfo[0] + \
                          "' and Unit_ID = '" + uperUnitID + "' and year = '" + weaveYearInfo[1] + "'"
                    cur.execute(sql)

        sql = "delete from pubilcequip where Group_ID = '" + Unit_ID + "'"
        # print(sql)
        cur.execute(sql)
        sql = "delete from weave where Unit_ID = '" + publicEquipID + "'"
        cur.execute(sql)
    else:
        result = selectAllFromPulicEquip()
        currentNum = len(result)
        sql = "update unit set Is_Group = '" + Is_Group + "' where Unit_ID = '" + Unit_ID + "'"
        cur.execute(sql)
        sql = "insert into pubilcequip (Equip_ID, Group_ID, work_Num) VALUES"\
              + "('"  + "gyzb" +  Unit_ID  + "', '" + Unit_ID + "', '0')"
        cur.execute(sql)
        # print(sql)
        equipInfoList = selectAllDataAboutEquip()
        weaveYearList = selectAllStrengthYearInfo()
        for equipInfo in equipInfoList:
            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + "gyzb" + Unit_ID + "','" + equipInfo[0] + "','公用装备','" + equipInfo[1] + "', '0', '0', '0', '" + \
                  "')"
            cur.execute(sql)
            for weaveYearInfo in weaveYearList:
                sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                      + "('" + "gyzb" + Unit_ID + "','" + equipInfo[0] + "','公用装备','" + equipInfo[
                          1] + "', '0', '0', '0', '" + weaveYearInfo[1] + "')"
                cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 查找某个旅团编号的公用装备编号
def selectGroupIDByPublicEquip(Group_ID):
    conn, cur = connectMySql()
    sql = "select Equip_ID from pubilcequip where Group_ID = '" + Group_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # print(result)
    if result:
        return result[0][0]
    else:
        return "0"

def selectPubilcEquipInfoByGroupID(Group_ID):
    conn, cur = connectMySql()
    sql = "select * from pubilcequip where Group_ID = '" + Group_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        return resultInfo

# 查找某个公用装备编号所属的旅团编号
def selectEquipIDByPublicEquip(Equip_ID):
    conn, cur = connectMySql()
    sql = "select Group_ID from pubilcequip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return "0"


# 修改录入信息表的某个信息
def updateInputInfo(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn, cur = connectMySql()
    sql = "update inputinfo set year = '" + year + "', shop = '" + shop + "', state = '" \
          + state + "', arrive = '" + arrive + "', confirm = '" + confirm + "', other = '" + other + \
          "' where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and ID = '" + ID + "'"
    print(sql)
    cur.execute(sql)
    conn.commit()
    return


# 获取某单位的所有子单位名称
def findUnitChildName(unitId):
    conn, cur = connectMySql()
    sql = "select Unit_Name from unit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    if result:
        return result
    else:
        return []


def findDisturbPlanUnitChildInfo(unitId):
    conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    #print("result",result)
    if result:
        return result
    else:
        return []



def findUnitChildInfo(unitId):
    conn, cur = connectMySql()
    sql = "select * from unit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    #print("result",result)
    if result:
        return result
    else:
        return []

#查询退休年份表
def selectAllRetirementYearInfo():
    conn, cur = connectMySql()
    sql = "select * from retireyear order by year"
    #print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result

def isHaveRecord(UnitID, EquipID, year):
    conn, cur = connectMySql()
    sql = "select * from retire where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    #print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


def selectEquipInfoByEquipID(EquipID):
    conn, cur = connectMySql()
    sql = "select * from equip where Equip_ID = '" + \
          EquipID + "'"
    #print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result

def findEquipInfo(equipId):
    conn, cur = connectMySql()
    sql = "select * from equip where Equip_ID = '" + equipId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    #print("result",result)
    if result:
        return result
    else:
        return []

# 查询编制信息
def selectWeaveInfo(UnitID, EquipID, year):
    conn, cur = connectMySql()
    sql = "select * from weave where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 插入退休表
def insertIntoRetire(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,Weave, Num, Now, Super, Apply, Other, year):
    #print(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,Weave, Num, Now, Super, Apply, Other, year)
    conn, cur = connectMySql()
    sql = "insert into retire (ID, Unit_ID, Equip_ID, Equip_Name, Equip_Unit, Weave, Num, Now, Super, Apply, Other, year) VALUES" \
          + "('" + ID + "', '" + Unit_ID + "', '" + EquipID + "', '" + Equip_Name + "', '" + Equip_Unit + "', '" + Weave + "', '"\
          + Num + "', '" + Now + "', '" + Super + "', '" + Apply + "', '" + Other + "','" + year + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()

# 查询退休信息
def selectInfoFromRetire(unitID, equipID, year):
    conn, cur = connectMySql()
    sql = "select * from retire where Equip_ID = '" + \
          equipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0]
    else:
        return ''


# 获取某装备的所有子装备ID
def findEquipChildID(equipId):
    conn, cur = connectMySql()
    sql = "select Unit_Name from equip where Equip_Uper = '" + equipId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    if result:
        return result
    else:
        return []

# 查询实力信息
def selectStrengthInfo(unitID, EquipID, year):
    conn, cur = connectMySql()
    sql = "select * from strength where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "' and equipYear = ''"
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 单位ID对应单位名
def findUnitNameFromID(UnitID):
    conn, cur = connectMySql()
    sql = "select Unit_Name from unit where Unit_ID = '" + UnitID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result


# 查询前更新退休表
def selectUpdateIntoRetire(unitID, EquipID, year):
    conn, cur = connectMySql()
    weaveInfo = selectWeaveInfo(unitID, EquipID, year)
    strengthInfo = selectStrengthInfo(unitID, EquipID, year)
    print("weaveInfo ============ ", weaveInfo, "strengthInfo ===========", strengthInfo)
    if weaveInfo:
        weave = weaveInfo[0][5]
    else:
        weave = '0'
    if strengthInfo:
        now = strengthInfo[0][6]
    else:
        now = '0'
    super = str(int(now) - int(weave))
    sql = "update retire set Weave = '" + weave + "', Now = '" + now + "', Super = '" + super + "' where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    print(sql)
    cur.execute(sql)
    conn.commit()


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
            equipName = equipInfo[0][1]
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
            else:
                now = '0'
            super = str(int(now) - int(weave))
            apply = ''
            other = ''
            print("'''''''''''''''''''", ID, unitID, EquipID, equipName, equipUnit, weave, num, now, super, other, year)
            haveChild = selectEquipIsHaveChild(EquipID)
            insertIntoRetire(ID, unitID, EquipID, equipName, equipUnit, weave, num, now, super, apply, other, year)
            currentResultInfo = [ID, unitID, EquipID, equipName, equipUnit, weave, num, now, super, apply, other, year]
            result.append(currentResultInfo)
    print(result)
    return result





# 查找某个装备的子目录
def selectChildEquip(Equip_ID):
    conn, cur = connectMySql()
    sql = "select * from equip where Equip_Uper = '" + \
          Equip_ID + "'"
    print(sql)
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
def updateRetireAboutRetire(num, apply, other, orginInfo):
    conn, cur = connectMySql()
    print("原来的数据：", orginInfo)
    if orginInfo:
        sql = "update retire set Num = '" + num + "', Apply = '" + apply + "', Other = '" + other +\
              "' where Equip_ID = '" + orginInfo[2] + "' and Unit_ID = '" + orginInfo[1] + "' and year = '" + orginInfo[11] + "'"
    else:
        return
    cur.execute(sql)
    conn.commit()


# 退役年份表中添加年份
def insertIntoRetireYear(year):
    conn, cur = connectMySql()

    result = selectAllRetirementYearInfo()
    sql = "insert into retireyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 删除某个退休年份
def delRetireYearByYear(year):
    conn, cur = connectMySql()

    sql = "delete from retireyear where year = '" + year + "'"
    # print(sql)
    cur.execute(sql)

    sql = "delete from retire where year = '" + year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)
# 删除退休表所有年份
def delRetireYearALLYear():
    conn, cur = connectMySql()
    sql = "truncate table retireyear "
    # print(sql)
    cur.execute(sql)
    sql = "truncate table retire "
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

def insertIntoWeaveYear(year):
    conn, cur = connectMySql()
    allEquipList = selectAllDataAboutEquip()
    allUnitList = selectAllDataAboutUnit()

    result = selectAllDataAboutWeaveYear()
    sql = "insert into weaveyear(ID, year) VALUES"\
    + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    cur.execute(sql)

    for equipInfo in allEquipList:
        for unitInfo in allUnitList:
            strengthInfo = selectStrengthInfo(equipInfo[0], unitInfo[0])
            if strengthInfo:
                strength = strengthInfo[0][4]
                now = strengthInfo[0][6]
            else:
                strength = "0"
                now = "0"
            work = '0'
            sql = "insert into weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "', '" + equipInfo[0] + "', '" + unitInfo[1] + "', '" + equipInfo[1] + "', '"\
                  + strength + "', '" + work + "', '" + now + "','" + str(year) + "')"
            print(sql)
            cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 设置单位别名
def updateUnitAlias(Unit_Alias,Unit_ID):
    conn, cur = connectMySql()
    sql = "update unit set Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    sql = "update disturbplanunit set Unit_Alias = '" + Unit_Alias + "' where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)


# 设置装备数量单位
def updateEquipUnit(unit, Equip_ID):
    conn, cur = connectMySql()

    sql = "update equip set unit = '" \
          + unit + "' where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)

    sql = "update retire set Equip_Unit = '" \
          + unit + "' where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)



def delStrengthYearByYear(year):
    conn, cur = connectMySql()

    sql = "delete from weave where year = '" + year + "'"
    print(sql)
    cur.execute(sql)

    sql = "delete from strength where year = '" + year + "'"
    cur.execute(sql)

    sql = "delete from inputinfo where inputYear = '" + year + "'"
    cur.execute(sql)

    sql = "delete from strengthyear where year = '" + year + "'"
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#根据装备ID查找某个装备的单位
def findEquipUnitByEquipID(EquipID):
    conn, cur = connectMySql()
    sql = "select unit from equip where Equip_ID ='" + EquipID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

def findUperEquipIDByName(Equip_Name):
    conn, cur = connectMySql()
    sql = "select * from equip where Equip_Name ='" + Equip_Name + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

def selectUnitIfUppermost(Unit_Id):
    conn, cur = connectMySql()
    sql = "select Unit_Uper from unit where Unit_ID = '" + Unit_Id + "'"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    if result[0][0]== '':
        return True
    else:
        return False

def findUperInfoList(EquipID, UperList):
    if EquipID == "":
        return
    else:
        conn, cur = connectMySql()
        sql = "select Equip_Uper from equip where Equip_ID = '" + EquipID + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            UperList.append(resultInfo)
            if resultInfo:
                findUperInfoList(resultInfo[0], UperList)
        disconnectMySql(conn, cur)

def selectUperInfoByEquipID(EquipID):
    UperList = []
    findUperInfoList(EquipID, UperList)
    return UperList

if __name__ == '__main__':
    print(len(findUnitNameFromID('10')))
    pass
