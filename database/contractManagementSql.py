from database.connectAndDisSql import *
import operator

def getYearsFromContractOrder():
    sql = "select year from contract_order_year "
    years = executeSql(sql)
    return years[0]

def isHaveContractOrderYear(year):
    sql = "select * from contract_order_year where year ='" + year + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return True
    else:
        return False
def addContractOrderYear(year):
    sql = "insert into contract_order_year(year) values('%s') "%year
    return executeCommit(sql)

def getResult(year,no,name):
    result = []
    if len(no) == 0 and len(name) == 0 :
        result = findAllContractOrderData(year)
        return result
    elif len(no) != 0 or len(name) != 0:
        sql = "select * from contract_order where year = '%s'"%year
        if len(no) != 0:
            sql = sql + " and no = %s" % no
        if len(name) != 0:
            sql = sql + " and name = '%s'"%name
        sql = sql + " order by id asc"
        result = executeSql(sql)
        return result


def findAllContractOrderData(year):
    sql = "select * from contract_order where year = '%s'  order by id asc "%year
    return executeSql(sql)

def insertOneDataInToContractOrder(rowData):
    print(rowData)
    sql = "insert into contract_order(year,id,no,name,part_A,part_B,unit_price,count,amount,note,delivery_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          %(rowData[0],rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[10])
    return executeCommit(sql)

def updataOneDataToContractOrder(rowData):
    print(rowData)
    sql = "update  contract_order set no = '%s', name = '%s', part_A = '%s', part_B = '%s', unit_price = '%s', count = '%s', amount = '%s',delivery_time = '%s', note = '%s' where id = '%s'" \
          %(rowData[1],rowData[2],rowData[3],rowData[4],rowData[5],rowData[6],rowData[7],rowData[8],rowData[9],rowData[0])
    return executeCommit(sql)

def deleteDataByContractOrderId(id):
    print(id)
    sql = "delete from contract_order where id = '%d'"%id
    return executeCommit(sql)

if __name__ == '__main__':
    print(getResult('2001','',''))