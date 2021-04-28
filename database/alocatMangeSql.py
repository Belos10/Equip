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
        sql = "select * from armytransfer"
    else:
        sql = "select * from armytransfer where year = '" + year + "'"

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
    print(sql)
    cur.execute(sql)
    conn.commit()
    disconnectMySql(conn, cur)