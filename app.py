from lib import DBcreate, DBimport, DBAll, DBnew, DBedit
from lib import DBTableDelete, DBsearch, check, menu


Account = input("請輸入帳號：")
Password = input("請輸入密碼：")

if check(Account, Password) is False:
    print("=>帳密錯誤，程式結束")
else:
    while True:
        menu()
        select = input("請輸入您的選擇 [0-7]: ")
        match select:
            case 0:
                break
            case 1:
                DBcreate()
            case 2:
                DBimport()
            case 3:
                DBAll()
            case 4:
                DBnew()
            case 5:
                name = input("請輸入想修改記錄的姓名: ")
                if name is None:
                    print("=>必須指定姓名才可修改記錄")
                else:
                    DBedit(name)
            case 6:
                phone = input("請輸入想查詢記錄的手機: ")
                if phone is None:
                    print("=>必須指定手機才可查詢記錄")
                else:
                    DBsearch("mphone", phone)
            case 7:
                DBTableDelete()
            case _:
                print("無效的選擇")
