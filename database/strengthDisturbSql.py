import pymysql
from database.connectAndDisSql  import connectMySql, disconnectMySql


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
        按照单位展开查找实力表
'''
def select_Equip_And_Unit_ByUnit(UnitID, EquipID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    unitHaveNoChild = UnitNotHaveChild(UnitID)
    equipHaveNoChild = EquipNotHaveChild(EquipID)

    # 如果单位和装备都没有下级
    if unitHaveNoChild and equipHaveNoChild:
        sql = "select * from strength where Unit_ID = '" + UnitID + "' and Equip_ID = '" + EquipID + "'"
        cur.execute(sql)
        # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
        data = cur.fetchall()
        if data:
            pass
        else:
            # 如果没有记录，则显示结果都为0
            result = []
            final_result = []
            addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            result.append(EquipID)
            result.append(UnitID)
            result.append(equipName)
            result.append(unitName)
            for value in addResult:
                result.append(value)
            final_result.append(result)
            cur.close()
            conn.close()
            return final_result
        return data
    result = []
    final_result = []
    addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    UnitList = []
    childEquipList = []
    findUnitList(UnitID, UnitList, cur)
    findChildEquip(EquipID, childEquipList, cur)
    equipName = selectEquipNameByEquipID(EquipID)
    # 对于每一个单位统计他们在该装备下有多少
    for childUnit in UnitList:
        result = []
        addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

        result.append(EquipID)
        result.append(childUnit[0])
        result.append(equipName)
        unitName = selectUnitNameByUnitID(childUnit[0])
        result.append(unitName)

        for equip_ID in childEquipList:
            for each_ID in childUnit:
                sql = "select * from strength where Unit_ID = '" + each_ID + "' and Equip_ID = '" + equip_ID + "'"
                cur.execute(sql)
                # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
                data = cur.fetchall()
                for item in data:
                    addList = item[4:]
                    for i, value in enumerate(addList):
                        add = int(addResult[i]) + int(addList[i])
                        addResult[i] = str(add)
        for value in addResult:
            result.append(value)
        final_result.append(result)
    #print(final_result)
    cur.close()
    conn.close()
    return final_result


'''
    功能：
        按照装备展开查找实力表
'''


def select_Equip_And_Unit_ByEquip(UnitID, EquipID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    unitHaveNoChild = UnitNotHaveChild(UnitID)
    equipHaveNoChild = EquipNotHaveChild(EquipID)

    # 如果单位和装备都没有下级
    if unitHaveNoChild and equipHaveNoChild:
        sql = "select * from strength where Unit_ID = '" + UnitID + "' and Equip_ID = '" + EquipID + "'"
        cur.execute(sql)
        # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
        data = cur.fetchall()
        if data:
            pass
        else:
            # 如果没有记录，则显示结果都为0
            result = []
            final_result = []
            addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            equipName = selectEquipNameByEquipID(EquipID)
            unitName = selectUnitNameByUnitID(UnitID)
            result.append(EquipID)
            result.append(UnitID)
            result.append(equipName)
            result.append(unitName)
            for value in addResult:
                result.append(value)
            final_result.append(result)
            cur.close()
            conn.close()
            return final_result
        return data
    result = []
    final_result = []
    addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    childUnitList = []
    EquipList = []
    findChildUnit(UnitID, childUnitList, cur)
    # print(childUnitList)
    findEquipList(EquipID, EquipList, cur)
    unitName = selectUnitNameByUnitID(UnitID)
    # print(EquipList)
    # 对于每一个装备统计他们在该单位下有多少
    for childEquip in EquipList:
        result = []
        addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

        result.append(childEquip[0])
        result.append(UnitID)
        equipName = selectEquipNameByEquipID(childEquip[0])
        result.append(equipName)
        result.append(unitName)

        for unit_ID in childUnitList:
            for each_ID in childEquip:
                sql = "select * from strength where Unit_ID = '" + unit_ID + "' and Equip_ID = '" + each_ID + "'"
                cur.execute(sql)
                # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
                data = cur.fetchall()
                for item in data:
                    addList = item[4:]
                    for i, value in enumerate(addList):
                        add = int(addResult[i]) + int(addList[i])
                        addResult[i] = str(add)
        for value in addResult:
            result.append(value)
        final_result.append(result)

    cur.close()
    conn.close()
    return final_result


'''
    功能：
        通过左边目录进行实力查询,没有展开
'''


def select_Equip_And_Unit(Unit_ID, Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    unitHaveNoChild = UnitNotHaveChild(Unit_ID)
    equipHaveNoChild = EquipNotHaveChild(Equip_ID)
    if unitHaveNoChild and equipHaveNoChild:
        sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
        cur.execute(sql)
        # print(sql)
        # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
        data = cur.fetchall()
        if data:
            pass
        else:
            result = []
            final_result = []
            addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            equipName = selectEquipNameByEquipID(Equip_ID)
            unitName = selectUnitNameByUnitID(Unit_ID)
            result.append(Equip_ID)
            result.append(Unit_ID)
            result.append(equipName)
            result.append(unitName)
            for value in addResult:
                result.append(value)
            final_result.append(result)
            cur.close()
            conn.close()
            return final_result
        return data
    result = []
    final_result = []
    addResult = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    childUnitList = []
    childEquipList = []
    findChildUnit(Unit_ID, childUnitList, cur)
    findChildEquip(Equip_ID, childEquipList, cur)
    equipName = selectEquipNameByEquipID(Equip_ID)
    unitName = selectUnitNameByUnitID(Unit_ID)
    result.append(Equip_ID)
    result.append(Unit_ID)
    result.append(equipName)
    result.append(unitName)
    # print(childUnitList, childEquipList)
    for unitID in childUnitList:
        for equipID in childEquipList:
            sql = "select * from strength where Unit_ID = '" + unitID + "' and Equip_ID = '" + equipID + "'"
            # print(sql)
            cur.execute(sql)
            # print(sql)
            # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
            data = cur.fetchall()
            # print(data)
            for item in data:
                # print(item)
                addList = item[4:]
                for i, value in enumerate(addList):
                    add = int(addResult[i]) + int(addList[i])
                    addResult[i] = str(add)
            # 打印测试
            # print(data)
    for value in addResult:
        result.append(value)
    final_result.append(result)
    cur.close()
    conn.close()
    return final_result


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
        通过装备号和单位号查找录入信息
'''


def select_Add_Info(Unit_ID, Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select * from inputinfo where Unit_ID = '" + Unit_ID + \
          "' and Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def insert_Strength(Unit_ID, Equip_ID, addNum):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    changeNum = 0
    # 插入的sql语句
    sql = "select * from strength where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for num in result:
        changeNum = int(num[4]) + int(addNum)
    sql = "Update strength set Strengh = '" + changeNum + "' where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def insert_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "','" + num + "','" + year + "','" + shop + "','" + state \
          + "','" + arrive + "','" + confirm + "','" + other + "')"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def add_UnitDict(Unit_ID, Unit_Name, Unit_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def delete_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "delete from inputinfo where (Unit_ID=  '" + (Unit_ID or None) + "' AND Equip_ID='" + (Equip_ID or None) \
          + "' AND ID='" + (ID or None) + "' AND num='" + (num or None) + "')"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def delete_Inquiry_Clicked(Unit_ID, Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "delete from strength where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    cur.execute(sql)
    sql = "delete from inputinfo where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()




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


def del_Unit_Dict(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from unit where Unit_ID = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def del_Unit_And_Child(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from unit where Unit_ID = '" + Unit_ID + "'" + "and Unit_Uper = '" + Unit_ID + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


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
    print("''''''''''")
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

'''
    实力分布所涉及的表的sql
'''

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

#往单位表unit中插入一条数据
def addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper):
    conn, cur = connectMySql()
    # 插入的sql语句
    sql = "INSERT INTO unit (Unit_ID, Unit_Name, Unit_Uper) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)

    equipInfoTuple = selectAllDataAboutEquip()
    strengthYearInfoTuple = selectAllDataAboutStrengthYear()

    for equipInfo in equipInfoTuple:
        sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
              "NonStrength, Single, Arrive, year) VALUES" \
              + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
            " '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '')"
        cur.execute(sql)

        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year) VALUES" \
                  + "('" + equipInfo[0] + "','" + Unit_ID + "','" + equipInfo[1] + "','" + Unit_Name + "', '0'," \
                " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'," + "'" + strengthYearInfo[1] + "')"
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

    print(unitInfoTuple)
    for unitInfo in unitInfoTuple:
        sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
              "NonStrength, Single, Arrive, year) VALUES" \
              + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
            " '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '')"
        #print(sql)
        cur.execute(sql)

        for strengthYearInfo in strengthYearInfoTuple:
            sql = "INSERT INTO strength (Equip_ID, Unit_ID, Equip_Name, Unit_Name, Strength, Work, Now, Error, Retire, Delay, Pre, NonObject," \
                  "NonStrength, Single, Arrive, year) VALUES" \
                  + "('" + Equip_ID + "','" + unitInfo[0] + "','" + Equip_Name + "','" + unitInfo[1] + "', '0'," \
                " '0', '0', '0','0', '0', '0', '0', '0', '0', '0'" + ",'" + strengthYearInfo[1] + "')"
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

    conn.commit()
    disconnectMySql(conn, cur)

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
        print(sql)

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

#按装备展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByEquipShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    if len(yearList) == 1:
        # 如果查询全部年的
        if yearList[0] == '全部':
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
                            "' and Equip_ID = '" + childEquipID + "' and year = '" + yearList[0] + "'"
                        cur.execute(sql)
                        result = cur.fetchall()
                        for resultInfo in result:
                            resultList.append(resultInfo)
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

    disconnectMySql(conn, cur)
    return resultList

    # 测试结果
    # print(result)

    return result

#按单位展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitShow(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    # 如果只查询某年的
    if len(yearList) == 1:
        # 如果查询全部年的
        if yearList[0] == '全部':
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
                            "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList[0] + "'"
                        cur.execute(sql)
                        result = cur.fetchall()
                        for resultInfo in result:
                            resultList.append(resultInfo)
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

    disconnectMySql(conn, cur)
    return resultList

    # 测试结果
    # print(result)

    return result

#没有展开时根据单位列表、装备列表以及年份查询实力表
def selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, yearList):
    conn, cur = connectMySql()
    #print(UnitList, EquipList)
    temp = ['Equip_ID', 'Unit_ID', 'Equip_Name', 'Unit_Name', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0']
    tempList = []
    resultList = []
    #如果只查询某年的
    if len(yearList) == 1:
        #如果查询全部年的
        if yearList[0] == '全部':
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
                          "' and Equip_ID = '" + Equip_ID + "' and year = '" + yearList[0] + "'"
                    cur.execute(sql)
                    result = cur.fetchall()
                    for resultInfo in result:
                        resultList.append(resultInfo)
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

    disconnectMySql(conn, cur)
    return resultList

    # 测试结果
    # print(result)

    return result

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

#通过单位号和装备号查找strength某条记录的现有数
def seletNowNumAboutStrength(Unit_ID, Equip_ID, year):
    conn, cur = connectMySql()
    sql = "select Now from strength where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "' and year = '" + year + "'"
    print(sql)
    cur.execute(sql)
    nowNumTuple = cur.fetchall()
    disconnectMySql(conn, cur)
    print(nowNumTuple)

    for nowNumInfo in nowNumTuple:
        return nowNumInfo[0]

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
            nowYearNum = seletNowNumAboutStrength(UnitID, EquipID, year)
            changeYearNum = int(nowYearNum) + addNum
            nowAllNum = seletNowNumAboutStrength(UnitID, EquipID, '')
            changeAllNum = int(nowAllNum) + addNum
            sql = "Update strength set Now = '" + str(changeYearNum) + "' where Equip_ID = '" + \
                  EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

            cur.execute(sql)
            sql = "update strength set Now = '" + str(changeAllNum) + "' where Unit_ID = '" \
                  + UnitID + "' and Equip_ID = '" + EquipID + "' and year = ''"
            print(sql)
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

if __name__ == '__main__':
    pass
