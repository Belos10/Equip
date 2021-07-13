import anaconda_navigator.external.UniversalAnalytics.Tracker

from database.strengthDisturbSql import *
#new
#查询陆军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutArmy():
    yearList = []
    sql = "select * from armytransferyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    #测试结果
    #print(result)
    return yearList

#查询火箭军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutRocket():
    yearList = []
    sql = "select * from rockettransferyear order by year "
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    # 测试结果
    # print(result)
    return yearList


#查询某年所有的陆军调拨单
def selectArmyTransferByYear(year):
    if year == '全部':
        sql = "select * from armytransfer"
    else:
        sql = "select * from armytransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # 测试结果
    # print(result)
    return result


#查询某年所有的火箭军调拨单
def selectRocketTransferByYear(year):
    if year == '全部':
        sql = "select * from rockettransfer"
    else:
        sql = "select * from rockettransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # 测试结果
    # print(result)
    return result


#向陆军调拨单年份表中添加年份
def insertIntoArmyTransferYear(year):
    result = selectYearListAboutArmy()
    sql = "insert into armytransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    cur.execute(sql)
    conn.commit()



# 向陆军调拨单中添加新数据
def insertIntoArmyTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                           Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                           Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                           Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year):
    sql = "INSERT INTO armytransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect, Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID, Equip_Name, Equip_Unit, Equip_Quity, Equip_Num,Equip_Other, year) VALUES ('" + ID + "', '"  + Trans_ID + "', '"  + Trans_Date + "', '"  + Trans_Reason + \
          "', '"  + Trans + "', '" + Trans_Way + "', '" + Port_Way + "', '" + Effic_Date + "', '" \
          + Send_UnitID + "', '" + Send_UnitName + "', '" + Send_Connect + "', '" + Send_Tel\
          + "', '" + Recive_Name + "', '" + Recive_Connect + "', '" + Recive_Tel + "', '" + Equip_ID + \
          "', '" + Equip_Name + "', '" + Equip_Unit + "', '" + Equip_Quity + "', '" + Equip_Num + "', '" + Equip_Other\
          + "', '" + year + "')"
    # print(sql)
    cur.execute(sql)
    conn.commit()


# 向火箭军调拨单中添加新数据
def insertIntoRocketTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                           Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                           Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                           Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year):
    sql = "INSERT INTO rockettransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way, Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect, Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID, Equip_Name, Equip_Unit, Equip_Quity, Equip_Num,Equip_Other, year) VALUES ('" + ID + "', '"  + Trans_ID + "', '"  + Trans_Date + "', '"  + Trans_Reason + \
          "', '"  + Trans + "', '" + Trans_Way + "', '" + Port_Way + "', '" + Effic_Date + "', '" \
          + Send_UnitID + "', '" + Send_UnitName + "', '" + Send_Connect + "', '" + Send_Tel\
          + "', '" + Recive_Name + "', '" + Recive_Connect + "', '" + Recive_Tel + "', '" + Equip_ID + \
          "', '" + Equip_Name + "', '" + Equip_Unit + "', '" + Equip_Quity + "', '" + Equip_Num + "', '" + Equip_Other\
          + "', '" + year + "')"
    # print("insertIntoRocketTransfersql",sql)
    cur.execute(sql)
    conn.commit()

def selectEquipIDFromArmyByYear(year):
    #result = selectYearListAboutArmy()
    sql = "select Equip_ID from armyTransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    equipID = []
    for year in result:
        equipID.append(year[0])
    return equipID

#返回当前年份中陆军调拨单序号
def selectIDFromArmyByYear(year):
    #conn, cur = connectMySql()
    #result = selectYearListAboutArmy()
    sql = "select ID from armyTransfer where year = '" + year + "'"
    # print("year: ", sql)
    cur.execute(sql)
    result = cur.fetchall()
    yearList = []
    for year in result:
        yearList.append(year[0])
    #disconnectMySql(conn, cur)
    return yearList


#删除当前陆军调拨单中某行数据
def delArmyTransferByIDAndYear(ID, year):
    #conn, cur = connectMySql()
    result = selectYearListAboutArmy()
    sql = "delete from armyTransfer where ID = '" + ID + "' and year = '" + year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)


#删除陆军调拨单年份表中某年
def delArmyTransferYearByYear(year):
    sql = "delete from armyTransferyear where year = '" + year +  "'"
    # print(sql)
    cur.execute(sql)
    sql = "delete from armyTransfer where year = '" + year +  "'"
    cur.execute(sql)
    conn.commit()


#向火箭军调拨单年份表中添加年份
def insertIntoRocketTransferYear(year):
    result = selectYearListAboutArmy()
    sql = "insert into rockettransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()


# 读取单个分配计划数，结果为 'xxx'
def selectOrderPlanNum(Unit_ID, Equip_ID, Year):
    sql = "select OrderNum from orderallotplan where Unit_Id = '" + Unit_ID + \
          "' and Equip_Id = '" + Equip_ID + "' and Year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result[0][0]

# 读取单个退役计划数，结果为 'xxx'
def selectOrderRetirePlanNum(Unit_ID, Equip_ID, Year):
    sql = "select RetireNum from orderretireplan where Unit_Id = '" + Unit_ID + \
          "' and Equip_Id = '" + Equip_ID + "' and Year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result[0][0]


# 按list读取批量分配计划数
def selectOrderAllotPlanNumByList(UnitList, EquipList, Year):
    resultList = []
    for Unit_ID in UnitList.values():
        for Equip_ID in EquipList.values():
            sql = "select OrderNum from orderallotplan where Unit_Id = '" + Unit_ID[0] + \
                  "' and Equip_Id = '" + Equip_ID[0] + "' and Year = '" + Year + "'"
            cur.execute(sql)
            result = cur.fetchall()
            if len(result)!=0:
                for resultInfo in result:
                    resultList.append(resultInfo[0])
    return resultList


# 更新分配计划数与实力数
def updateOrderPlanNum(Equip_Id, Unit_Id, Year, OrderNum, originalOrderPlanNum):
    if originalOrderPlanNum == '':
        originalOrderPlanNum = 0
    if OrderNum == '':
        OrderNum = 0
    updateOrderPlanNumUper(Equip_Id, Unit_Id, Year, OrderNum, originalOrderPlanNum)
    updateStrengthAboutStrengrh(Unit_Id, Equip_Id, Year, OrderNum, originalOrderPlanNum)
    conn.commit()

# 更新上级分配计划数
def updateOrderPlanNumUper(Equip_Id, Unit_Id, Year, OrderNum, originalOrderPlanNum):
    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_Id, UnitIDList)
    findEquipUperIDList(Equip_Id, EquipIDList)
    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            originalNum = selectOrderPlanNum(UnitID, EquipID, Year)
            if originalNum == '':
                originalNum = 0
            num = int(originalNum) - int(originalOrderPlanNum) + int(OrderNum)
            sql="update orderallotplan set OrderNum = '"+ str(num) + "'where Equip_Id='" + EquipID + "'and Unit_Id ='" \
                + UnitID + "' and Year = '" + Year + "'"
            cur.execute(sql)
    conn.commit()


# 读取分配计划年份
def selectYearListAboutOrderPlan():
    yearList = []
    sql = "select * from orderallotplanyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 新增分配计划年份
def insertIntoOrderPlanYear(year):
    UnitList = []
    EquipList=selectAllDataAboutEquip()
    selectAllDataAboutUnit(UnitList)
    result = selectYearListAboutOrderPlan()
    sql = "insert into orderallotplanyear (num, year,proof) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "','')"
    #print(sql)
    cur.execute(sql)
    for EquipInfo in EquipList:
        sql = "insert into orderallotplannote(Equip_id,Equip_Name,Year,Note) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + str(year) +"', '' )"
        cur.execute(sql)
        sql = "insert into orderallotschedule (Equip_Id,Equip_Name,army,allotconditionUper,rocketUper,finishUper,year) values " \
              + "('" + EquipInfo[0] + "','" + EquipInfo[1] + "', '0','0','0','0','" + str(year) + "' )"
        cur.execute(sql)
        for UnitInfo in UnitList:
            sql = "insert into orderallotplan(Equip_id,Equip_Name,Unit_Id,Unit_Name,Year,OrderNum) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + UnitInfo[0] +\
                    "','" + UnitInfo[1] + "','"+ str(year) +"', '' )"
            cur.execute(sql)
    conn.commit()


# 删除分配计划年份
def deleteOrderPlanYear(year):
    # conn, cur = connectMySql()
    sql = "delete from orderallotplanyear where year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderallotplannote where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderallotplan where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderallotschedule where Year= '" + year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

def selectOrderPlanInputNumBase(EquipList, Year):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select InputNumBase from orderallotplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])
    #print("自定义输入数字",resultList)
    # disconnectMySql(conn, cur)
    return resultList


def selectOrderPlanInputNumUpmost(EquipList, Year):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select InputNumUpmost from orderallotplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])
    #print("自定义输入数字",resultList)
    # disconnectMySql(conn, cur)
    return resultList

# 读取年份对应调拨依据
def selectOrderPlanProof(year):
    # conn, cur = connectMySql()
    sql = "select proof from orderallotplanyear where year= '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #disconnectMySql(conn, cur)
    return result

# 修改Allot年份对应调拨依据
def updateOrderPlanProof(year, proof):
    # conn, cur = connectMySql()
    sql = "update orderallotplanyear set proof = '" + proof + "' where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# 修改Retire年份对应调拨依据
def updateOrderRetirePlanProof(year, proof):
    # conn, cur = connectMySql()
    sql = "update orderretireplanyear set proof = '" + proof + "' where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# 读取分配计划备注
def selectOrderPlanNote(EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Note from orderallotplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])

    # disconnectMySql(conn, cur)
    return resultList


# 读取分配计划军委计划数与装备单位
def selectOrderPlanOther(EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Equip_Unit,Equip_Num from armytransfer where Equip_Id = '" + Equip_ID[0] + "' and year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        #print("other result",result)
        if result:
            resultList.append(result)
        else:
            resultList.append([])
    # print("陆军调拨单resultList", resultList)
    return resultList


# 更新自定义分配数  机关
def updateOrderPlanInputNumUpmost(Equip_Id, Year, InputNum):
    # conn,cur=connectMySql()
    sql= "update orderallotplannote set InputNumUpmost ='" + InputNum + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 更新自定义分配数  基地
def updateOrderPlanInputNumBase(Equip_Id, Year, InputNum):
    # conn,cur=connectMySql()
    sql= "update orderallotplannote set InputNumBase ='" + InputNum + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 更新分配计划备注
def updateOrderPlanNote(Equip_Id, Year, Note):
    # conn,cur=connectMySql()
    sql="update orderallotplannote set Note='"+ Note + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 查询陆军调拨单进度
def selectArmySchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "select army from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询是否具备条件进度(基地)
def selectAllotConditionBase(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select allotconditionBase from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询是否具备条件进度(机关)
def selectAllotConditionUper(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select allotconditionUper from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询火箭军调拨单进度(基地)
def selectRocketScheduleBase(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select rocketBase from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询火箭军调拨单进度(机关)
def selectRocketScheduleUper(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select rocketUper from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询是否完成(基地)
def selectIfScheduleFinishBase(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select finishBase from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result


# 查询是否完成(机关)
def selectIfScheduleFinishUper(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "select finishUper from orderallotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 更新陆军调拨单进度
def updateArmySchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set army = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新是否具备条件进度
def updateAllotConditionBase(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set allotconditionBase = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)


# 更新是否具备条件进度
def updateAllotConditionUper(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set allotconditionUper = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新火箭军调拨单进度(机关)
def updateRocketScheduleBase(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set rocketBase = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新火箭军调拨单进度(基地)
def updateRocketScheduleUper(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set rocketUper = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新是否完成进度(基地)
def updateScheduleFinishBase(Equip_Id, Year, fileName):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set finishBase = '" + fileName + "' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# 更新是否完成进度(机关)
def updateScheduleFinishUper(Equip_Id, Year, fileName):
    # conn, cur = connectMySql()
    sql = "update orderallotschedule set finishUper = '" + fileName + "' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# 陆军调拨号与装备质量
def selectQuaAndID(Equip_ID, year):
    sql = "select Equip_Quity,Trans_ID from armytransfer where Equip_ID = '" + Equip_ID + "'and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # print("找质量和陆军单号result", result)
    conn.commit()
    return result

# # 按装备ID列表从unit表复制数据至Orderplanunit表
# def insertIntoDisturbPlanUnitFromList(UnitList):
#     # conn,cur = connectMySql()
#     equipInfoTuple = selectAllDataAboutEquip()
#     OrderplanYearInfoTuple = selectYearListAboutOrderPlan()
#     for i in UnitList:
#         unitInfo = selectUnitInfoByUnitID(i)
#         sql = "insert into disturbplanunit select * from unit where Unit_ID = '" + i + "'"
#         cur.execute(sql)
#         for equipInfo in equipInfoTuple:
#             for OrderplanYearInfo in OrderplanYearInfoTuple:
#                 sql = "insert into orderallotplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,OrderNum) values " \
#                       + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + i + \
#                       "','" + unitInfo[1] + "','" + OrderplanYearInfo[1] + "', '' )"
#                 cur.execute(sql)
#
#     conn.commit()
#     #  disconnectMySql(conn,cur)

# 查找是否是第三级目录的各基地
def selectUnitIfBase(unitID):
    # conn, cur = connectMySql()
    sql = "select Unit_Uper from unit where Unit_ID = '" + unitID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # disconnectMySql(conn, cur)
    if result[0][0] == '2':
        return True
    else:
        return False


def selectOrderPlanChooseUnit():
    # conn, cur = connectMySql()
    sql = "select * from unit where Unit_Uper= '2' or Unit_ID = '3'"
    cur.execute(sql)
    result = cur.fetchall()
    # disconnectMySql(conn, cur)
    if result:
        return result
    else:
        return []

def selectLevelForEquip(Equip_ID, count = -1):
    sql = "select Equip_Uper from equip where Equip_ID = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    result_Uper = result[0][0]
    if result_Uper != '':
        count = selectLevelForEquip(result_Uper, count + 1)
    return count


'''
退役报废计划
'''
# 读取分配计划年份
def selectYearListAboutOrderRetirePlan():
    yearList = []
    sql = "select * from orderretireplanyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 新增分配计划年份
def insertIntoOrderRetirePlanYear(year):
    #conn, cur = connectMySql()
    EquipList=selectAllDataAboutEquip()
    UnitList=[]
    selectAllDataAboutUnit(UnitList)
    result = selectYearListAboutOrderRetirePlan()
    sql = "insert into orderretireplanyear (num, year,proof) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "','')"
    #print(sql)
    cur.execute(sql)
    for EquipInfo in EquipList:
        sql = "insert into orderretireplannote(Equip_id,Equip_Name,Year,Note) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + str(year) +"', '' )"
        cur.execute(sql)
        # sql = "insert into allotschedule (Equip_Id,Equip_Name,army,allotcondition,rocket,finish,year) values " \
        #       + "('" + EquipInfo[0] + "','" + EquipInfo[1] + "', '0','0','0','0','" + str(year) + "' )"
        # cur.execute(sql)
        for UnitInfo in UnitList:
            sql = "insert into orderretireplan(Equip_id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + UnitInfo[0] +\
                    "','" + UnitInfo[1] + "','"+ str(year) +"', '' )"
            cur.execute(sql)

    conn.commit()
    #disconnectMySql(conn, cur)

# 删除分配计划年份
def deleteOrderRetirePlanYear(year):
    #conn, cur = connectMySql()
    sql = "delete from orderretireplanyear where year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderretireplannote where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderretireplan where Year= '" + year + "'"
    cur.execute(sql)
    # sql = "delete from allotschedule where year= '" + year + "'"
    # cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# def selectRetirePlanUnitInfoByUnitID(Unit_ID):
#     #conn, cur = connectMySql()
#     sql = "select * from disturbplanunit where Unit_ID = '" + Unit_ID + "'"
#     cur.execute(sql)
#     result = cur.fetchall()
#     for info in result:
#         #disconnectMySql(conn, cur)
#         return info

# 更新退役计划数
def updateOrderRetirePlanNum(Equip_Id, Unit_Id, Year, RetireNum, originalRetirePlanNum):
    if originalRetirePlanNum == '':
        originalRetirePlanNum = 0
    if RetireNum == '':
        RetireNum = 0
    updateRetirePlanNumUper(Equip_Id, Unit_Id, Year, RetireNum, originalRetirePlanNum)
    updateStrengthAboutStrengrh(Unit_Id, Equip_Id, Year, 0-int(RetireNum), 0-int(originalRetirePlanNum))
    conn.commit()


# 更新上级分配计划数
def updateRetirePlanNumUper(Equip_Id,Unit_Id,Year,RetireNum,originalRetirePlanNum):
    EquipIDList = []
    UnitIDList = []
    findUnitUperIDList(Unit_Id, UnitIDList)
    findEquipUperIDList(Equip_Id, EquipIDList)
    for UnitID in UnitIDList:
        for EquipID in EquipIDList:
            originalNum = selectOrderRetirePlanNum(UnitID, EquipID, Year)
            if originalNum == '':
                originalNum = 0
            num = int(originalNum) - int(originalRetirePlanNum) + int(RetireNum)
            sql="update orderretireplan set RetireNum='"+ str(num) + "'where Equip_Id='" + EquipID + "'and Unit_Id ='" \
                + UnitID + "' and Year = '" + Year + "'"
            cur.execute(sql)
    conn.commit()

# 更新分配计划备注
def updateOrderRetirePlanNote(Equip_Id, Year, Note):
    sql="update orderretireplannote set Note='"+ Note + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()


# 读取分配计划备注
def selectOrderRetirePlanNote(EquipList, YearList):
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Note from orderretireplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])
    return resultList


# 按list读取批量分配计划数
def selectOrderRetirePlanNumByList(UnitList, EquipList, YearList):
    resultList = []
    for Unit_ID in UnitList.values():
        for Equip_ID in EquipList.values():
            sql = "select RetireNum from orderretireplan where Unit_Id = '" + Unit_ID[0] + \
                  "' and Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
            cur.execute(sql)
            result = cur.fetchall()
            if len(result)!=0:
                for resultInfo in result:
                    resultList.append(resultInfo[0])
    return resultList

# def findRetirePlanUnitChildInfo(unitId):
#     sql = "select * from disturbplanunit where Unit_Uper = '" + unitId + "'"
#     cur.execute(sql)
#     result = cur.fetchall()
#     if result:
#         return result
#     else:
#         return []


'''
    调整计划
'''

# 新增分配计划年份
def insertIntoOrderAdjustYear(year):
    UnitList = []
    EquipList=selectAllDataAboutEquip()
    selectAllDataAboutUnit(UnitList)
    result = selectYearListAboutOrderAdjust()
    sql = "insert into orderadjustyear (num, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    cur.execute(sql)
    for EquipInfo in EquipList:
        sql = "insert into orderAdjust(year,equip_id,equipName,equipUnit,costUnit,oneYear_LastNum,oneYear_NowNum," \
              "oneYear_NextNum,oneYear_Amount,twoYear_LastNum,twoYear_NowNum,twoYear_NextNum,twoYear_Amount," \
              "applicationUnit,supplierUnit,buyMode,manufacturer,adjustFactor,allotUnit,note) values " +\
                  "('" + str(year) + "','" + EquipInfo[0] + "','" + EquipInfo[1] +"', '','','','','','','','','',''," \
                                                                                  "'','','','','','','' ) "
        cur.execute(sql)
        sql = "insert into orderAdjustCont (year,equip_Id,equip_Name,contSource,makeProj1,bid2,approval3,status1," \
              "signContract2,finish3) values " \
              + "('" + str(year) + "','" + EquipInfo[0] + "','" + EquipInfo[1] + "','','','','','','','' )"
        cur.execute(sql)
    conn.commit()


# 删除分配计划年份
def deleteOrderAdjustYear(year):
    sql = "delete from orderadjustyear where year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderAdjust where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from orderAdjustCont where Year= '" + year + "'"
    cur.execute(sql)
    conn.commit()


# 读取分配计划年份
def selectYearListAboutOrderAdjust():
    yearList = []
    sql = "select * from orderadjustyear order by year"
    cur.execute(sql)
    result = cur.fetchall()
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList

# EquipList字典形式  返回 [(xxx),(xxx),(xxx)] 数据
def selectOrderAdjustDataByList(EquipList,Year):
    resultList = []
    for EquipInfo in EquipList.values():
        sql = "select * from orderAdjust where equip_ID = '" + EquipInfo[0] + "' and year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) != 0:
            resultList.append(result[0])
    return resultList


# EquipList字典形式  返回 [(xxx),(xxx),(xxx)] 数据
def selectOrderAdjustContDataByList(EquipList,Year):
    resultList = []
    for EquipInfo in EquipList.values():
        sql = "select * from orderAdjustCont where equip_ID = '" + EquipInfo[0] + "' and year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) != 0:
            resultList.append(result[0])
    return resultList


# 按equip_ID号和年份 检索合同来源表  返回 [xxx]
def selectOneOrderAdjustContData(equip_ID,Year):
    sql = "select * from orderAdjustCont where equip_ID = '" + equip_ID + "' and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # print(result[0])
    return result[0]

# 某年某装备是否选择了合同来源
def ifHaveContSource(equip_ID,Year):
    sql = "select contSource from orderAdjustCont where equip_ID = '" + equip_ID + "' and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result[0][0]=='单一来源' or result[0][0]=='招标':
        # return True
        return result[0][0]
    else:
        return False

# 按Data数组更新调整计划表
def updateOrderAdjustData(equip_ID,data,year):
    sql = "update orderAdjust set costUnit = '" + data[0] + "' , oneYear_LastNum = '" + data[1] + "', oneYear_NowNum = '" + data[2] \
          + "' , oneYear_NextNum = '" + data[3] + "' , oneYear_Amount = '" + data[4] + "' , twoYear_LastNum = '" + data[5] \
          + "' , twoYear_NowNum = '" + data[6] + "' , twoYear_NextNum = '" + data[7] + "' , twoYear_Amount = '" + data[8] \
          + "' , applicationUnit = '" + data[9] + "' , supplierUnit = '" + data[10] + "' , buyMode = '" + data[11] \
          + "' , manufacturer = '" + data[12] + "' , adjustFactor = '" + data[13] + "' , allotUnit = '" + data[14] \
          + "' , note = '" + data[15] + "' where equip_ID = '" + equip_ID + "' and year = '" + year + "'"
    cur.execute(sql)
    conn.commit()

# 更新装备的合同来源
def updateContSource(contSource,equip_ID,Year):
    sql = "update orderAdjustCont set contSource = '" + contSource + "' where equip_ID = '" + \
          equip_ID + "' and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()

# 更新单一来源装备的合同进度表
def udpateOrderAdjustContSingle(equip_ID,data,Year):
    sql = "update orderAdjustCont set makeProj1 = '" + data[1] + "' , bid2 = '" + data[2] \
          + "' , approval3 = '" + data[3] + "' , status1 = '" + data[0] \
          + "' , signContract2 = '" + data[4] + "' , finish3 = '" + data[5] + "' where equip_ID = '" + \
          equip_ID + "' and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()

# 更新招标来源装备的合同进度表
def udpateOrderAdjustContBid(equip_ID, data, Year):
    sql = "update orderAdjustCont set makeProj1 = '" + data[0] + "' , bid2 = '" + data[1] \
          + "' , approval3 = '" + data[2] + "' where equip_ID = '" + \
          equip_ID + "' and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()

# 返回某一年的合同 [(xxx),(xxx),(xxx)]
def selectDataFromContractOrder(Year):
    sql = "select * from contract_order where year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result