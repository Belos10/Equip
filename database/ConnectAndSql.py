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


def insert_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO inputinfo (Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other) VALUES" \
          + "('" + Unit_ID + "','" + Equip_ID + "','" + ID + "','" + num + "','" + year + "','" + shop + "','" + state \
          + "','" + arrive + "','" + confirm + "','" + other + "')"
    print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def add_UnitDict(Unit_ID, Unit_Name, Unit_Uper):
    print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "INSERT INTO dept (Dept_ID, Dept_Name, Dept_Uper) VALUES" \
          + "('" + Unit_ID + "','" + Unit_Name + "','" + Unit_Uper + "')"
    print(sql)
    print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def delete_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="equ2")
    cur = conn.cursor()
    sql = "delete from inputinfo where (Unit_ID=  '" + (Unit_ID or None) + "' AND Equip_ID='" + (Equip_ID or None) \
          + "' AND ID='" + (ID or None) + "' AND num='" + (num or None) + "')"
    print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def delete_Inquiry_Clicked(Unit_ID, Equip_ID):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="equ2")
    cur = conn.cursor()
    sql = "delete from equipandunit where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    print(sql)
    cur.execute(sql)
    sql = "delete from inputinfo where (Unit_ID=  '" + Unit_ID + "' AND Equip_ID='" + Equip_ID + "')"
    print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def update_Unit_Dict(Unit_ID, Unit_Name, Unit_Uper):
    print("''''''''''")
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    # 插入的sql语句
    sql = "Update dept set Dept_Name = '" + Unit_Name + "', Dept_Uper = '" + Unit_Uper + "' where Dept_ID = '" + Unit_ID + "'"
    print(sql)
    print(sql)
    # 执行sql语句，并发送给数据库
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    update_Unit_Dict('019', 'd', '')