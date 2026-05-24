import csv

# 商品目錄
catalog = {
    "御飯糰": 35,
    "礦泉水": 20,
    "布丁": 25,
    "關東煮": 15,
    "飯糰": 30,
}

# 購物車與訂單紀錄
cart = {}
order_list = []  # 用列表來記錄結帳後的 CSV 檔名

while True:
    # 顯示主選單
    print("\n歡迎使用便利商店自助結帳系統！")
    print("1. 加入商品到購物車")
    print("2. 查看購物車")
    print("3. 移除購物車中的商品")
    print("4. 結帳")
    print("5. 列出訂單")
    print("6. 查看訂單內容")
    print("7. 離開")
    
    choice = input("請輸入選項 (1-7)：")
    
    # 1. 加入商品
    if choice == '1':
        print("\n商品目錄：")
        for item in catalog:
            print(item, ":", catalog[item], "元")
            
        item_name = input("請輸入要加入購物車的商品名稱：")
        if item_name in catalog:
            quantity = int(input("請輸入數量："))
            if item_name in cart:
                cart[item_name] = cart[item_name] + quantity
            else:
                cart[item_name] = quantity
            print(item_name, "已加入購物車。")
        else:
            print("商品不存在，請重新輸入。")
            
    # 2. 查看購物車
    elif choice == '2':
        if len(cart) > 0:
            print("\n購物車內容：")
            total = 0
            for item in cart:
                price = catalog[item]
                quantity = cart[item]
                subtotal = price * quantity
                total = total + subtotal
                print(item, "x", quantity, "=", subtotal, "元")
            print("總計:", total, "元")
        else:
            print("\n購物車是空的。")
            
    # 3. 移除商品
    elif choice == '3':
        if len(cart) > 0:
            item_name = input("請輸入要移除的商品名稱：")
            if item_name in cart:
                del cart[item_name]
                print(item_name, "已從購物車移除。")
            else:
                print("商品不在購物車中。")
        else:
            print("\n購物車是空的。")
            
    # 4. 結帳
    elif choice == '4':
        if len(cart) > 0:
            total = 0
            for item in cart:
                total = total + catalog[item] * cart[item]
            print("\n您的總計是", total, "元。")
            
            confirm = input("是否要結帳？(y/n)：")
            if confirm == 'y' or confirm == 'Y':
                # 讓使用者自己輸入訂單編號，最符合新手的做法
                order_id = input("請輸入今天日期作為訂單編號 (例如 20260525)：")
                filename = "order_" + order_id + ".csv"
                
                # 寫入 CSV 檔案
                with open(filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["商品名稱", "數量", "單價", "小計"])
                    for item in cart:
                        price = catalog[item]
                        quantity = cart[item]
                        subtotal = price * quantity
                        writer.writerow([item, quantity, price, subtotal])
                    writer.writerow(["總計", "", "", total])
                
                print("訂單已儲存為", filename)
                order_list.append(filename)  # 把檔名記下來，等一下功能5要用
                cart.clear()  # 清空購物車
            else:
                print("結帳已取消。")
        else:
            print("\n購物車是空的，無法結帳。")
            
    # 5. 列出訂單
    elif choice == '5':
        if len(order_list) > 0:
            print("\n目前的訂單：")
            for order in order_list:
                print(order)
        else:
            print("\n目前沒有訂單紀錄。")
            
    # 6. 查看訂單內容
    elif choice == '6':
        filename = input("請輸入要查看的訂單檔案名稱 (例如 order_20260525.csv)：")
        # 直接嘗試打開，不寫複雜的 os.path.exists
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                print("\n訂單內容：")
                for row in reader:
                    print(row[0], "\t", row[1], "\t", row[2], "\t", row[3])
        except:
            print("找不到該訂單檔案，請重新輸入。")
            
    # 7. 離開
    elif choice == '7':
        print("謝謝使用，再見！")
        break
        
    else:
        print("無效的選項，請重新輸入。")
