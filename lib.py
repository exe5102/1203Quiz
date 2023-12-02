import sqlite3
import json

try:
    with open("pass.json", "r", encoding="UTF-8") as D:
        UserData = json.load(D)
    with open("members.txt", "r", encoding="UTF-8") as f:
        Datalist = [line.strip().split(",") for line in f]
except FileNotFoundError:  # 找不到對象檔案
    print("找不到檔案")
except IOError:  # 檔案讀取錯誤
    print("讀取失敗")
except (EOFError, KeyboardInterrupt):  # 例: ctrl + c
    print("使用者中斷程式")
except BaseException:
    print("發生預期外的錯誤")
else:
    def menu() -> None:  # 完成
        """列印選單"""
        print()
        print("-" * 10 + " 選單 " + "-" * 10)
        print(
            "0 / Enter 離開\n"
            + "1 建立資料庫與資料表\n"
            + "2 匯入資料\n"
            + "3 顯示所有紀錄\n"
            + "4 新增記錄\n"
            + "5 修改記錄\n"
            + "6 查詢指定手機\n"
            + "7 刪除所有記錄\n"
            + "-" * 24
        )

    def check(act: str, pw: str) -> bool:  # 完成
        """json.load() 讀取 JSON 檔案，判斷密碼是否正確"""
        Correct = 0
        for i in range(len(UserData)):
            checkap = act == UserData[i]['帳號'] and pw == UserData[i]['密碼']
            if checkap is True:
                Correct += 1
        return True if Correct == 1 else False

    def DBcreate(cursor: object) -> None:  # 完成
        """建立資料表"""
        try:
            cursor.execute(
                """create table if not exists members
                    (iid INTEGER PRIMARY KEY, mname TEXT NOT NULL,
                    msex TEXT NOT NULL, mphone TEXT UNIQUE NOT NULL)"""
            )
        except sqlite3.Error as error:
            print(f"執行 INSERT 操作時發生錯誤：{error}")
        else:
            print("=>資料庫已建立")

    def DBimport(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        """資料讀取，匯入資料庫"""
        cont = 0
        try:
            for i in range(len(Datalist)):
                cursor.execute(
                    "INSERT OR IGNORE INTO members(mname, msex, mphone)\
                        VALUES (?, ?, ?);",
                    (Datalist[i][0], Datalist[i][1], Datalist[i][2]),
                )
                cont += cursor.rowcount
            conn.commit()

        except sqlite3.Error as error:
            print(f"執行 INSERT 操作時發生錯誤：{error}")
        else:
            print(f"=>異動 {cont} 筆記錄")

    def DBAll(cursor: object) -> None:  # 完成
        """抓取資料庫所有資料"""
        try:
            cursor.execute("SELECT * FROM members")
            data = cursor.fetchall()
        except sqlite3.Error as error:
            print(f"執行 SELECT 操作時發生錯誤：{error}")
        if len(data) > 0:
            print("\n姓名　　　　性別　手機")
            print("-----------------------------")
            for record in data:
                print(f"{record[1]:　<6} {record[2]}　　{record[3]}")
        else:
            print("=>查無資料")

    def DBnew(conn: object, cursor: object) -> None:  # 完成
        """使用者在資料庫中新增資料"""
        mname = input("請輸入姓名: ")
        msex = input("請輸入性別: ")
        mphone = input("請輸入手機: ")
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO members(mname, msex, mphone)\
                        VALUES (?, ?, ?);",
                (mname, msex, mphone),
            )
            conn.commit()
        except sqlite3.Error as error:
            print(f"執行 SELECT 操作時發生錯誤：{error}")
        else:
            print(f"=>異動 {cursor.rowcount} 筆記錄")

    def DBedit(conn: object, cursor: object, name: str) -> None:  # 完成
        """修改資料庫指定資料"""
        msex = input("請輸入要改變的性別: ")
        mphone = input("請輸入要改變的手機: ")
        print("\n原資料：")
        DBsearch(cursor, "mname", name)
        try:
            cursor.execute(
                "UPDATE members SET msex=?, mphone=? WHERE mname=?;",
                (msex, mphone, name)
            )
            conn.commit()
        except sqlite3.Error as error:
            print(f"執行 SELECT 操作時發生錯誤：{error}")
        else:
            print(f"=>異動 {cursor.rowcount} 筆記錄")
        print("修改後資料：")
        DBsearch(cursor, "mname", name)

    def DBsearch(cursor: object, mode: str, data: str) -> None:  # 完成
        """查詢資料庫指定資料"""
        try:
            cursor.execute(f"SELECT * FROM members WHERE {mode}=? ",
                           (data,))
            DBdata = cursor.fetchall()
        except sqlite3.Error as error:
            print(f"執行 SELECT 操作時發生錯誤：{error}")
        if len(DBdata) > 0:
            if mode == "mphone":
                print("姓名　　　　性別　手機")
                print("-----------------------------")
                for record in DBdata:
                    print(f"{record[1]:　<6} {record[2]}　　{record[3]}")
            elif mode == "mname":
                for record in DBdata:
                    print(f"姓名：{record[1]}，性別：{record[2]}，手機：{record[3]}")
        else:
            print("查無資料")

    def DBTableDelete(conn: object, cursor: object) -> None:  # 完成
        """刪除資料表所有資料"""
        try:
            cursor.execute("DELETE FROM  members")
            conn.commit()
        except sqlite3.Error as error:
            print(f"執行 DELETE 操作時發生錯誤：{error}")
        else:
            print(f"=>異動 {cursor.rowcount} 筆記錄")
