
from database.connectAndDisSql import *

# 读取年份
from database.contractManagementSql import insertOneDataInToContractMaintenance, updataOneDataToContractMaintenance


def selectYearListAboutServiceSupport():
    yearList = []
    sql = "select year from servicesupportyear "
    cur.execute(sql)
    result = cur.fetchall()
    # print(result)
    for yearInfo in result:
        yearList.append(yearInfo[0])
    return yearList


# 新增年份
def insertIntoServiceSupportYear(year):
    result = selectYearListAboutServiceSupport()
    sql = "insert into servicesupportyear (num, year,proof) VALUES" + "('" + str(len(result) + 1) + "', '" + str(year) + "','')"
    # print(sql)
    cur.execute(sql)
    conn.commit()


# 删除年份
def deleteServiceSupportYear(year):
    sql = "delete from servicesupportyear where year= '" + year + "'"
    cur.execute(sql)
    conn.commit()


# 读取维修保障表格数据内容
def selectContentOfServiceSupport():
    sql = "select * from serviceSupport order by num"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def selectYearContentOfServiceSupport(year):
    sql = "select * from serviceSupport where project_year= '" + year + "'"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows



'''
    功能：
        根据序号删除一行数据
'''
def deleteDataByServiceSupportNum(ServiceSupportNum):
    sql = "delete from serviceSupport where num='%s'" % ServiceSupportNum
    executeCommit(sql)



#num,projectName,compute_agent,price,amount,money,agent_allocation,agent_supply,progress_technology_state,progress_contract,progress_pay,project_year,other
def insertContentOfServiceSupport(data):
    sql = "insert into serviceSupport(num, projectName, compute_agent, price, amount, money,agent_allocation, agent_supply, progress_technology_state, progress_contract, progress_pay, project_year, other)VALUES ('" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + \
          "', '" + data[4] + "', '" + data[5] + "', '" + data[6] + "', '" + data[7] + "', '" \
          + data[8] + "', '" + data[9] + "', '" + data[10] + "', '" + data[11] + "', '" + data[12] + "')"
    # print(sql)
    executeCommit(sql)



# 更新修改过的维修保障表的数据
def updateContentOfServiceSupport(data):
    sql = "update serviceSupport set projectName = '" + data[1] + "', compute_agent = '" + data[2] + "', price = '" + data[3] + "', amount = '" + data[4] + "', money = '" + data[5] + "', agent_allocation = '" + data[6] + "', agent_supply = '" + data[7] + "', progress_technology_state = '" + data[8] + "', progress_contract = '" + data[9] + "', progress_pay = '" + data[10] + "', project_year = '" + data[11] + "', other = '" + data[12] + "' where num = '" + data[0] + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()

def getYearsFromServiceSupportYear():
    result = []
    sql = "select year from servicesupportyear  order by year desc "
    years = executeSql(sql)
    if years != None and len(years) != 0:
        for year in years:
            result.append(year[0])
    return result

def isHaveServiceSupportYear(year):
    sql = "select * from servicesupportyear where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def addServiceSupportYear(year):
    sql = "insert into servicesupportyear(year) values('%s') "%year
    return executeCommit(sql)

def getResult(year,maintanceType):
    result = []
    if maintanceType == '全选':
        result = findAllServiceSupportData(year)
        return result
    elif maintanceType == '装备大修':
        sql = "select * from service_support where type = '%d' and year = '%s' order by  id asc"%(0, year)
    elif maintanceType == '装备中修':
        sql = "select * from service_support where type = '%d' and year = '%s' order by  id asc" %(1, year)
    elif maintanceType == '维修器材购置':
        sql = "select * from service_support where type = '%d' and year = '%s' order by  id asc" %(2, year)
    elif maintanceType == '修理能力建设':
        sql = "select * from service_support where type = '%d' and year = '%s' order by  id asc" %(3,year)
    result = executeSql(sql)
    return result

def findAllServiceSupportData(year):
    sql = "select * from service_support where year = '%s'  order by id asc "%year
    return executeSql(sql)

def getMaintanceContractNos():
    sql = "select no from contract_maintenance "
    data = executeSql(sql)
    if len(data) > 0:
        return data
    else:
        return []

def insertOneDataInToServiceSuppot(rowData):
    print(rowData)
            #[0, '2', '2', '2', '2', '4.0', '2', '2', 0, 0, 'null', 0, '2001', '2']
    sql = "insert into service_support(type, name, unit, price, amount, money, allocation, supply, technology_state, contract, contract_no, paying, year, note) values " \
          "('%d','%s','%s','%s','%s','%s','%s','%s','%d','%d','%s','%d','%s', '%s')" \
          % (rowData[0], rowData[1], rowData[2], rowData[3], rowData[4], rowData[5], rowData[6], rowData[7], rowData[8],
             rowData[9], rowData[10], rowData[11], rowData[12], rowData[13])
    return executeCommit(sql)

def updataOneDataToServiceSuppot(rowData):
    print(rowData)
    #[2, 0, '2', '3', '2.0', '2', '4.0', '2', '2', 0, 0, 'null', 2, '2001', '2']
    sql = "update  service_support set name = '%s', unit = '%s', price = '%s', amount = '%s', money = '%s', allocation = '%s',supply = '%s', technology_state = '%d', contract = '%d', contract_no = '%s',paying = '%d', year = '%s', note = '%s' where id = '%d'" \
          %(rowData[2], rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11], rowData[12], rowData[13], rowData[14], rowData[0])
    return executeCommit(sql)

def deleteDataByServiceSuppotIdAndYear(id,year):
    sql = "delete from service_support where id = '%d' and year = '%s'"%(id,year)
    return executeCommit(sql)

def getMaintanceContractInfo(no):
    sql = "select * from contract_maintenance where no = '%s'"%no
    result = executeSql(sql)
    if len(result) > 0:
        return result[0]
    else:
        return []
def inputOneDataIntoServiceSuppot(lineInfo):
    try:
        if isHaveServiceSuppotYear(lineInfo[-3]) == False:
            addServiceSuppotYear(lineInfo[-3])
        #[2, '0001', '0001', 2.0, 2, 4.0, '0001', '0001', 1, 1, '0001', 1, '2002', '无', ('2002', '0001', '0001', '01', '02', 2.0, 2, 4.0, '2000-01-01', '2')]
        if lineInfo[9] == 1:
            sql = "select id from contract_maintenance where no = '%s' and year = '%s'" % (
            lineInfo[10], lineInfo[-1][0])
            result = executeSql(sql)
            print('oringnal')
            print(result)
            if len(result) == 0:
                print('插入')
                data = list(lineInfo[-1])
                data[-3] = str(data[-3])
                data[-4] = str(data[-4])
                data[-5] = str(data[-5])
                insertOneDataInToContractMaintenance(data)
            else:
                print('更新')
                print(result)
                data = list(lineInfo[-1])
                data.insert(0, result[0][0])
                data[-3] = str(data[-3])
                data[-4] = str(data[-4])
                data[-5] = str(data[-5])
                print(data)
                updataOneDataToContractMaintenance(data)
        insertOneDataInToServiceSuppot(lineInfo[0:-1])
        return True
    except Exception as e:
        print(e)
        raise e

def isHaveServiceSuppotYear(year):
    sql = "select * from service_support_year where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False

def addServiceSuppotYear(year):
    sql = "insert into service_support_year(year) values('%s') "%year
    return executeCommit(sql)






# 读取物资管理表-数据内容
def selectContentOfMaterialManagement():
    sql = "select * from materialManagement order by Number"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def insertContentOfMaterialManagement(data):
    sql = "insert into materialManagement(Number, VoucherNumber, AssetName, ContractNumber, SettlementTime, NumberOfContracts, ContractUnitPrice, ContractAmount, FinancialValuationAccountingQuantity, FinancialValuationAccountingPrice, other, AllocationSituation) VALUES ('" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + \
          "', '" + data[4] + "', '" + data[5] + "', '" + data[6] + "', '" + data[7] + "', '" \
          + data[8] + "', '" + data[9] + "', '" + data[10] + "', '" + data[11] + "')"
    # print(sql)
    return executeCommit(sql)

def updateContentOfMaterialManagement(data):
    sql = "update materialManagement set VoucherNumber = '" + data[1] + "', AssetName = '" + data[2] + "', ContractNumber = '" + data[3] + "', SettlementTime = '" + data[4] + "', NumberOfContracts = '" + data[5] + "', ContractUnitPrice = '" + data[6] + "', ContractAmount = '" + data[7] + "', FinancialValuationAccountingQuantity = '" + data[8] + "', FinancialValuationAccountingPrice = '" + data[9] + "', other = '" + data[10] + "',  AllocationSituation = '" + data[11] + "' where Number = '" + data[0] + "'"
    # print(sql)
    return executeCommit(sql)

def deleteDataByMaterialManagementNum(MaterialManagementNum):
    sql = "delete from MaterialManagement where Number ='%s'" % MaterialManagementNum
    return executeCommit(sql)