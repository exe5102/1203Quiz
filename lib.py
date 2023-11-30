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
    """json.load() 讀取 JSON 檔案，判斷密碼是否正確"""
    with open("pass.json", "r", encoding="Big5") as f:
        data = json.load(f)
    return True if account == data["帳號"] and password == data["密碼"] else False


def DBcreate() -> None:
    """建立資料表"""
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS members
                            (iid INTEGER PRIMARY KEY, mname TEXT NOT NULL,
                            msex TEXT NOT NULL, mphone TEXT NOT NULL)"""
    )
    cursor.close()
    conn.close()
    print("=>資料庫已建立")


def DBimport() -> None:
    """資料讀取，匯入資料庫"""
    try:
        with open("members.txt", "r", encoding="UTF-8") as f:
            try:
                for data in f:
                    cursor.execute(
                        """INSERT INTO members(iid,msex , mname, mphone)
                        SELECT ?, ?, ? ,?WHERE NOT EXISTS(SELECT 1 FROM members
                        WHERE mname=? AND msex=? AND mphone=?);""",
                        data,
                    )
            except sqlite3.Error as error:
                print(f"執行 INSERT 操作時發生錯誤：{error}")
            except KeyboardInterrupt:
                print("使用者中斷程式")
            else:
                print(f"異動 {cursor.rowcount} 筆記錄")
                cursor.commit()
                cursor.close()
                conn.close()
    except Exception as e:
        print("開檔發生錯誤...")
        print(f"錯誤代碼為：{e.errno}")
        print(f"錯誤訊息為：{e.strerror}")
        print(f"錯誤檔案為：{e.filename}")
    except KeyboardInterrupt:
        print("使用者中斷程式")


def DBAll() -> None:
    """抓取資料庫所有資料"""
    try:
        cursor.execute("SELECT * FROM members")
        data = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
    if len(data) > 0:
        for record in data:
            print(f"{record[0]},{record[1]},{record[2]}")
    cursor.close()
    conn.close()


def DBnew() -> None:
    """使用者在資料庫中新增資料"""
    mname = input("請輸入姓名: ")
    msex = input("請輸入性別: ")
    mphone = input("請輸入手機: ")
    cursor.execute(
        """INSERT INTO members(mname, msex, mphone)
                SELECT ?, ? ,?WHERE NOT EXISTS(SELECT 1 FROM members
                WHERE mname=? AND msex=? AND mphone=?);""",
        (mname, msex, mphone)
    )
    print(f"異動 {cursor.rowcount} 筆記錄")
    cursor.commit()
    cursor.close()
    conn.close()


def DBedit(name: str) -> None:
    '''修改資料庫指定資料'''
    mname = input("請輸入想修改記錄的姓名: ")
    msex = input("請輸入要改變的性別: ")
    mphone = input("請輸入要改變的手機: ")
    DBsearch("mname", name)
    cursor.execute(
        """UPDATE members SET mname=? AND msex= ? AND mphone=?
        WHERE mname=?;""",
        (mname, msex, mphone, name)
    )
    DBsearch("mname", name)
    print(f"異動 {cursor.rowcount} 筆記錄")
    cursor.commit()
    cursor.close()
    conn.close()


def DBsearch(mode: str, data: str) -> None:
    try:
        cursor.execute(f"SELECT * FROM members WHERE {mode}=? ", (mode, data))
        DBdata = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
    if len(DBdata) > 0:
        for record in DBdata:
            print(f"{record[0]},{record[1]},{record[2]}")
    else:
        print("查無資料")

    cursor.close()
    conn.close()


def DBTableDelete():
    try:
        cursor.execute("DELETE FROM  members")
        print(f"異動 {cursor.rowcount} 筆記錄")
        conn.commit()
    except sqlite3.Error as error:
        print(f"執行 DELETE 操作時發生錯誤：{error}")