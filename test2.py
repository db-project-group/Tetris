import sqlite3
db_name = "data.db"
iptAct = "aaa"
iptPwd = "123"

def islogin(iptAct, iptPwd):
    sql = f"select * from User where account = '{iptAct}' and password = '{iptPwd}'"
    cursor.execute(sql)
    if len(cursor.fetchall()) == 0:
        return False
    return True
def login():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # sql = f"select * from User where account = '{iptAct}' and password = '{iptPwd}'"
        if not islogin(iptAct, iptPwd):
            print("Account or Password is wrong!")
        for row in cursor.fetchall():
            act, pwd = row
            print(act, " ", pwd)
login()