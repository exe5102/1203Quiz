from lib import DBcreate, DBimport, DBAll, DBnew, DBedit
from lib import DBTableDelete, DBsearch, check, menu
import sqlite3

DB_NAME = "wanghong.db"

# 建立對檔案型資料庫 wanghong.db 的物件參考
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    Account = input("請輸入帳號：")
    Password = input("請輸入密碼：")

    if check(Account, Password) is False:
        print("=>帳密錯誤，程式結束")
    else:
        while True:
            menu()
            select = input("請輸入您的選擇 [0-7]: ")
            match select:
                case "":
                    break
                case "0":
                    break
                case "1":
                    DBcreate(cursor)
                case "2":
                    DBimport(conn, cursor)
                case "3":
                    DBAll(cursor)
                case "4":
                    DBnew(conn, cursor)
                case "5":
                    name = input("請輸入想修改記錄的姓名: ")
                    if name == "":
                        print("=>必須指定姓名才可修改記錄")
                    else:
                        DBedit(conn, cursor, name)
                case "6":
                    phone = input("請輸入想查詢記錄的手機: ")
                    if phone == "":
                        print("=>必須指定手機才可查詢記錄")
                    else:
                        DBsearch(cursor, "mphone", phone)
                case "7":
                    DBTableDelete(conn, cursor)
                case _:
                    print("=>無效的選擇")
except KeyboardInterrupt:
    print("使用者中斷程式")
except BaseException:
    print("發生預期外的錯誤")
cursor.close()
conn.close()
