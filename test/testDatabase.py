import pymysql

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', port=3306, user='root', password="123456", db="test")
    cur = conn.cursor()
    sql = "select * from dept where Dept_ID=1"
    cur.execute(sql)
    print(cur.fetchone())