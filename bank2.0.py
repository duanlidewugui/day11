#首先，如果是第一次运行该代码，请在mysql中运行下行语句（请不要有bank数据库）
#          CREATE DATABASE bank CHARACTER SET utf8;
#运行完上一行代码后，再运行 python_mysql.py 这个代码文件，建立列表bankbase，后续的代码运行，就不再需要以上准备
#注意，数据库的用户名称和密码可能不一致，请自行更改python_mysql.py 第3行代码
#       new_base.py的第五行，第17行，第37行代码
# 2021/6/21 17:43 舒识

#运行该代码前，请确保new_base.py 代码和该代码在一个包（Package）下

#用于添加用户，会返回一个 列表，列表中有一个用户的
# 账号（int：系统随机产生8位数字）、姓名(str)、密码(int:6位数字)、
# 地址、存款余额(int)、开户行（银行的名称（str））六项数据

#录入地址 ，state（国家），province（省份），street（街道），house_number(门牌号）
from random import Random, random
import pymysql
from new_base import open_account,select_base,update

def set_site():
    state = input("请输入您所在的国家")
    province = input("请输入您所在的省份")
    street = input("请输入您所在的街道")
    house_number = input("请输入您的门牌号")
    site = (state,province,street,house_number)
    return site


#添加新用户，需要输入 name（用户名），password(密码)，site(地址)（地址是一个元祖),
#还有过去存放所有用户的二维列表 names
#还需要添加随机账号，为o的存款，开户行，顺序为[随机账号,用户名,密码,地址,余额,开户行]
#返回添加了用户的names
#返回3代表用户已满，添加失败
#返回2代表用户名已存在，添加失败
#返回0 代表用户已添加成功，存款为0，开户行为昌平行
def random_number():
    dom = ['0','1','2','3','4','5','6','7','8','9','q',
           'w','e','r','t','y','u','i','o','p','a','s',
           'd','f','g','h','j','k','l','z','x','c','v',
           'b','n','m']
    i=0
    num =''
    while i<8:
        a = int(random()*35)
        num=num+dom[a]
        i+=1
    return num

def new_user(name,password,site,names):
    #检测names是否已满，满了就返回3
    if len(names) >= 100:
        print("添加失败，用户库已满")
        return 3
    #这个while循环确定随机数不会重复
    while True:
        key_uesr = 0
        account_number = random_number()
        #if len(names) == 0:
        #    break
        for a,b,c,d,e,f in names:
            if account_number == a:
                key_uesr = 1
                break

        if key_uesr == 1:
            continue
        if key_uesr == 0:
            break
    for a,b,c,d,e,f in names:
        if b == name:
            print("添加失败，用户名已存在")
            return 2
    new_name = [account_number,name,password,site,0,"中国工商银行北京昌平支行"]
    open_account(new_name)
    names.append(new_name)
    return 0

#存钱需要先输入账号，还有要存的钱的多少
#若存钱失败会返回1，成功会返回0,并将钱直接就存了

def save_money (number,money,names):
    i = 0
    if len(names) == 0:
        print("目前银行没有注册账户，请添加账户后再来存款")
        return False
    while i < len(names):
        if number == names[i][0] :
            names[i][4] = names[i][4]+money
            update(number,names[i][4])
            print("存款成功")
            return 0
        i += 1
    print("存款失败，不存在的账户或密码，请查询是否输入有误")
    return 1

#取款，输入正确的账号和密码即能进入，还需要要money
#需要输入账号，输入密码
#若账号不对，会返回1,密码不对，返回2
#取款成功，会返回0
#若金钱不够，返回3
#金钱要在输入前进行判断，不能等于小于0
def draw_money (number,password,money,names):
    i = 0
    if len(names) == 0:
        print("目前银行没有注册账户，请添加账户后再来取款")
        return 1
    while i < len(names):
        if number == names[i][0] :
            if password != names[i][2]:
                print("取款账户密码不对")
                return 2
            if names[i][4] == 0:
                print("您的账户余额为0，无法取款")
                return 3
            if names[i][4] < money:
                print("您的余额为", names[i][4])
                print("您的余额不足，无法取款")
                return 3
            names[i][4] = names[i][4] - money
            update(number,names[i][4])
            print("取款成功")
            return 0
        i +=1

    print("取款失败，不存在的账户或密码，请查询是否输入有误")
    return 1
#需要转钱给对面的账户1 number1，存钱的账号1
#需要有钱可转的账户2 number2,还有账户2的密码password，取钱的账号2
#同时需要输入多少的金钱 money
#还需要整个银行数据
#转账成功返回0,失败返回1

def transfer_accounts(number1,number2,password,money,names):
    key = draw_money(number2,password,money,names)
    if key == 0 :
        key1 = save_money(number1, money, names)
        if key1 == 0:
            print("转账成功")
            return 0
        if key1 == 1:
            print("转账失败")
            #这里把账号2取走的钱还回去
            save_money(number2, money, names)
            return 1
#需要输入账号，账号密码，还有names
#查询成功返回0，失败返回1
def inquire(number,password,names):
    if len(names) == 0:
        print("查询失败，目前账户数量为0")
        return 1
    i = 0
    while i < len(names):
        if number == names[i][0]:
            if password == names[i][2]:
                print("当前账号", names[i][0])
                print("当前用户名", names[i][1])
                print("当前密码", names[i][2])
                print("当前地址", names[i][3])
                print("当前余额", names[i][4])
                print("开户行", names[i][5])
                return 0
            else:
                print("密码不匹配")
                return 1
        i+=1
    print("账户不存在，请查询是否输入错误")
    return 1
#只要用这个方法，就能显示界面
def inface():
    print("**********************************")
    print("**\t\t\t中国工商银行\t\t\t**")
    print("**\t\t\t账户管理系统\t\t\t**")
    print("**********************************")
    print("**\t1.开户\t\t\t\t\t\t**")
    print("**\t2.存钱\t\t\t\t\t\t**")
    print("**\t3.取钱\t\t\t\t\t\t**")
    print("**\t4.转账\t\t\t\t\t\t**")
    print("**\t5.查询\t\t\t\t\t\t**")
    print("**\t6.退出\t\t\t\t\t\t**")
    print("**********************************")



#开始main


while True:
    names = select_base()
    print(names)
    key2 = 0
    inface()
    key2 = int(input("请输入要进入的界面"))


    if key2 == 1:
        while True:
            name = input("请输入您的用户名")
            password = int(input("请输入您的六位密码"))
            if password > 1000000 or password <100000:
                print("密码格式不规范")
                break
            site = set_site()
            new = new_user(name, password, site, names)
            if new == 0:

                print("添加用户成功")
                l = len(names)
                print("您的账号为",names[l-1][0],"请牢记您的账号")
                input("输入任意数字将返回主页面")
                break
            else:
                print("添加失败，将返回主页面")
                break
#存钱
    if key2 == 2:
        while True:
            number = input("请输入八位账号")
            money = int(input("请输入您想存的金额"))
            sa = save_money(number,money,names)
            if sa == 0:
                print("存款成功，即将返回主页面")
                break
            else:
                print("存款失败，即将返回主页面")
                break
#取钱
    if key2 == 3:
        while True:
            number = input("请输入八位账号")
            password = int(input("请输入六位密码"))
            money = int(input("请输入要取的钱"))
            if money <= 0:
                print("要取的钱不能是负数，即将重新输入")
                continue
            dr = draw_money(number, password, money, names)
            if dr == 0:
                print("取款成功，将返回主页面")
                break
            else:
                print("取款失败，即将返回主页面")
#转账
    if key2 == 4:
        while True:
            number1 = input("请输入会收到钱的八位账号")
            number2 = input("请输入您的八位账号")
            password = int(input("请输入您的六位密码"))
            money = int(input("请输入您要转账的钱的数量"))
            if money <= 0:
                print("转账的金额不能小于等于0")
                continue
            tr = transfer_accounts(number1,number2,password,money,names)
            if tr == 0:
                print("转账成功，返回主页面")
                break
            else:
                print("转账失败，返回主页面")
                break
#查询
    if key2 == 5:
        while True:
            number = input("请输入要查询的八位账号")
            password = int(input("请输入查询账号的六位密码"))
            inq = inquire(number,password,names)
            if inq == 0:
                print("查询成功，随机输入数字返回主页面")
                input()
                break
            else:
                print("查询失败，随机输入数字返回主页面")
                input()
                break
    if key2 == 6:
        print("感谢您的光临，欢迎下次再来")
        break
