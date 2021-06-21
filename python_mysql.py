import pymysql
#获取连接
conn = pymysql.connect(host ="localhost",user = "root",passwd = "",db = "bank")
#创建控制台
curson = conn.cursor()
#准备sql语句
#sql = "insert into link values('舒识',25,5000.22,'123456')"
sql = '''CREATE TABLE bankbase
(   
     account    CHAR(8)     NOT NULL,
     name       CHAR(10)    NULL,
     paswword   INT(6)      NULL,
     state      CHAR(10)    NULL,
     province   CHAR(10)    NULL,
     street     CHAR(10)    NULL,
     house_number    CHAR(10)    NULL,
     money      INT        NULL,
     bankname     CHAR(20)  NULL,
     PRIMARY KEY(account)
);'''
#执行sql
curson.execute(sql)
#提交数据到数据库保存
conn.commit()
#关闭资源
curson.close()
conn.close()