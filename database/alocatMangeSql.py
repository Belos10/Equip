from database.strengthDisturbSql import *
#new
#查询陆军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutArmy():
    #conn, cur = connectMySql()

    yearList = []
    sql = "select * from armytransferyear order by year"

    cur.execute(sql)
    result = cur.fetchall()

    #disconnectMySql(conn, cur)

    for yearInfo in result:
        yearList.append(yearInfo[1])
    #测试结果
    #print(result)

    return yearList

#查询火箭军调拨单所有年份表, 返回全部年份列表
def selectYearListAboutRocket():
    #conn, cur = connectMySql()
    yearList = []
    sql = "select * from rockettransferyear order by year "
    cur.execute(sql)
    result = cur.fetchall()
    #disconnectMySql(conn, cur)
    for yearInfo in result:
        yearList.append(yearInfo[1])
    # 测试结果
    # print(result)
    return yearList


#查询某年所有的陆军调拨单
def selectArmyTransferByYear(year):
    #conn, cur = connectMySql()
    if year == '全部':
        sql = "select * from armytransfer"
    else:
        sql = "select * from armytransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


#查询某年所有的火箭军调拨单
def selectRocketTransferByYear(year):
    #conn, cur = connectMySql()
    if year == '全部':
        sql = "select * from rockettransfer"
    else:
        sql = "select * from rockettransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #disconnectMySql(conn, cur)
    # 测试结果
    # print(result)
    return result


#向陆军调拨单年份表中添加年份
def insertIntoArmyTransferYear(year):
    #conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "insert into armytransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)


#向陆军调拨单中添加新数据
def insertIntoArmyTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                           Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                           Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                           Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year):
    # conn, cur = connectMySql()
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
    # disconnectMySql(conn, cur)


#向火箭军调拨单中添加新数据
def insertIntoRocketTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                           Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                           Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                           Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year):
    #conn, cur = connectMySql()
    sql = "INSERT INTO rockettransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way," \
          "Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect, Send_Tel, Recive_Name," \
          "Recive_Connect, Recive_Tel, Equip_ID, Equip_Name, Equip_Unit, Equip_Quity, Equip_Num," \
          "Equip_Other, year) VALUES ('" + ID + "', '"  + Trans_ID + "', '"  + Trans_Date + "', '"  + Trans_Reason + \
          "', '"  + Trans + "', '" + Trans_Way + "', '" + Port_Way + "', '" + Effic_Date + "', '" \
          + Send_UnitID + "', '" + Send_UnitName + "', '" + Send_Connect + "', '" + Send_Tel\
          + "', '" + Recive_Name + "', '" + Recive_Connect + "', '" + Recive_Tel + "', '" + Equip_ID + \
          "', '" + Equip_Name + "', '" + Equip_Unit + "', '" + Equip_Quity + "', '" + Equip_Num + "', '" + Equip_Other\
          + "', '" + year + "')"

    print("insertIntoRocketTransfersql",sql)
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

def selectEquipIDFromArmyByYear(year):
    # conn, cur = connectMySql()
    result = selectYearListAboutArmy()
    sql = "select Equip_ID from armyTransfer where year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    equipID = []
    for year in result:
        equipID.append(year[0])
    #disconnectMySql(conn, cur)
    return equipID

#返回当前年份中陆军调拨单序号
def selectIDFromArmyByYear(year):
    #conn, cur = connectMySql()
    result = selectYearListAboutArmy()
    sql = "select ID from armyTransfer where year = '" + year + "'"
    print("year: ", sql)
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
    #conn, cur = connectMySql()


    sql = "delete from armyTransferyear where year = '" + year +  "'"
    # print(sql)
    cur.execute(sql)
    sql = "delete from armyTransfer where year = '" + year +  "'"
    cur.execute(sql)

    conn.commit()
    #disconnectMySql(conn, cur)

#向火箭军调拨单年份表中添加年份
def insertIntoRocketTransferYear(year):
    #conn, cur = connectMySql()

    result = selectYearListAboutArmy()
    sql = "insert into rockettransferyear (ID, year) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "')"
    #print(sql)
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)



# 按list读取批量分配计划数
def selectDisturbPlanNum(UnitList, EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Unit_ID in UnitList.values():
        for Equip_ID in EquipList.values():
            sql = "select DisturbNum from disturbplan where Unit_Id = '" + Unit_ID[0] + \
                  "' and Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
            cur.execute(sql)
            result = cur.fetchall()
            if len(result)!=0:
                for resultInfo in result:
                    resultList.append(resultInfo[0])
            else:
                resultList.append('-1')
    #disconnectMySql(conn, cur)
    return resultList


# 更新分配计划数
def updateDisturbPlanNum(Equip_Id,Unit_Id,Year,DisturbNum):
    #conn,cur=connectMySql()
    sql="update disturbplan set DisturbNum='"+ DisturbNum + "'where Equip_Id='" + Equip_Id + "'and Unit_Id ='" \
        + Unit_Id + "' and Year = '" + Year + "'"
    print("===========", sql)
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn,cur)


# 读取分配计划年份
def selectYearListAboutDisturbPlan():
    #conn, cur = connectMySql()
    yearList = []
    sql = "select * from disturbplanyear order by year"

    cur.execute(sql)
    result = cur.fetchall()

    # disconnectMySql(conn, cur)
    for yearInfo in result:
        yearList.append(yearInfo[1])
    return yearList


# 新增分配计划年份
def insertIntoDisturbPlanYear(year):
    #conn, cur = connectMySql()
    UnitList = []
    EquipList=selectAllDataAboutEquip()
    selectAllDataAboutUnit(UnitList)
    result = selectYearListAboutDisturbPlan()
    sql = "insert into disturbplanyear (num, year,proof) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "','')"
    #print(sql)
    cur.execute(sql)
    for EquipInfo in EquipList:
        sql = "insert into disturbplannote(Equip_id,Equip_Name,Year,Note) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + str(year) +"', '' )"
        cur.execute(sql)
        sql = "insert into allotschedule (Equip_Id,Equip_Name,army,allotcondition,rocket,finish,year) values " \
              + "('" + EquipInfo[0] + "','" + EquipInfo[1] + "', '0','0','0','0','" + str(year) + "' )"
        cur.execute(sql)
        for UnitInfo in UnitList:
            sql = "insert into disturbplan(Equip_id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + UnitInfo[0] +\
                    "','" + UnitInfo[1] + "','"+ str(year) +"', '' )"
            cur.execute(sql)

    conn.commit()
    #disconnectMySql(conn, cur)


# 删除分配计划年份
def deleteDisturbPlanYear(year):
    # conn, cur = connectMySql()
    sql = "delete from disturbplanyear where year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from disturbplannote where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from disturbplan where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from allotschedule where year= '" + year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

def selectDisturbPlanInputNumBase(EquipList, Year):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select InputNumBase from disturbplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])
    #print("自定义输入数字",resultList)
    # disconnectMySql(conn, cur)
    return resultList


def selectDisturbPlanInputNumUpmost(EquipList, Year):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select InputNumUpmost from disturbplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + Year + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])
    #print("自定义输入数字",resultList)
    # disconnectMySql(conn, cur)
    return resultList

# 读取年份对应调拨依据
def selectDisturbPlanProof(year):
    # conn, cur = connectMySql()
    sql = "select proof from disturbplanyear where year= '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #disconnectMySql(conn, cur)
    return result

# 修改年份对应调拨依据
def updateDisturbPlanProof(year,proof):
    # conn, cur = connectMySql()
    sql = "update disturbplanyear set proof = '" + proof + "' where year = '" + year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)


# 读取分配计划备注
def selectDisturbPlanNote(EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Note from disturbplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])

    # disconnectMySql(conn, cur)
    return resultList


# 读取分配计划军委计划数与装备单位
def selectDisturbPlanOther(EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Equip_Unit,Equip_Num from armytransfer where Equip_Id = '" + Equip_ID[0] + "' and year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        print("other result",result)
        if result:
            pass
        else:
            resultList.append([])
        for resultInfo in result:
            resultList.append(resultInfo)
    print("Other", resultList)
    # disconnectMySql(conn, cur)
    return resultList

# 读取火箭军计划数
def selectRocketOther(EquipList, YearList):
    # conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Equip_Num from rockettransfer where Equip_Id = '" + Equip_ID[0] + "' and year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        #print("other result",result)
        if result:
            pass
        else:
            resultList.append([])
        for resultInfo in result:
            resultList.append(resultInfo)
    print("火箭军调拨", resultList)
    # disconnectMySql(conn, cur)
    return resultList

# 更新自定义分配数  机关
def updateDisturbPlanInputNumUpmost(Equip_Id,Year,InputNum):
    # conn,cur=connectMySql()
    sql= "update disturbplannote set InputNumUpmost ='" + InputNum + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 更新自定义分配数  基地
def updateDisturbPlanInputNumBase(Equip_Id,Year,InputNum):
    # conn,cur=connectMySql()
    sql= "update disturbplannote set InputNumBase ='" + InputNum + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 更新分配计划备注
def updateDisturbPlanNote(Equip_Id,Year,Note):
    # conn,cur=connectMySql()
    sql="update disturbplannote set Note='"+ Note + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 查询陆军调拨单进度
def selectArmySchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "select army from allotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询是否具备条件进度
def selectAllotCondition(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "select allotcondition from allotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询火箭军调拨单进度
def selectRocketSchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "select rocket from allotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 查询是否完成
def selectIfScheduleFinish(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "select finish from allotschedule where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 更新陆军调拨单进度
def updateArmySchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "update allotschedule set army = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新是否具备条件进度
def updateAllotCondition(Equip_Id, Year):
    # conn, cur = connectMySql()
    sql = "update allotschedule set allotcondition = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    print(sql)
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新火箭军调拨单进度
def updateRocketSchedule(Equip_Id,Year):
    # conn, cur = connectMySql()
    sql = "update allotschedule set rocket = '1' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn, cur)

# 更新是否完成进度
def updateScheduleFinish(Equip_Id,Year,fileName):
    # conn, cur = connectMySql()
    sql = "update allotschedule set finish = '" + fileName + "' where Equip_Id = '" + Equip_Id + "'and year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

# 陆军调拨号与装备质量
def selectQuaAndID(Equip_ID, year):
    # conn, cur = connectMySql()
    sql = "select Equip_Quity,Trans_ID from armytransfer where Equip_ID = '" + Equip_ID + "'and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    print("找质量和陆军单号result", result)
    conn.commit()
    # disconnectMySql(conn, cur)
    return result

# 按装备ID列表从unit表复制数据至disturbplanunit表
def insertIntoDistrubPlanUnitFromList(UnitList):
    # conn,cur = connectMySql()
    equipInfoTuple = selectAllDataAboutEquip()
    disturbplanYearInfoTuple = selectAllDataAboutDisturbPlan()
    for i in UnitList:
        unitInfo = selectUnitInfoByUnitID(i)
        sql = "insert into disturbplanunit select * from unit where Unit_ID = '" + i + "'"
        cur.execute(sql)
        for equipInfo in equipInfoTuple:
            for disturbplanYearInfo in disturbplanYearInfoTuple:
                sql = "insert into disturbplan (Equip_Id,Equip_Name,Unit_Id,Unit_Name,Year,DisturbNum) values " \
                      + "('" + equipInfo[0] + "','" + equipInfo[1] + "','" + i + \
                      "','" + unitInfo[1] + "','" + disturbplanYearInfo[1] + "', '' )"
                cur.execute(sql)

    conn.commit()
    #  disconnectMySql(conn,cur)

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


def selectDisturbPlanChooseUnit():
    # conn, cur = connectMySql()
    sql = "select * from unit where Unit_Uper= '2' or Unit_ID = '3'"
    cur.execute(sql)
    result = cur.fetchall()
    # disconnectMySql(conn, cur)
    if result:
        return result
    else:
        return []



'''
退役报废计划
'''
# 读取分配计划年份
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


# 新增分配计划年份
def insertIntoRetirePlanYear(year):
    #conn, cur = connectMySql()
    EquipList=selectAllDataAboutEquip()
    UnitList=selectAllDataAboutUnit()
    result = selectYearListAboutRetirePlan()
    sql = "insert into retireplanyear (num, year,proof) VALUES" \
          + "('" + str(len(result) + 1) + "', '" + str(year) + "','')"
    #print(sql)
    cur.execute(sql)
    for EquipInfo in EquipList:
        sql = "insert into retireplannote(Equip_id,Equip_Name,Year,Note) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + str(year) +"', '' )"
        cur.execute(sql)
        # sql = "insert into allotschedule (Equip_Id,Equip_Name,army,allotcondition,rocket,finish,year) values " \
        #       + "('" + EquipInfo[0] + "','" + EquipInfo[1] + "', '0','0','0','0','" + str(year) + "' )"
        # cur.execute(sql)
        for UnitInfo in UnitList:
            sql = "insert into retireplan(Equip_id,Equip_Name,Unit_Id,Unit_Name,Year,RetireNum) values " +\
                  "('" + EquipInfo[0] + "','" + EquipInfo[1] + "','" + UnitInfo[0] +\
                    "','" + UnitInfo[1] + "','"+ str(year) +"', '' )"
            cur.execute(sql)

    conn.commit()
    #disconnectMySql(conn, cur)

# 删除分配计划年份
def deleteRetirePlanYear(year):
    #conn, cur = connectMySql()
    sql = "delete from retireplanyear where year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from retireplannote where Year= '" + year + "'"
    cur.execute(sql)
    sql = "delete from retireplan where Year= '" + year + "'"
    cur.execute(sql)
    # sql = "delete from allotschedule where year= '" + year + "'"
    # cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn, cur)

def selectRetirePlanUnitInfoByUnitID(Unit_ID):
    #conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_ID = '" + Unit_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    for info in result:
        #disconnectMySql(conn, cur)
        return info

# 更新分配计划数
def updateRetirePlanNum(Equip_Id,Unit_Id,Year,RetireNum):
    #conn,cur=connectMySql()
    sql="update retireplan set RetireNum='"+ RetireNum + "'where Equip_Id='" + Equip_Id + "'and Unit_Id ='" \
        + Unit_Id + "' and Year = '" + Year + "'"
    #print("===========", sql)
    cur.execute(sql)
    conn.commit()
    #disconnectMySql(conn,cur)

# 更新分配计划备注
def updateRetirePlanNote(Equip_Id,Year,Note):
    #conn,cur=connectMySql()
    sql="update retireplannote set Note='"+ Note + "'where Equip_Id='" + Equip_Id + "' and Year = '" + Year + "'"
    cur.execute(sql)
    conn.commit()
    # disconnectMySql(conn,cur)

# 读取分配计划备注
def selectRetirePlanNote(EquipList, YearList):
    #conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Note from retireplannote where Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        for resultInfo in result:
            resultList.append(resultInfo[0])

    #disconnectMySql(conn, cur)
    return resultList

# 读取分配计划军委计划数与装备单位
def selectRetirePlanOther(EquipList, YearList):
    #conn, cur = connectMySql()
    resultList = []
    for Equip_ID in EquipList.values():
        sql = "select Equip_Unit,Equip_Num from armytransfer where Equip_Id = '" + Equip_ID[0] + "' and year = '" + YearList + "'"
        cur.execute(sql)
        result = cur.fetchall()
        #print("other result",result)
        if result:
            pass
        else:
            resultList.append([])
        for resultInfo in result:
            resultList.append(resultInfo)
    print("Other", resultList)
    #disconnectMySql(conn, cur)
    return resultList

# 按list读取批量分配计划数
def selectRetirePlanNum(UnitList, EquipList, YearList):
    #conn, cur = connectMySql()
    resultList = []
    for Unit_ID in UnitList.values():
        for Equip_ID in EquipList.values():
            sql = "select RetireNum from retireplan where Unit_Id = '" + Unit_ID[0] + \
                  "' and Equip_Id = '" + Equip_ID[0] + "' and Year = '" + YearList + "'"
            cur.execute(sql)
            result = cur.fetchall()
            if len(result)!=0:
                for resultInfo in result:
                    resultList.append(resultInfo[0])
            else:
                resultList.append('-1')
    #disconnectMySql(conn, cur)
    return resultList

def findRetirePlanUnitChildInfo(unitId):
    #conn, cur = connectMySql()
    sql = "select * from disturbplanunit where Unit_Uper = '" + unitId + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # disconnectMySql(conn, cur)
    if result:
        return result
    else:
        return []