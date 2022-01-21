from database.connectAndDisSql import *
def getResult(contactNo, bureauName):
    if len(contactNo) == 0 and len(bureauName) == 0:
        result = getAllContractSigningDate()
        return result
    elif len(contactNo) > 0:
        sql = "select * from contract_sign where contract_no like '%%%s%%'" %contactNo
    else:
        sql = "select * from contract_sign where bureau_name like '%%%s%%'"%bureauName
    # print(sql)
    result = list(executeSql(sql))
    # print('result', result)
    return result


def getAllContractSigningDate():
    sql = "select * from contract_sign order by id asc "
    return list(executeSql(sql))

def getAllocationByContractNo(contractNo):
    sql = "select allocation from service_support where contract_no = '%s'"%contractNo
    return list(executeSql(sql))

def getBureauNamesFromAgentRoom():
    sql = "select bureau_name from agent_room group by bureau_name"
    return list(executeSql(sql))

def getAgentNamesAndIds(bureauName):
    sql = "select id,agent_name from agent_room where bureau_name = '%s'"%bureauName
    print(sql)
    result = list(executeSql(sql))
    ids = []
    names = []
    if len(result) > 0:
        for i in range(len(result)):
            ids.append(result[i][0])
            names.append(result[i][1])
    return ids, names

def getContractNos():
    sql = "select no from contract_maintenance"
    result = list(executeSql(sql))
    nos = []
    if len(result) > 0:
        for i in range(len(result)):
            nos.append(result[i][0])
    return nos

def insertOneDataIntContactSign(rowData):
    sql = "insert into contract_sign(bureau_name, agent_name, agent_id, contract_no, price_reply, price_contract, work_basis, price_progress, plan_basis, overall_progress, plan_annual, " \
          " count_plan, count_detail, plan_price_unit, plan_price_count, offer_unit, offer_count, paid_amount, due_amount, current_progress, storage, dial_order, complete_assembly, note) " \
          "values ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          %(rowData[0], rowData[1],str(rowData[2]),rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10],rowData[11],rowData[12],rowData[13],rowData[14],
            rowData[15],rowData[16],rowData[17],rowData[18],rowData[19],str(rowData[20]),str(rowData[21]),str(rowData[22]),rowData[23])
    return executeCommit(sql)

def updataOneDataIntoContractSign(rowData):
    print("rowDate")
    print(rowData)
    sql = "update contract_sign  set bureau_name = '%s',  agent_name = '%s',  agent_id = '%d',  contract_no = '%s',  price_reply = '%s',  price_contract = '%s'," \
          "  work_basis = '%s',  price_progress = '%s',  plan_basis = '%s',  overall_progress = '%s', plan_annual = '%s', " \
          "  count_plan = '%s',  count_detail = '%s',  plan_price_unit = '%s',  plan_price_count = '%s',  offer_unit = '%s',  offer_count = '%s',  paid_amount = '%s'," \
          "  due_amount = '%s',   current_progress = '%s',  storage = '%d',  dial_order = '%d',  complete_assembly = '%d',  note = '%s' where id = '%d' " \
          % (rowData[1], rowData[2], rowData[3], rowData[4], rowData[5], rowData[6], rowData[7], rowData[8],
             rowData[9], rowData[10], rowData[11], rowData[12], rowData[13], rowData[14],
             rowData[15], rowData[16], rowData[17], rowData[18], rowData[19], rowData[20], rowData[21],
             rowData[22], rowData[23],rowData[24],rowData[0])
    print(sql)
    return executeCommit(sql)

def deleteDataByContractSignId(id):
    sql = "delete from contract_sign where id = '%d'"%id
    return executeCommit(sql)