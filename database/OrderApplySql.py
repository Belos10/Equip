from database.connectAndDisSql import *
import operator
# 删除订购申请表表所有年份
def clearOrderApply():
    sql = "delete from order_apply_year "
    # print(sql)
    cur.execute(sql)
    sql = "delete from order_apply "
    # print(sql)
    cur.execute(sql)
    conn.commit()

# 删除某个订购申请某个年份
def deleteOrderApplyYearByYear(year):

    sql = "delete from order_apply_year where year = '" + year + "'"
    # print(sql)
    cur.execute(sql)

    sql = "delete from order_apply where year = '" + year + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()

#查询年份表
def selectAllOrderApplyYearInfo():
    sql = "select * from order_apply_year "
    years = executeSql(sql)
    if years != None and len(years) != 0:
        return years
    else:
        return []

# 退役年份表中添加年份
def insertIntoOrderApplyYear(year):
    sql = "insert into order_apply_year values ('%s')"%year
    return executeCommit(sql)


def isHaveOrderApplyRecord(UnitID, EquipID, year):
    sql = "select * from order_apply where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"
    #print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


# 查询编制信息
def selectWeaveInfo(UnitID, EquipID, year):
    sql = "select * from weave where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + UnitID + "' and year = '" + year + "'"

    cur.execute(sql)
    result = cur.fetchall()
    return result

# 查询实力信息
def selectStrengthInfo(unitID, EquipID, year):
    sql = "select * from strength where Equip_ID = '" + \
          EquipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    return result

# 查询前更新退休表
def selectUpdateIntoOrderApply(unitID, EquipID, year):
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
    sql = "update order_apply set strenth='%s', weave='%s',now='%s' where Equip_ID='%s' and Unit_ID='%s' and year='%s'"%(strength, weave, now, EquipID, unitID, year)
    cur.execute(sql)

# 查询退休信息
def selectInfoFromOrderApply(unitID, equipID, year):
    sql = "select * from order_apply where Equip_ID = '" + \
          equipID + "' and Unit_ID = '" + unitID + "' and year = '" + year + "'"

    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return list(result[0])
    else:
        return ''
def selectEquipInfoByEquipID(EquipID):
    sql = "select * from equip where Equip_ID = '" + \
          EquipID + "'"

    cur.execute(sql)
    result = cur.fetchall()
    return result

# 查看某装备是否有子装备
def selectEquipIsHaveChild(Equip_ID):
    sql = "select * from equip where Equip_Uper = '" + Equip_ID + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

# 查询退休表
def selectAboutOrderApplyByEquipAndUnit(UnitList, EquipList, year):
    unitID = UnitList[0]
    result = []
    for EquipID in EquipList:
        m_isHaveRecord = isHaveOrderApplyRecord(unitID, EquipID, year)
        if m_isHaveRecord:
            selectUpdateIntoOrderApply(unitID, EquipID, year)
            currentResultInfo = selectInfoFromOrderApply(unitID, EquipID, year)
            result.append(currentResultInfo)
        else:
            currentResultInfo = []
            weaveInfo = selectWeaveInfo(unitID, EquipID, year)
            strengthInfo = selectStrengthInfo(unitID, EquipID, year)
            ID = unitID + EquipID + year
            equipInfo = selectEquipInfoByEquipID(EquipID)
            from database.SD_EquipmentBanlanceSql import getFomatEquipmentName
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
            apply = ''
            other = ''
            haveChild = selectEquipIsHaveChild(EquipID)
            insertIntoOrderApply(ID, unitID, EquipID, equipName, equipUnit, strength,weave, num, now, apply, other, year)
            currentResultInfo = [ID, unitID, EquipID, equipName, equipUnit,weave, strength, num, now, apply, other, year]
            result.append(currentResultInfo)
    return result

# 插入退休表
def insertIntoOrderApply(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,strength,Weave, Num, Now, Apply, Other, year):
    sql = "insert into order_apply (id, Unit_ID, Equip_ID, Equip_Name, Equip_Unit, strenth, weave, plan_num, now, apply_num, note, year) " \
          "VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(ID, Unit_ID, EquipID, Equip_Name,Equip_Unit,strength,Weave, Num, Now, Apply, Other, year)
    #print(sql)
    cur.execute(sql)

# 判断是否为倒数第二级目录
def isSecondDict(EquipID):
    selfHaveChild = selectEquipIsHaveChild(EquipID)
    if selfHaveChild:
        from database.strengthDisturbSql import selectChildEquip
        child = selectChildEquip(EquipID)[0][0]
        selfHaveChild = selectEquipIsHaveChild(child)
        if selfHaveChild:
            return False
        else:
            return True
    else:
        return False

# 更新退休表
def updateOrderApply(num, apply, other, orginInfo):
    if orginInfo:
        sql = "update order_apply set plan_num = '" + num + "', apply_num = '" + apply + "', note = '" + other +\
              "' where Equip_ID = '" + orginInfo[2] + "' and Unit_ID = '" + orginInfo[1] + "' and year = '" + orginInfo[11] + "'"
    else:
        return
    cur.execute(sql)
    conn.commit()

