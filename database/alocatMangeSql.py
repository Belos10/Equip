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

#查询某年所有的陆军调拨单
def selectArmyTransferByYear(year):
    conn, cur = connectMySql()

    if year == '全部':
        sql = "select * from armytransferyear"
    else:
        sql = "select * from armytransferyear where year = '" + year + "'"

    cur.execute(sql)
    result = cur.fetchall()

    disconnectMySql(conn, cur)
    # 测试结果
    # print(result)

    return result
