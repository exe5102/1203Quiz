import sqlite3
import json

conn = sqlite3.connect("wanghong.db")
cursor = conn.cursor()


def menu():
    print(
        """
    ---------- 選單 ----------
    0 / Enter 離開
    1 建立資料庫與資料表
    2 匯入資料
    3 顯示所有紀錄
    4 新增記錄
    5 修改記錄
    6 查詢指定手機
    7 刪除所有記錄
    --------------------------"""
    )


def check(account, password: str) -> bool:
    '''json.load() 讀取 JSON 檔案，判斷密碼是否正確'''
    with open("pass.json", "r", encoding="Big5") as f:
        data = json.load(f)
    return True if account == data['帳號'] and password == data['密碼'] else False


def DBcreate() -> None:
    '''建立資料表'''
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS members
                            (iid INTEGER PRIMARY KEY, mname TEXT NOT NULL,
                            msex TEXT NOT NULL, mphone TEXT NOT NULL)"""
    )
    cursor.close()
    conn.close()
    print("=>資料庫已建立")


def DBimport() -> None:
    '''資料讀取，匯入資料庫'''
    with open("members.txt", "r", encoding="UTF-8") as f:
        for line in f:
            cursor.execute(
                """INSERT INTO members (iid, mname, msex, mphone)
                VALUES (?, ?, ?, ?)""", line)
    cursor.close()
    conn.close()


def DBAll() -> None:
    '''抓取資料庫所有資料'''
    cursor.execute('SELECT * FROM members')
    result_all = cursor.fetchall()
    for row in result_all:
        print(f'{row[0]},{row[1]},{row[1]}')
    cursor.close()
    conn.close()


def DBnew(line) -> None:
    '''在資料庫中新增資料'''

    cursor.execute(
                """INSERT INTO members (iid, mname, msex, mphone)
                VALUES (?, ?, ?, ?)""", line)