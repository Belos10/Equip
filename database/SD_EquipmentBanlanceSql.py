from database.connectAndDisSql import *
tableInformation = {
        '6':{'tableName':'eb_quality_status','fieldName':'issue_new_product'},
        '7':{'tableName':'eb_quality_status','fieldName':'issue_inferior_product'},
        '8': {'tableName': 'eb_quality_status', 'fieldName': 'issue_need_repaired'},
        '9': {'tableName': 'eb_quality_status', 'fieldName': 'issue_need_retire'},
        '10': {'tableName': 'eb_quality_status', 'fieldName': 'report_new_product'},
        '11': {'tableName': 'eb_quality_status', 'fieldName': 'report_inferior_product'},
        '12': {'tableName': 'eb_quality_status', 'fieldName': 'report_need_repaired'},
        '13': {'tableName': 'eb_quality_status', 'fieldName': 'report_need_retire'},
        '14': {'tableName': 'equipment_balance', 'fieldName': 'change_value'},
        '15': {'tableName': 'equipment_balance', 'fieldName': 'existing_value'},
        '16': {'tableName': 'eb_change_project', 'fieldName': 'increase_count'},
        '17': {'tableName': 'eb_change_project', 'fieldName': 'increase_superior_supplement'},
        '18': {'tableName': 'eb_change_project', 'fieldName': 'increase_model_change'},
        '19': {'tableName': 'eb_change_project', 'fieldName': 'increase_missing_reports'},
        '20': {'tableName': 'eb_change_project', 'fieldName': 'increase_self_purchase'},
        '21': {'tableName': 'eb_change_project', 'fieldName': 'increase_transfer_in'},
        '22': {'tableName': 'eb_change_project', 'fieldName': 'increase_other'},
        '23': {'tableName': 'eb_change_project', 'fieldName': 'reduce_count'},
        '24': {'tableName': 'eb_change_project', 'fieldName': 'reduce_model_change'},
        '25': {'tableName': 'eb_change_project', 'fieldName': 'reduce_callout'},
        '26': {'tableName': 'eb_change_project', 'fieldName': 'reduce_train_consumption'},
        '27': {'tableName': 'eb_change_project', 'fieldName': 'reduce_restatement'},
        '28': {'tableName': 'eb_change_project', 'fieldName': 'reduce_retire'},
        '29': {'tableName': 'eb_change_project', 'fieldName': 'reduce_scrap'},
        '30': {'tableName': 'eb_change_project', 'fieldName': 'reduce_other'},
        '31': {'tableName': 'equipment_balance', 'fieldName': 'unprepared_value'},
        '32': {'tableName': 'equipment_balance', 'fieldName': 'unmatched_value'},
        '33': {'tableName': 'equipment_balance', 'fieldName': 'uncutdown_value'},
        '34': {'tableName': 'eb_carry', 'fieldName': 'carry_count'},
        '35': {'tableName': 'eb_carry', 'fieldName': 'carry_new_product'},
        '36': {'tableName': 'eb_carry', 'fieldName': 'carry_inferior_product'},
        '37': {'tableName': 'eb_carry', 'fieldName': 'carry_need_repaired'},
        '38': {'tableName': 'eb_carry', 'fieldName': 'carry_need_retire'},
        '39': {'tableName': 'eb_carry', 'fieldName': 'carry_unprepared_value'},
        '40': {'tableName': 'eb_carry', 'fieldName': 'carryUn_cutdown_value'},
        '41': {'tableName': 'eb_stock', 'fieldName': 'stock_count'},
        '42': {'tableName': 'eb_stock', 'fieldName': 'stock_new_product'},
        '43': {'tableName': 'eb_stock', 'fieldName': 'stock_inferior_product'},
        '44': {'tableName': 'eb_stock', 'fieldName': 'stock_need_repaired'},
        '45': {'tableName': 'eb_stock', 'fieldName': 'stock_need_retire'},
        '46': {'tableName': 'eb_stock', 'fieldName': 'stock_unprepared_value'},
        '47': {'tableName': 'eb_stock', 'fieldName': 'stockUn_cutdown_value'},
        '48': {'tableName': 'eb_management', 'fieldName': 'authorized_rate'},
        '49': {'tableName': 'eb_management', 'fieldName': 'instock_rate'},
        '50': {'tableName': 'eb_management', 'fieldName': 'matched_rate'},
        '51': {'tableName': 'eb_management', 'fieldName': 'prepared_rate'},
        '52': {'tableName': 'eb_management', 'fieldName': 'intact_rate'},
        '53': {'tableName': 'eb_repair_time', 'fieldName': 'never_repair'},
        '54': {'tableName': 'eb_repair_time', 'fieldName': 'once'},
        '55': {'tableName': 'eb_repair_time', 'fieldName': 'twice'},
        '56': {'tableName': 'eb_repair_time', 'fieldName': 'three_times'},
        '57': {'tableName': 'eb_repair_time', 'fieldName': 'More_than_three'},
        '58': {'tableName': 'eb_production_year', 'fieldName': 'before1970'},
        '59': {'tableName': 'eb_production_year', 'fieldName': 'between1971and1975'},
        '60': {'tableName': 'eb_production_year', 'fieldName': 'between1976and1980'},
        '61': {'tableName': 'eb_production_year', 'fieldName': 'between1981and1985'},
        '62': {'tableName': 'eb_production_year', 'fieldName': 'between1986and1990'},
        '63': {'tableName': 'eb_production_year', 'fieldName': 'between1991and1995'},
        '64': {'tableName': 'eb_production_year', 'fieldName': 'between1996and2000'},
        '65': {'tableName': 'eb_production_year', 'fieldName': 'between2001and2005'},
        '66': {'tableName': 'eb_production_year', 'fieldName': 'after2006'}
    }


'''
获取装备平衡表的年份并返回。
'''
def findYear():
    sql = "select year from equipment_balance group by year "
    data = selectData(sql)
    year = []
    print(data)
    if len(data) > 0:
        if data[0][0]:
            pass
        else:
            return year
        for key in range(len(data)):
            if(len(data[key][0]) <= 1):
                continue
            else:
                year.append(data[key][0])

        return tuple(year)


def _dateSaveToList(dataDict):
    newDateList = []
    if dataDict is None or len(dataDict) is 0:
       pass
    else:
        for key in range(len(dataDict)):
            newDateList.append(dataDict[key][0])
    return newDateList




def getResultByYearAndEquipAndUnit(year,equipList,unitList):
    resultList = []
    item = {}
    if equipList is None or unitList is None:
        return resultList
    else:
        for equip in equipList:
            for unit in unitList:
                updateOneEquipmentBalanceData(year, equip, unit)
                resultList.append(getOneEquipmentBalanceDate(year, equip, unit))

        return resultList

def getOneEquipmentBalanceDate(year, equip, unit):
    item = {}
    sql = "select equip_balance_id,Equip_ID from equipment_balance where year=%s and Equip_ID=%s and Unit_ID=%s" % (
    year, equip, unit)
    result = selectOne(sql)
    sql = "select Equip_Name from equip where Equip_ID=%s" % result['Equip_ID']
    item.update(selectOne(sql))
    sql = "select * from equipment_balance where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_quality_status where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_change_project where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_carry where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_stock where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_management where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_repair_time where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    sql = "select * from eb_production_year where equip_balance_id=%s" % result['equip_balance_id']
    item.update(selectOne(sql))
    return item

'''
删除某一年度装备平衡表
'''
def deleteByYear(year):
    sqlFindid = "select equip_balance_id from equipment_balance where year=%s"%year
    data = executeSql(sqlFindid)
    ids = []
    for key in range(len(data)):
        ids.append(data[key][0])
    for id in ids:
        sqlDelete = "delete from eb_quality_status where equip_balance_id=%s"%id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_change_project where equip_balance_id=%s"%id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_carry where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_stock where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_management where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from eb_repair_time where equip_balance_id=%s" % id
        executeCommit(sqlDelete)
        sqlDelete = "delete from equipment_balance where equip_balance_id=%s" % id
        executeCommit(sqlDelete)


#根据分配调整计划更新装备平衡表
def updateOneEquipmentBalanceData(year,equipmentId,unitId):
    item = {}
    item['Equip_ID'] = equipmentId
    item['Unit_ID'] = unitId
    item['OrignalAuthorizedValue'] = 0
    item['authorizedValue'] = 0
    item['authorizedValueIncrease'] = 0
    item['authorizedValueDecrease'] = 0
    item['existingValue'] = 0
    item['originalValue'] = 0
    item['changeValue'] = 0
    item['superiorSupplement'] = 0
    item['retire'] = 0
    item['equipmentBalanceKey'] = str(year) + item['Equip_ID'] + item['Unit_ID']
    item['year'] = str(year)
    # 原有数（originalValue） =  原有实力数    strength（Strength）
    sql = "select Equip_ID,Unit_ID,Work from strength where year=%s and Equip_ID =%s and Unit_ID=%s " % (str(int(year)), equipmentId,unitId)
    workEquipment = selectOne(sql)
    if workEquipment is not None:
        originalValue = int(workEquipment.get('Work', 0))
        item['originalValue'] = originalValue

    # 原有编制数(OrignalAuthorizedValue) = 上一年编制数维护中对应编制数(Work)
    sql = "select Equip_ID,Unit_ID,Work from weave where year=%s and Equip_ID=%s and Unit_ID=%s " % (
    str(int(year) - 1), equipmentId, unitId)
    weaveEquipment = selectOne(sql)
    if weaveEquipment is not None:
        OrignalAuthorizedValue = int(weaveEquipment.get('Work', 0))
        item['OrignalAuthorizedValue'] = OrignalAuthorizedValue

    # 编制数（authorizedValue） = 今年编制数维护的对应编制数（Work）
    sql = "select Equip_ID,Unit_ID,Work from weave where year=%s and Equip_ID=%s and Unit_ID=%s " % (
        str(year), equipmentId, unitId)
    weaveEquipment = selectOne(sql)
    if weaveEquipment is not None:
        authorizedValue = int(weaveEquipment.get('Work', 0))
        item['authorizedValue'] = authorizedValue

    #现有数（existingValue） = 原有数（originalValue）+本年度本单位本装备分配数（DisturbNum）- 退役计划退役数（RetireNum）
    sql = "select Equip_Id,Unit_Id,DisturbNum from disturbplan where Year=%s and Equip_Id=%s and Unit_Id=%s" % (
    str(year), equipmentId, unitId)
    disturbEquipment = selectOne(sql)
    DisturbNum = 0
    if disturbEquipment is not None:
        if (disturbEquipment.get('DisturbNum', 0) == 0 or disturbEquipment['DisturbNum'] is None or len(
                disturbEquipment['DisturbNum']) < 1):
           pass
        else:
            DisturbNum = int(disturbEquipment['DisturbNum'])
        item['superiorSupplement'] = DisturbNum
    sql = "select Equip_Id,Unit_Id,RetireNum from retireplan where Year=%s and Equip_Id=%s and Unit_Id=%s" % (
        str(year), equipmentId, unitId)
    retirePlanEquipment = selectOne(sql)
    RetireNum = 0

    if retirePlanEquipment is not None:
        if (retirePlanEquipment.get('RetireNum', 0) == 0 or retirePlanEquipment['RetireNum'] is None or len(
                retirePlanEquipment['RetireNum']) < 1):
            pass
        else:
            RetireNum = int(retirePlanEquipment['RetireNum'])
        item['retire'] = RetireNum

    item['existingValue'] = item['originalValue'] + DisturbNum - RetireNum

    #编制增（authorizedValueIncrease） =  authorizedValue - OrignalAuthorizedValue
    authorizedValueChange = item['authorizedValue'] - item['OrignalAuthorizedValue']
    if authorizedValueChange >= 0:
        item['authorizedValueIncrease'] = authorizedValueChange
    else:
        item['authorizedValueDecrease'] = authorizedValueChange

    #变化数 = 现有数 - 原有数
    item['changeValue'] = item['existingValue'] - item['originalValue']

    sql = "select equip_balance_id from  equipment_balance where equip_balance_id=%s"%item['equipmentBalanceKey']
    equipmentBalance = selectOne(sql)
    if equipmentBalance is None or equipmentBalance['equip_balance_id'] is None:
        insertOneEquipmentBalanceData(item)
    else:
        alterOneEquipmentBalanceData(item)


def alterOneEquipmentBalanceData(item):
    sqls = []
    sql = "update equipment_balance set original_authorized_value=%d, authorized_value=%d,authorized_value_increase=%d,authorized_value_decrease=%d,original_value=%d,change_value=%d,existing_value=%d where equip_balance_id=%s"\
          %(item['OrignalAuthorizedValue'],item['authorizedValue'],item['authorizedValueIncrease'],item['authorizedValueDecrease'],item['originalValue'],item['changeValue'],item['existingValue'],item['equipmentBalanceKey'])
    sqls.append(sql)
    sql = "update eb_change_project set increase_superior_supplement=%d, reduce_retire=%d where equip_balance_id=%s" \
          % (item['superiorSupplement'], item['retire'], item['equipmentBalanceKey'])
    sqls.append(sql)
    excuteupdata(sqls)

#根据单位Id号删除一天数据
def deleteEquipmentBalanceDataByUnitID(unitId):
    sql = "select equip_balance_id from equipment_balance where Unit_ID='%s'"%unitId
    equipmentbalanceIdList = selectData(sql)
    if equipmentbalanceIdList != None:
        for equipmentbalanceKey in equipmentbalanceIdList:
            sqls = []
            sql = "delete from eb_carry where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_change_project where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_management where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_production_year where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_quality_status where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_repair_time where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_stock where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from equipment_balance where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            excuteupdata(sqls)
    return True

#根据装备Id号删除一天数据
def deleteEquipmentBalanceDataByEquipmentID(equipmentId):
    sql = "select equip_balance_id from equipment_balance where Equip_ID='%s'"%equipmentId
    equipmentbalanceIdList = selectData(sql)
    if equipmentbalanceIdList != None:
        for equipmentbalanceKey in equipmentbalanceIdList:
            sqls = []
            sql = "delete from eb_carry where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_change_project where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_management where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_production_year where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_quality_status where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_repair_time where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from eb_stock where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            sql = "delete from equipment_balance where equip_balance_id=%s" % equipmentbalanceKey[0]
            sqls.append(sql)
            excuteupdata(sqls)
    return True


def deleteOneEquipmentBalanceData(year, equipmentId, unitId):
    sqls = []
    equipKey = str(year) + equipmentId + unitId
    sql = "delete from equipment_balance where equip_balance_id=%s"%equipKey
    sqls.append(sql)
    sql = "delete from eb_carry where equip_balance_id=%s"%equipKey
    sqls.append(sql)
    sql = "delete from eb_change_project where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    sql = "delete from eb_management where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    sql = "delete from eb_production_year where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    sql = "delete from eb_quality_status where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    sql = "delete from eb_repair_time where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    sql = "delete from eb_stock where equip_balance_id=%s" % equipKey
    sqls.append(sql)
    excuteupdata(sqls)


def insertOneEquipmentBalanceData(tempItem):
    sqls = []
    equipKey = tempItem['equipmentBalanceKey']
    year = tempItem['year']
    sql = "insert into equipment_balance(equip_balance_id,Equip_ID,Unit_ID,year,original_authorized_value," \
          "authorized_value,authorized_value_increase,authorized_value_decrease,original_value,change_value,existing_value) values (%s,%s,%s,%s,%d,%d,%d,%d,%d,%d,%d)" % (
              equipKey, tempItem['Equip_ID'], tempItem['Unit_ID'], str(year), tempItem['OrignalAuthorizedValue'],
              tempItem['authorizedValue'], tempItem['authorizedValueIncrease'],tempItem['authorizedValueDecrease'], tempItem['originalValue'],tempItem['changeValue'],tempItem['existingValue'])
    sqls.append(sql)
    sql1 = "insert into eb_carry(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql1)
    sql2 = "insert into eb_change_project(equip_balance_id,increase_superior_supplement,reduce_retire) values(%s,%d,%d)" % (equipKey,tempItem['superiorSupplement'],tempItem['retire'])
    sqls.append(sql2)
    sql3 = "insert into eb_management(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql3)
    sql4 = "insert into eb_production_year(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql4)
    sql5 = "insert into eb_quality_status(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql5)
    sql6 = "insert into eb_repair_time(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql6)
    sql7 = "insert into eb_stock(equip_balance_id) values(%s)" % equipKey
    sqls.append(sql7)
    excuteupdata(sqls)





def getEquipmentIdByName(equipmentName):
    sql = "select Equip_ID from equip where Equip_Name='%s'"%equipmentName
    equipment = selectOne(sql)
    return equipment['Equip_ID']

def getEquipmentBalanceIdByEquipmentIdAndUnitAndYear(equipmentId,unitId,year):
    sql = "select equip_balance_id from equipment_balance where Equip_ID=%s and Unit_ID=%s and year=%s"%(equipmentId,unitId,year)
    data = selectOne(sql)
    if data is None:
        return None
    else:
        return data['equip_balance_id']

def updateOnedata(index,fieldVlaue,equipmentBalanceId):
    insertTableInformation = tableInformation.get(str(index),None)
    if(insertTableInformation is not None):
        sql = "update %s set %s=%s where 'equip_balance_id'=%s"%(insertTableInformation['tableName'],insertTableInformation['fieldName'],fieldVlaue,equipmentBalanceId)
        executeCommit(sql)

def getEquipmentNameByID(equipmentId):
    if equipmentId is None:
        return None
    else:
        sql = "select Equip_Name from equip where Equip_ID=%s"%equipmentId
        data = selectOne(sql)
        if(data is not None):
            return data['Equip_Name']
        else:
            return None




def getEquipmentBalanceIdByEquipmentId(equipmentId,unit,year):
    sql = "select equip_balance_id from equipment_balance where Equip_ID='%s' and Unit_ID='%s'and year='%s'"%(equipmentId,unit,year)
    data = selectOne(sql)
    if data is None:
        return None
    else:
        return data['equip_balance_id']






def saveEquipmentBalanceByRow(dataList,unit,year):
    equipmentBalanceId = getEquipmentBalanceIdByEquipmentId(getEquipmentIdByName(dataList[0]), unit, year)
    if equipmentBalanceId is not None:
        # print(dataList)
        executeCommit("update eb_quality_status set issue_new_product='%s',issue_inferior_product='%s', issue_need_repaired='%s',"
                 "issue_need_retire='%s',report_new_product='%s',report_inferior_product='%s',report_need_repaired='%s',"
                 "report_need_retire='%s' where equip_balance_id='%s' " % (dataList[6],dataList[7],dataList[8],dataList[9],
                                                                       dataList[10],dataList[11],dataList[12],dataList[13],equipmentBalanceId))
        executeCommit("update equipment_balance set change_value='%s',existing_value='%s' where equip_balance_id='%s' " % (
        dataList[14], dataList[15],equipmentBalanceId))
        executeCommit("update eb_change_project set increase_count='%s',increase_superior_supplement='%s',increase_model_change='%s',"
                 "increase_missing_reports='%s',increase_self_purchase='%s',increase_transfer_in='%s',increase_other='%s',reduce_count='%s',"
                 "reduce_model_change='%s',reduce_callout='%s',reduce_train_consumption='%s',reduce_restatement='%s',reduce_retire='%s',"
                 "reduce_scrap='%s',reduce_other='%s' where equip_balance_id='%s' " % (
        dataList[16],dataList[17],dataList[18],dataList[19],dataList[20],dataList[21],dataList[22],dataList[23],dataList[24],dataList[25],
        dataList[26],dataList[27],dataList[28],dataList[29],dataList[30],equipmentBalanceId))
        executeCommit("update equipment_balance set unprepared_value='%s',unmatched_value='%s',uncutdown_value='%s' where equip_balance_id='%s' " % (
        dataList[31],dataList[32],dataList[33], equipmentBalanceId))
        executeCommit("update eb_carry set carry_count='%s',carry_new_product='%s',carry_inferior_product='%s',carry_need_repaired='%s',"
                 "carry_need_retire='%s',carry_unprepared_value='%s',carryUn_cutdown_value='%s' where equip_balance_id='%s' " % (
        dataList[34],dataList[35],dataList[36],dataList[37],dataList[38],dataList[39],dataList[40], equipmentBalanceId))
        executeCommit("update eb_stock set stock_count='%s',stock_new_product='%s',stock_inferior_product='%s',stock_need_repaired='%s',stock_need_retire='%s',"
                 "stock_unprepared_value='%s',stockUn_cutdown_value='%s' where equip_balance_id='%s' " % (
        dataList[41],dataList[42],dataList[43],dataList[44],dataList[45],dataList[46],dataList[47], equipmentBalanceId))
        executeCommit("update eb_management set authorized_rate='%s',instock_rate='%s',matched_rate='%s',prepared_rate='%s',intact_rate='%s' where equip_balance_id='%s' " % (
        dataList[48], dataList[49], dataList[50], dataList[51],dataList[52], equipmentBalanceId))
        executeCommit("update eb_repair_time set never_repair='%s',once='%s',twice='%s',three_times='%s',More_than_three='%s' where equip_balance_id='%s' " % (
        dataList[53],dataList[54],dataList[55],dataList[56],dataList[57], equipmentBalanceId))
        executeCommit(
        "update eb_production_year set before1970='%s',between1971and1975='%s',between1976and1980='%s',between1981and1985='%s',"
        "between1986and1990='%s',between1991and1995='%s',between1996and2000='%s',between2001and2005='%s',after2006='%s' where equip_balance_id='%s' " % (
           dataList[58], dataList[59], dataList[60], dataList[61], dataList[62],dataList[63],dataList[64],dataList[65],dataList[66], equipmentBalanceId))


if __name__ == "__main__":
    EquipID = '5'
    sql = "select equip_balance_id from equipment_balance where Equip_ID='%s'" % EquipID
    equipmentbalanceIdList = selectData(sql)
    print(equipmentbalanceIdList)

    pass

    # deleteOneEquipmentBalanceData('2008','2','5')


