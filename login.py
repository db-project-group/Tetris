import tkinter as tk
import time
import pygame
import os
import random
import sqlite3
import easygui as g

db_name = "data.db"

def islogin(iptAct, iptPwd):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        sql = f"select * from User where account = '{iptAct}' and password = '{iptPwd}'"
        cursor.execute(sql)
        if len(cursor.fetchall()) == 0:
            return False
        return True

def login():
    fields = ('使用者名稱：', '密碼：')
    msg = '請輸入使用者名稱和密碼'
    title = '登入'
    tmp = g.multpasswordbox(msg, title, fields)
     
    if tmp == None:
        return "取消登入"
    else:
        iptAct, iptPwd = tmp
        if not islogin(iptAct, iptPwd):
            g.msgbox('密碼錯誤，請重新輸入!', ok_button='確定')
            login()

login()
pygame.quit()