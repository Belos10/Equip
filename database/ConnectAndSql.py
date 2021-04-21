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


# 信息录入界面添加
def insert_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    # print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "','" + num + "','" + year + "','" + shop + "','" + state \
          + "','" + arrive + "','" + confirm + "','" + other + "')"
    # print(sql)
    # 执行sql语句，并发送给数据库
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


# 信息逐号录入界面删除
def delete_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "delete from inputinfo where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID \
          + "' AND ID='" + ID + "' AND num='" + num + "')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 删除选中装备
def delete_Inquiry_Clicked(Unit_ID, Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "delete from equipandunit where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    # print(sql)
    cur.execute(sql)
    sql = "delete from inputinfo where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 更改单位目录
def update_Unit_Dict(Unit_ID, Unit_Name, Unit_Uper):
    print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "Update dept set Dept_Name = '" + Unit_Name + "', Dept_Uper = '" + Unit_Uper + "' where Dept_ID = '" + Unit_ID + "'"
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


def selectUnitDictByUper(Unit_Uper):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select * from dept where Dept_Uper = '" + Unit_Uper + "'"
    # print(sql)
    cur.execute(sql)
    # 获取查询到的数据，是以字典的形式存储的，所以读取需要使用data[i][j]下标定位
    data = cur.fetchall()
    # 打印测试
    # print(data)
    cur.close()
    conn.close()
    return data


# 删除单位目录
def del_Unit_Dict(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from dept where Dept_ID = '" + Unit_ID + "'"
    # print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# 删除单位及子目录
def del_Unit_And_Child(Unit_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "delete from dept where Dept_ID = '" + Unit_ID + "'" + "and Dept_Uper = '" + Unit_ID + "'"
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


if __name__ == '__main__':
    update_Unit_Dict('019', 'd', '')
