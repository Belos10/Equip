from database.connectAndDisSql import *
import operator

def getYearsFromContractOrder():
    result = []
    sql = "select year from contract_order_year  order by year desc "
    years = executeSql(sql)
    if years != None and len(years) != 0:
        for year in years:
            result.append(year[0])
    return result
def getYearsFromContractMaintenance():
    result = []
    sql = "select year from contract_maintenance_year order by year desc "
    years = executeSql(sql)
    if years != None and len(years) != 0:
        for year in years:
            result.append(year[0])
    return result
def isHaveContractOrderYear(year):
    sql = "select * from contract_order_year where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False
def isHaveContractMaintenanceYear(year):
    sql = "select * from contract_maintenance_year where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False
def addContractOrderYear(year):
    sql = "insert into contract_order_year(year) values('%s') "%year
    return executeCommit(sql)

def addContractMaintanceYear(year):
    sql = "insert into contract_maintenance_year(year) values('%s') "%year
    return executeCommit(sql)
def getResult(year,no,name):
    result = []
    if len(no) == 0 and len(name) == 0 :
        result = findAllContractOrderData(year)
        return result
    elif len(no) != 0 or len(name) != 0:
        sql = "select * from contract_order where year = '%s'"%year
        if len(no) != 0:
            sql = sql + " and no like '%%%s%%'" % no
        if len(name) != 0:
            sql = sql + " and name like '%%%s%%'"%name
        sql = sql + " order by id asc"
        result = executeSql(sql)
        return result
def getResultFromContractMaintenance(year,no,name):
    result = []
    if len(no) == 0 and len(name) == 0 :
        result = findAllContractMaintenanceData(year)
        return result
    elif len(no) != 0 or len(name) != 0:
        sql = "select * from contract_maintenance where year = '%s'"%year
        if len(no) != 0:
            sql = sql + " and no like '%%%s%%'" % no
        if len(name) != 0:
            sql = sql + " and name like '%%%s%%'"%name
        sql = sql + " order by id asc"
        result = executeSql(sql)
        return result
#检查合同是否重复
def checkedNo(no):
    result = []
    sql = "select no from contract_maintenance where no = '%s'"%no
    result = executeSql(sql)
    if len(result) < 1:
        return True
    else:
        return False
def findAllContractMaintenanceData(year):
    sql = "select * from contract_maintenance where year = '%s'  order by id asc "%year
    return executeSql(sql)

def findAllContractOrderData(year):
    sql = "select * from contract_order where year = '%s'  order by id asc "%year
    return executeSql(sql)

def insertOneDataInToContractOrder(rowData):
    print(rowData)
    #('2003', '2', '2', '2', '2', 2.0, 2, 4.0, '2000-01-01', '2')
    #['2003', '2', '2', '2', '3', '3', '3', '3', '9.0', '2000-01-01', '3']
    sql = "insert into contract_order(year,no, name,part_A,part_B,unit_price,count,amount,delivery_time,note) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          %(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9])
    return executeCommit(sql)

def insertOneDataInToContractMaintenance(rowData):
    sql = "insert into contract_maintenance(year,no,name,part_A,part_B,unit_price,count,amount,sign_time, delivery_time,note) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          %(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9], rowData[10])
    return executeCommit(sql)

def updataOneDataToContractOrder(rowData):
    print(rowData)
    #['1', '2', '2', '2', '2', '2.0', '2', '4.0', '2000-01-01', '2']
    #[3, 2, '2', '2', '2', '2', 2.0, 3, 6.0, '2000-01-01', '2']
    sql = "update  contract_order set no = '%s',name = '%s', part_A = '%s', part_B = '%s', unit_price = '%s', count = '%s', amount = '%s',delivery_time = '%s', note = '%s' where id = '%s'" \
          %(rowData[1], rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[0])
    print(sql)
    return executeCommit(sql)

def updataOneDataToContractMaintenance(rowData):
    sql = "update  contract_maintenance set no = '%s', name = '%s', part_A = '%s', part_B = '%s', unit_price = '%s', count = '%s', amount = '%s', sign_time = '%s',delivery_time = '%s', note = '%s' where year = '%s' and id = '%s'" \
          %(rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[1],rowData[0])
    return executeCommit(sql)

def deleteDataByContractOrderIdAndYear(id,year):
    sql = "delete from contract_order where id = '%d' and year = '%s'"%(id,year)
    return executeCommit(sql)

def deleteDataByContractMaintenance(id,year):
    print(id,year)
    sqls = []
    sql = "delete from contract_maintenance where id = '%d' and year = '%s'"%(id,year)
    sqls.append(sql)
    sql = "delete from contract_attachment where maintenance_id = '%d' and year = '%s'"%(id,year)
    sqls.append(sql)

    sql = " select  no from  contract_maintenance where id = '%s'"%id
    contratcNo = list(executeSql(sql))
    print(contratcNo)
    if len(contratcNo) > 0:
        sql = "delete from service_support where contract_no = '%s' and  year = '%s'" % (contratcNo[0][0], year)
        sqls.append(sql)
        sql = "delete from contract_sign where contract_no = '%s'"%contratcNo[0][0]
        sqls.append(sql)
    return excuteupdata(sqls)

def deleteAttachmentDataByMaintenance(id,year):
    sql = "delete from contract_attachment where maintenance_id = '%s' and year = '%s'"%(str(id),year)
    return executeCommit(sql)

def getAttachmentInformation(maintenanceId,year):
    sql = "select * from contract_attachment where maintenance_id = '%s' and year = '%s' order by id asc "%(str(maintenanceId),year)
    return executeSql(sql)

def insertOneDataInToContractAttachment(rowData):
    print(rowData)
    sql = "insert into contract_attachment(maintenance_id,id,no,contract_name,plan_project,budget_amount,unit_price,count,amount,payable_amount,signing_date,part_A_unit,unit_property,taxpayer_code,part_B_unit,payer_unit,planning_document,delivery_date,note,year) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          %(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[12],rowData[13],rowData[14],rowData[15],rowData[16],rowData[17],rowData[18],rowData[19])
    return executeCommit(sql)

def updataOneDataToContractAttachment(rowData):
    print(rowData)
    sql = "update  contract_attachment set no = '%s', contract_name = '%s', plan_project = '%s', budget_amount = '%s', unit_price = '%s', count = '%s'," \
          " amount = '%s',payable_amount = '%s', signing_date = '%s', part_A_unit = '%s', unit_property = '%s', taxpayer_code = '%s'," \
          " part_B_unit = '%s', payer_unit = '%s', planning_document = '%s', delivery_date = '%s', note = '%s' where maintenance_id = '%s' and id = '%s' and year = '%s'" \
          %(rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[12],rowData[13],rowData[14],rowData[15],rowData[16],rowData[17],rowData[18],rowData[0],rowData[11],rowData[19])
    return executeCommit(sql)

def deleteDataByContractAttachmentId(maintenanceId,id,year):
    sql = "delete from contract_attachment where maintenance_id = '%d' and id = '%s' and year = '%s'"%(maintenanceId,id,year)
    return executeCommit(sql)


def insertOneDataIntoContractOrder(lineInfo):
    if isHaveContractOrderYear(lineInfo[1]) == False:
        addContractOrderYear(lineInfo[1])
    #(1, '2003', '2', '2', '2', '2', 2.0, 2, 4.0, '2000-01-01', '2')
    sql = "select no from contract_maintenance where no = '%s' "%(lineInfo[2])
    result = executeSql(sql)
    try:
        if result == None or len(result) == 0:
            data = lineInfo[-1]
            insertOneDataInToContractOrder(data)
        else:
            data = []
            data.append(result[0][0])
            for i in range(len(lineInfo)):
                if i == 0 or i == 1:
                    continue
                else:
                    data.append(lineInfo[i])
            updataOneDataToContractOrder(data)
        return True
    except Exception as e:
        print(e)
        raise e


def inputOneDataIntoContractMaintenance(lineInfo):
    if isHaveContractMaintenanceYear(lineInfo[0]) == False:
        addContractOrderYear(lineInfo[0])
    try:
        #['2002', '3', '3', '2', '2', 2.0, 2, 4.0, '2000-01-01', '2', [[]]]
        insertOneDataInToContractMaintenance(lineInfo[0:11])
        lastId = executeSql("select max(id) from contract_maintenance")[0][0]
        print("lastId")
        print(lastId)
        for item in lineInfo[11]:
            if len(item) > 0:
                item.insert(0, lastId)
                insertOneDataInToContractAttachment(item)
        return True
    except Exception as e:
        print(e)
        return False

def getContractMaintenanceInfoByNo(contractNo):
    sql = "select * from contract_maintenance where no = '%s'"%contractNo
    result = list(executeSql(sql))
    print('result',result)
    if len(result) > 0:
        return result[0]
    else:
        return []



if __name__ == '__main__':
    print(getResult('2001','',''))