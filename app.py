from lib import check, menu


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
                print("OK")
            case 2:
                print("OK")
            case 3:
                print("OK")
            case 4:
                print("OK")
            case 5:
                print("OK")
            case 6:
                print("OK")
            case 7:
                print("OK")
            case _:
                print("無效的選擇")

