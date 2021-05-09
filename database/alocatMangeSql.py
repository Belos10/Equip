import pymysql
from database.connectAndDisSql  import connectMySql, disconnectMySql

#查询陆军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutArmy():
    conn, cur = connectMySql()

    yearList = []
    sql = "select * from armytransferyear"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    for yearInfo in result:
        yearList.append(yearInfo[1])
    #测试结果
    #print(result)

    return yearList

#查询火箭军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutRocket():
    conn, cur = connectMySql()

    yearList = []
    sql = "select * from rockettransferyear"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)

    for yearInfo in result:
        yearList.append(yearInfo[1])
    # 测试结果
    # print(result)

    return yearList

#查询某年所有的陆军调拨单
def selectArmyTransferByYear(year):
    conn, cur = connectMySql()

    if year == '全部':
        sql = "select * from armytransfer"
    else:
        sql = "select * from armytransfer where year = '" + year + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)

    return result

#查询某年所有的火箭军调拨单
def selectRocketTransferByYear(year):
    conn, cur = connectMySql()

    if year == '全部':
        sql = "select * from rockettransfer"
    else:
        sql = "select * from rockettransfer where year = '" + year + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)

    return result


#向陆军调拨单年份表中添加年份
def insertIntoArmyTransferYear(year):
    conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "insert into armytransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

#向陆军调拨单中添加新数据
def insertIntoArmyTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                           Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                           Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                           Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year):
    conn, cur = connectMySql()
    sql = "INSERT INTO armytransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way," \
          "Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect, Send_Tel, Recive_Name," \
          "Recive_Connect, Recive_Tel, Equip_ID, Equip_Name, Equip_Unit, Equip_Quity, Equip_Num," \
          "Equip_Other, year) VALUES ('" + ID + "', '"  + Trans_ID + "', '"  + Trans_Date + "', '"  + Trans_Reason + \
          "', '"  + Trans + "', '" + Trans_Way + "', '" + Port_Way + "', '" + Effic_Date + "', '" \
          + Send_UnitID + "', '" + Send_UnitName + "', '" + Send_Connect + "', '" + Send_Tel\
          + "', '" + Recive_Name + "', '" + Recive_Connect + "', '" + Recive_Tel + "', '" + Equip_ID + \
          "', '" + Equip_Name + "', '" + Equip_Unit + "', '" + Equip_Quity + "', '" + Equip_Num + "', '" + Equip_Other\
          + "', '" + year + "')"

    #print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

#返回当前年份中陆军调拨单序号
def selectIDFromArmyByYear(year):
    conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "select ID from armyTransfer where year = '" + year + "'"
    print("year: ", sql)

    cur.execute(sql)
    result = cur.fetchall()
    yearList = []
    for year in result:
        yearList.append(year[0])

    disconnectMySql(conn, cur)
    return yearList

#删除当前陆军调拨单中某行数据
def delArmyTransferByIDAndYear(ID, year):
    conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "delete from armyTransfer where ID = '" + ID + "' and year = '" + year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)

#删除陆军调拨单年份表中某年
def delArmyTransferYearByYear(year):
    conn, cur = connectMySql()

    if year == "全部":
        sql = "delete from armyTransferyear"
        # print(sql)
        cur.execute(sql)
        sql = "delete from armyTransfer"
        cur.execute(sql)
    else:
        sql = "delete from armyTransferyear where year = '" + year +  "'"
        # print(sql)
        cur.execute(sql)
        sql = "delete from armyTransfer where year = '" + year +  "'"
        cur.execute(sql)

    conn.commit()
    disconnectMySql(conn, cur)

#向火箭军调拨单年份表中添加年份
def insertIntoRocketTransferYear(year):
    conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "insert into rockettransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)