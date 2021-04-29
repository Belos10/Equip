import pymysql
from database.connectAndDisSql  import connectMySql, disconnectMySql

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

# 增加装备目录
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
    #print("''''''''''")
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

    #测试结果
    #print(result)

    return result

#返回unit单位表的所有数据
def selectAllDataAboutUnit():
    conn, cur = connectMySql()

    sql = "select * from unit"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#根据Equip_Uper查询单位信息,并返回
def selectEquipInfoByEquipUper(Equip_Uper):
    conn, cur = connectMySql()

    sql = "select * from equip where Equip_Uper = '" + Equip_Uper + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    #测试结果
    #print(result)

    return result

#返回equip装备表的所有数据
def selectAllDataAboutEquip():
    conn, cur = connectMySql()

    sql = "select * from equip"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#查找所有的编制年份
def selectAllDataAboutWeaveYear():
    conn, cur = connectMySql()

    sql = "select * from weaveyear"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#往单位表unit中插入一条数据
def addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper, Is_Group) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "', Is_Group = '否')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    equipInfoTuple = selectAllDataAboutEquip()
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    weaveYearInfoTuple = selectAllDataAboutWeaveYear()

    for equipInfo in equipInfoTuple:
        sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
              "NonStrength, Single, Arrive, year) VALUES" \
              + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
            " '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '')"
        cur.execute(sql)

        sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, " \
              "year) VALUES" \
              + "('" + Unit_ID + "','" + equipInfo[0] + "','" + Unit_Name + "','" + equipInfo[1] + "','0', '0', '0', '')"
        cur.execute(sql)

        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year) VALUES" \
                  + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
                " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + strengthYearInfo[1] + "')"
            cur.execute(sql)

        for weaveYearInfo in weaveYearInfoTuple:
            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + Unit_ID + "','" + equipInfo[0] + "','" + Unit_Name + "','" + equipInfo[1] + "', '0', '0', '0', '" + weaveYearInfo[1] + "')"

            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#往装备表equip中插入一条数据
def addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "INSERT INTO equip (Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type) VALUES" \
          + "('" + Equip_ID + "','" + Equip_Name + "','" + Equip_Uper + "','" + Input_Type + "','" + Equip_Type + "')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    strengthYearInfoTuple = selectAllDataAboutStrengthYear()
    unitInfoTuple = selectAllDataAboutUnit()
    weaveYearInfoTuple = selectAllDataAboutWeaveYear()

    #print(unitInfoTuple)
    for unitInfo in unitInfoTuple:
        sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
              "NonStrength, Single, Arrive, year) VALUES" \
              + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
            " '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '')"
        #print(sql)
        cur.execute(sql)

        sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, " \
              "year) VALUES" \
              + "('" + unitInfo[0] + "','" + Equip_ID + "','" + unitInfo[1] + "','" + Equip_Name + "', '0', '0', '0', '')"
        #print(sql)
        cur.execute(sql)

        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year) VALUES" \
                  + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
                " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'" + ",'" + strengthYearInfo[1] + "')"
            cur.execute(sql)

        for weaveYearInfo in weaveYearInfoTuple:
            sql = "INSERT INTO weave (Unit_ID, Equip_ID, Unit_Name, Equip_Name, Strength, Work, Now, year) VALUES" \
                  + "('" + unitInfo[0] + "','" + Equip_ID + "','" + unitInfo[1] + "','" + Equip_Name + "', '0', '0', '0', '" + \
                  weaveYearInfo[1] + "')"
            #print(sql)
            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#单位表unit中修改一条数据
def updateDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "Update unit set Unit_Name = '" + Unit_Name + "', Unit_Uper = '" + Unit_Uper + "' where Unit_ID = '" + Unit_ID + "'"
    #print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    sql = "Update strength set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    #print(sql)
    cur.execute(sql)

    sql = "Update weave set Unit_Name = '" + Unit_Name + "' where Unit_ID = '" + Unit_ID + "'"
    # print(sql)
    cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#单位表equip中修改一条数据
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

    conn.commit()
    disconnectMySql(conn, cur)

#找到某个旅团的公用装备信息
def findChildUnitForPublic(Unit_ID):
    conn, cur = connectMySql()
    sql = "select * from pubilcequip where Group_ID = '" + Unit_ID  + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

#单位表unit中删除一条数据
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
        sql = "Delete from pubilcequip where Equip_ID = '" + publicInfo[0][0] + "'"
        # print(sql)
        cur.execute(sql)
        sql = "Delete from weave where Unit_ID = '" + UnitID + "'"
        # print(sql)
        cur.execute(sql)
        sql = "Delete from weave where Unit_ID = '" + publicInfo + "'"
        # print(sql)
        cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#装备表equip中删除一条数据
def delDataInEquip(Equip_ID):
    conn, cur = connectMySql()
    # 插入的sql语句
    EquipIDList = []
    findChildEquip(Equip_ID, EquipIDList, cur)

    for EquipID in EquipIDList:
        sql = "Delete from equip where Equip_ID = '" + EquipID + "'"
        #print(sql)
        # 执行sql语句，并发送给数据库
        cur.execute(sql)

        sql = "Delete from inputinfo where Equip_ID = '" + EquipID + "'"
        #print(sql)
        cur.execute(sql)

        sql = "Delete from strength where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)
        #print(sql)

        sql = "Delete from weave where Equip_ID = '" + EquipID + "'"
        # print(sql)
        cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#返回strengthyear表中所有信息
def selectAllDataAboutStrengthYear():
    conn, cur = connectMySql()

    sql = "select * from strengthyear"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    # 测试结果
    # print(result)

    return result

#按照单位编号，装备编号以及出厂年份查找录入信息
def selectInfoAboutInput(Unit_ID, Equip_ID):
    conn, cur = connectMySql()

    resultList = []
    sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        resultList.append(resultInfo)

    disconnectMySql(conn, cur)
    return resultList

#判断当前是否为公用装备
def selectIsPublicEquip(Unit_ID):
    conn, cur = connectMySql()

    sql = "select * from pubilcequip where Equip_ID = '" + Unit_ID + "'"
    #print(sql)
    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    if result:
        return True
    else:
        return False

#按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutWeaveByEquipShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    if yearList == '全部':
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                #查询当前装备ID的孩子序列
                EquipIDChildList = []
                findChildEquip(Equip_ID, EquipIDChildList, cur)
                for childEquipID in EquipIDChildList:
                    sql = "select * from weave where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + childEquipID + "' and year = ''"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    # 如果查询某一年的
    else:
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

#按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByEquipShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    if yearList == '全部':
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                #查询当前装备ID的孩子序列
                EquipIDChildList = []
                findChildEquip(Equip_ID, EquipIDChildList, cur)
                for childEquipID in EquipIDChildList:
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + childEquipID + "' and year = ''"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    # 如果查询某一年的
    else:
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                # 查询当前装备ID的孩子序列
                EquipIDChildList = []
                findChildEquip(Equip_ID, EquipIDChildList, cur)
                for childEquipID in EquipIDChildList:
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                        "' and Equip_ID = '" + childEquipID + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    '''
    # 如果查询多年的
    else:
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                EquipIDChildList = []
                findChildEquip(Equip_ID, EquipIDChildList, cur)
                for childEquipID in EquipIDChildList:
                    for year in yearList:
                        sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + childEquipID + "', and year = '" + year + "'"
                        cur.execute(sql)
                        result = cur.fetchall()
                        tempList.append(result)

                    for tempInfo in tempList:
                        temp[0] = tempInfo[0]
                        temp[1] = tempInfo[1]
                        temp[2] = tempInfo[2]
                        temp[3] = tempInfo[3]
                        temp[4] = str(int(temp[4]) + int(tempInfo[4]))
                        temp[5] = str(int(temp[5]) + int(tempInfo[5]))
                        temp[6] = str(int(temp[6]) + int(tempInfo[6]))
                        temp[7] = str(int(temp[7]) + int(tempInfo[7]))
                        temp[8] = str(int(temp[8]) + int(tempInfo[8]))
                        temp[9] = str(int(temp[9]) + int(tempInfo[9]))
                        temp[10] = str(int(temp[10]) + int(tempInfo[10]))
                        temp[11] = str(int(temp[11]) + int(tempInfo[11]))
                        temp[12] = str(int(temp[12]) + int(tempInfo[12]))
                        temp[13] = str(int(temp[13]) + int(tempInfo[13]))
                        temp[14] = str(int(temp[14]) + int(tempInfo[14]))

                    resultList.append(temp)
    '''
    disconnectMySql(conn, cur)
    return resultList

#判断当前单位是否是旅团
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

#按单位展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    #if len(yearList) == 1:
        # 如果查询全部年的

    if yearList == '全部':
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
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
                #查询当前单位ID的孩子序列
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

#按单位展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    #if len(yearList) == 1:
        # 如果查询全部年的
    if yearList == '全部':
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
                UnitIDChildList = []
                findChildUnit(Unit_ID, UnitIDChildList, cur)
                for childUnitID in UnitIDChildList:
                    sql = "select * from strength where Unit_ID = '" + childUnitID + "' and Equip_ID = '" + Equip_ID + "' and year = ''"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    # 如果查询某一年的
    else:
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                #查询当前单位ID的孩子序列
                UnitIDChildList = []
                findChildUnit(Unit_ID, UnitIDChildList, cur)
                for childUnitID in UnitIDChildList:
                    sql = "select * from strength where Unit_ID = '" + childUnitID + \
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
    '''
    # 如果查询多年的
    else:
        for Equip_ID in EquipList:
            for Unit_ID in UnitList:
                # 查询当前单位ID的孩子序列
                UnitIDChildList = []
                findChildUnit(Unit_ID, UnitIDChildList, cur)
                for childUnitID in UnitIDChildList:
                    for year in yearList:
                        sql = "select * from strength where Unit_ID = '" + childUnitID + "' and Equip_ID = '" + Equip_ID + "', and year = '" + year + "'"
                        cur.execute(sql)
                        result = cur.fetchall()
                        tempList.append(result)

                    for tempInfo in tempList:
                        temp[0] = tempInfo[0]
                        temp[1] = tempInfo[1]
                        temp[2] = tempInfo[2]
                        temp[3] = tempInfo[3]
                        temp[4] = str(int(temp[4]) + int(tempInfo[4]))
                        temp[5] = str(int(temp[5]) + int(tempInfo[5]))
                        temp[6] = str(int(temp[6]) + int(tempInfo[6]))
                        temp[7] = str(int(temp[7]) + int(tempInfo[7]))
                        temp[8] = str(int(temp[8]) + int(tempInfo[8]))
                        temp[9] = str(int(temp[9]) + int(tempInfo[9]))
                        temp[10] = str(int(temp[10]) + int(tempInfo[10]))
                        temp[11] = str(int(temp[11]) + int(tempInfo[11]))
                        temp[12] = str(int(temp[12]) + int(tempInfo[12]))
                        temp[13] = str(int(temp[13]) + int(tempInfo[13]))
                        temp[14] = str(int(temp[14]) + int(tempInfo[14]))

                    resultList.append(temp)
    '''
    disconnectMySql(conn, cur)
    return resultList

    # 测试结果
    # print(result)

    return result

#没有展开时根据单位列表、装备列表以及年份查询编制表
def selectAboutWeaveByUnitListAndEquipList(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    # print(UnitList, EquipList)
    temp = ['Unit_ID', 'Equip_ID', 'Unit_Name', 'Equip_Name', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    # if len(yearList) == 1:
    # 如果查询全部年的
    if yearList == '全部':
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                sql = "select * from weave where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = ''"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    resultList.append(resultInfo)
        # 如果查询某一年的
    else:
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                sql = "select * from weave where Unit_ID = '" + Unit_ID + \
                      "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    resultList.append(resultInfo)
    disconnectMySql(conn, cur)
    return resultList

#没有展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    #print(UnitList, EquipList)
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    #如果只查询某年的
    #if len(yearList) == 1:
        #如果查询全部年的
    if yearList == '全部':
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "' and year = ''"
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    resultList.append(resultInfo)
        #如果查询某一年的
    else:
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                sql = "select * from strength where Unit_ID = '" + Unit_ID + \
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList + "'"
                #print(sql)
                cur.execute(sql)
                result = cur.fetchall()
                for resultInfo in result:
                    resultList.append(resultInfo)
    '''
    #如果查询多年的
    else:
        for Unit_ID in UnitList:
            for Equip_ID in EquipList:
                for year in yearList:
                    sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "', and year = '" + year + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    tempList.append(result)

                for tempInfo in tempList:
                    temp[0] = tempInfo[0]
                    temp[1] = tempInfo[1]
                    temp[2] = tempInfo[2]
                    temp[3] = tempInfo[3]
                    temp[4] = str(int(temp[4]) + int(tempInfo[4]))
                    temp[5] = str(int(temp[5]) + int(tempInfo[5]))
                    temp[6] = str(int(temp[6]) + int(tempInfo[6]))
                    temp[7] = str(int(temp[7]) + int(tempInfo[7]))
                    temp[8] = str(int(temp[8]) + int(tempInfo[8]))
                    temp[9] = str(int(temp[9]) + int(tempInfo[9]))
                    temp[10] = str(int(temp[10]) + int(tempInfo[10]))
                    temp[11] = str(int(temp[11]) + int(tempInfo[11]))
                    temp[12] = str(int(temp[12]) + int(tempInfo[12]))
                    temp[13] = str(int(temp[13]) + int(tempInfo[13]))
                    temp[14] = str(int(temp[14]) + int(tempInfo[14]))

                resultList.append(temp)
    '''
    disconnectMySql(conn, cur)
    #print(resultList)
    return resultList


#查看某单位是否有子单位
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

#查看某装备是否有子装备
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

#返回装备是否是逐批录入
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

#查找某个单位的所有上级单位编号
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

#查找某个装备的所有上级单位编号
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

#通过单位号和装备号查找strength某条记录的实力数，现有数
def seletNumAboutStrength(Unit_ID, Equip_ID, year):
    conn, cur = connectMySql()
    sql = "select Strength, Now from strength where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    nowNumTuple = cur.fetchall()
    disconnectMySql(conn, cur)

    for nowNumInfo in nowNumTuple:
        return nowNumInfo[0], nowNumInfo[1]

#往录入表inputinfo中插入一条数据
def addDataIntoInputInfo(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn, cur = connectMySql()
    EquipIDList = []
    UnitIDList = []
    addNum = int(num)
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "', '" + num + "', '" + year + "', '" + shop + "', '" + state +\
          "', '" + arrive + "', '" + confirm + "', '" + other + "')"
    cur.execute(sql)
    # print(sql)
    # 执行sql语句，并发送给数据库

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            strengthYearNum, nowYearNum = seletNumAboutStrength(UnitID, EquipID, year)
            changeYearNowNum = int(nowYearNum) + addNum
            changeYearErrorNum = int(strengthYearNum) - changeYearNowNum
            strengthAllNum, nowAllNum = seletNumAboutStrength(UnitID, EquipID, '')
            changeAllNowNum = int(nowAllNum) + addNum
            changeAllErrorNum = int(strengthAllNum) - changeAllNowNum
            sql = "Update strength set Now = '" + str(changeYearNowNum) + "', Error = '" + str(changeYearErrorNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)

            sql = "Update weave set Now = '" + str(changeYearNowNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)
            sql = "update strength set Now = '"  + str(changeAllNowNum) + "', Error = '" + str(changeAllErrorNum) +  "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = ''"
            #print(sql)
            cur.execute(sql)

            sql = "update weave set Now = '" + str(changeAllNowNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = ''"
            #print(sql)
            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#根据单位号和装备号查询现有数和实力数
def selectNowNumAndStrengthNum(Unit_ID, Equip_ID):
    conn, cur = connectMySql()
    sql = "SELECT Now, Strength from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for resultInfo in result:
        return resultInfo[0], resultInfo[1]

#根据单位号，装备号修改某年的实力数，strengthNum为修改后的实力数，orginStrengthNum为原来的实力数
def updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, strengthNum, orginStrengthNum):
    conn, cur = connectMySql()

    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_ID, UnitIDList)
    findEquipUperIDList(Equip_ID, EquipIDList)

    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            orginYearStrengthNum,  YearNowNum= seletNumAboutStrength(UnitID, EquipID, year) #获取原有的实力数以及现有数
            changeYearStrengthNum = int(orginYearStrengthNum) - int(orginStrengthNum) + int(strengthNum)
            changeYearErrorNum = int(changeYearStrengthNum) - int(YearNowNum)
            orginAllStrengthNum, nowAllNum = seletNumAboutStrength(UnitID, EquipID, '')
            changeAllStrengthNum = int(orginAllStrengthNum) - int(orginStrengthNum) + int(strengthNum)
            changeAllErrorNum = int(changeAllStrengthNum) - int(nowAllNum)
            sql = "Update strength set Strength = '" + str(changeYearStrengthNum) + "', Error = '" + str(
                changeYearErrorNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)

            sql = "Update weave set Strength = '" + str(changeYearStrengthNum) + "', Error = '" + str(
                changeYearErrorNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)
            sql = "update strength set Strength = '" + str(changeAllStrengthNum) + "', Error = '" + str(
                changeAllErrorNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = ''"
            cur.execute(sql)
            sql = "update weave set Strength = '" + str(changeAllStrengthNum) + "', Error = '" + str(
                changeAllErrorNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = ''"
            cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#查找所有末级装备
def selectAllEndEquip():
    resultList = []
    allEquipTuple = selectAllDataAboutEquip()
    for equipInfo in allEquipTuple:
        if selectEquipIsHaveChild(equipInfo[0]):
            pass
        else:
            resultList.append(equipInfo)
    return resultList

#查找实力查询所有年份名字
def selectAllStrengthYear():
    yearList = []
    conn, cur = connectMySql()
    sql = "SELECT * from strengthyear "
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    for yearInfo in yearListTuple:
        yearList.append(yearInfo[1])

    return yearList

#查找实力查询所有年份信息
def selectAllStrengthYearInfo():
    yearList = []
    conn, cur = connectMySql()
    sql = "SELECT * from strengthyear "
    cur.execute(sql)
    yearListTuple = cur.fetchall()
    return yearListTuple

#获取公用装备信息
def selectAllFromPulicEquip():
    conn, cur = connectMySql()
    sql = "select * from pubilcequip"
    cur.execute(sql)
    result = cur.fetchall()
    disconnectMySql(conn, cur)
    return result

#查找编制表中某个装备以及某个单位的编制数
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

#修改单位是否是旅团状态
def updateUnitIsGroupFromUnit(Unit_ID, Is_Group):
    conn, cur = connectMySql()
    if Is_Group == '否':
        uperUnitList = []
        findUnitUperIDList(Unit_ID, uperUnitList)
        equipInfoList = selectAllDataAboutEquip()
        publicEquipID = selectGroupIDByPublicEquip(Unit_ID)
        weaveYearList = selectAllDataAboutWeaveYear()
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

                for weaveYearInfo in weaveYearList:
                    orginYearWorkNum = selectWorkNumFromWeave(uperUnitID, equipInfo[0], weaveYearInfo[1])
                    delWorkYearNum = selectWorkNumFromWeave(publicEquipID, equipInfo[0], weaveYearInfo[1])
                    nowYearWorkNum = str(int(orginYearWorkNum) - int(delWorkYearNum))
                    sql = "update weave set Work = '" + nowYearWorkNum + "' where Equip_ID = '" + equipInfo[0] + \
                          "' and Unit_ID = '" + uperUnitID + "' and year = '" + weaveYearInfo[1] + "'"
                    cur.execute(sql)

        sql = "delete from pubilcequip where Group_ID = '" + Unit_ID + "'"
        #print(sql)
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
        #print(sql)
        equipInfoList = selectAllDataAboutEquip()
        weaveYearList = selectAllDataAboutWeaveYear()
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

#查找某个旅团编号的公用装备编号
def selectGroupIDByPublicEquip(Group_ID):
    conn, cur = connectMySql()
    sql = "select Equip_ID from pubilcequip where Group_ID = '" + Group_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #print(result)
    if result:
        return result[0][0]
    else:
        return "0"

#查找某个公用装备编号所属的旅团编号
def selectEquipIDByPublicEquip(Equip_ID):
    conn, cur = connectMySql()
    sql = "select Group_ID from pubilcequip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return "0"

if __name__ == '__main__':
    pass
