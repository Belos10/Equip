import pymysql
from database.connectAndDisSql import *

# 读取年份
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
    sql = "insert into serviceSupport(num, projectName, compute_agent, price, amount, money," \
          "agent_allocation, agent_supply, progress_technology_state, progress_contract, progress_pay, project_year, other)" \
          "VALUES ('" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + \
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