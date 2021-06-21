
import pymysql
#开户
def open_account(new_name):
    con1 = pymysql.connect(host="localhost", user="root", passwd="", db="bank")
    curson = con1.cursor()
    sql = "insert into bankbase values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    param = [new_name[0], new_name[1], new_name[2], new_name[3][0], new_name[3][1], new_name[3][2], new_name[3][3],
             new_name[4], new_name[5]]
    curson.execute(sql, param)
    con1.commit()
    curson.close()
    con1.close()
#获取所有已经存的数据，并做为names
def select_base():
        con = pymysql.connect(host="localhost", user="root", passwd="", db="bank")
        cursor = con.cursor()
        # 将数据的数据先显示在控制变慢
        sql = "SELECT * FROM bankbase"
        cursor.execute(sql)
        # 提取控制面板上的所有的数据
        names = []
        data = cursor.fetchall()  # 提取查询的所有的数据
        # 将数据库格式的数据转变为names格式的数据
        for i in data:
            sides = (i[3], i[4], i[5], i[6])
            new_name = [i[0], i[1], i[2], sides, i[7], i[8]]
            names.append(new_name)
        con.commit()
        cursor.close()
        con.close()
        return names
def update(account,money):
    con = pymysql.connect(host="localhost", user="root", passwd="", db="bank")
    cursor = con.cursor()
    sql = '''UPDATE bankbase  
             SET money = %s
             WHERE account = %s;'''
    parms = [money,account]
    cursor.execute(sql,parms)
    con.commit()
    cursor.close()
    con.close()







