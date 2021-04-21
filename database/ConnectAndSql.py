import pymysql


def Clicked(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    cur.execute(sql)
    # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
    data = cur.fetchall()
    # 打印测试
    # print(data)
    cur.close()
    conn.close()
    return data


'''
    功能：
        找到某个单位的所有下级单位
        Unit_ID: 需要找的单位的ID号
        childUnitList：存放该单位所有下级单位，包括自己，自己在0位置
        cur：执行sql语句
'''


def findChildUnit(Unit_ID, childUnitList, cur):
    childUnitList.append(Unit_ID)
    sql = "select Dept_ID from dept where Dept_Uper = '" + Unit_ID + "'"
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
    sql = "select Dept_Name from dept where Dept_ID = '" + Unit_ID + "'"
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
    sql = "select Dept_ID from dept where Dept_Uper = '" + UnitID + "'"
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
        sql = "select * from equipandunit where Unit_ID = '" + UnitID + "' and Equip_ID = '" + EquipID + "'"
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
                sql = "select * from equipandunit where Unit_ID = '" + each_ID + "' and Equip_ID = '" + equip_ID + "'"
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
    print(final_result)
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
        sql = "select * from equipandunit where Unit_ID = '" + UnitID + "' and Equip_ID = '" + EquipID + "'"
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
                sql = "select * from equipandunit where Unit_ID = '" + unit_ID + "' and Equip_ID = '" + each_ID + "'"
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
        sql = "select * from equipandunit where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
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
            sql = "select * from equipandunit where Unit_ID = '" + unitID + "' and Equip_ID = '" + equipID + "'"
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
    sql = "select * from dept where Dept_Uper = '" + Unit_ID + "'"
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
    sql = "select * from equipandunit where Unit_ID = '" + Unit_ID + "' and Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for num in result:
        changeNum = int(num[4]) + int(addNum)
    sql = "Update equipandunit set Strengh = '" + changeNum + "' where Equip_ID = '" + Equip_ID + "' and Unit_ID = '" + Unit_ID + "'"
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
    sql = "INSERT INTO dept (Dept_ID, Dept_Name, Dept_Uper) VALUES" \
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
    sql = "delete from equipandunit where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    cur.execute(sql)
    sql = "delete from inputinfo where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def update_Unit_Dict(Unit_ID, Unit_Name, Unit_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "Update dept set Dept_Name = '" + Unit_Name + "', Dept_Uper = '" + Unit_Uper + "' where Dept_ID = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def selectUnitDictByUper(Unit_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select * from dept where Dept_Uper = '" + Unit_Uper + "'"
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
    sql = "delete from dept where Dept_ID = '" + Unit_ID + "'"
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def del_Unit_And_Child(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from dept where Dept_ID = '" + Unit_ID + "'" + "and Dept_Uper = '" + Unit_ID + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 增加单位目录
def add_UnitDictDept(Unit_ID, Unit_Name, Unit_Uper):
    # print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO dept (Dept_ID, Dept_Name, Dept_Uper) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "')"
    # print(sql)
    # print(sql)
    # 执行sql语句，并发送给数据库
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
    sql = "delete from dept where Equip_ID = '" + Equip_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    update_Unit_Dict('019', 'd', '')
