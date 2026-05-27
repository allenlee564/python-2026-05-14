import csv
import os
from datetime import datetime

# 起始資料
catalog = {
    "御飯糰": 35,
    "礦泉水": 20,
    "布丁": 25,
    "關東煮": 15,
    "飯糰": 30,
}

cart = {}
ORDER_DIR = "orders"

# 1. 啟動時確認訂單資料夾
try:
    if not os.path.exists(ORDER_DIR):
        os.makedirs(ORDER_DIR)
        print("已建立 orders 資料夾")
except OSError as error:
    print(f"建立資料夾失敗：{error}")

while True:
    print("\n====== 便利商店購物車訂單系統 ======")
    print("1. 顯示商品目錄")
    print("2. 新增商品到購物車")
    print("3. 移除購物車商品")
    print("4. 查看購物車")
    print("5. 結帳並產生 CSV 訂單")
    print("6. 列出訂單檔案")
    print("7. 讀取訂單 CSV")
    print("0. 離開")
    
    choice = input("請選擇：")
    
    # 1. 顯示商品目錄
    if choice == '1':
        print("\n====== 商品目錄 ======")
        for item, price in catalog.items():
            print(f"{item:<6}\t{price} 元")
            
    # 2. 新增商品到購物車
    elif choice == '2':
        item_name = input("請輸入要加入購物車的商品名稱：")
        if item_name in catalog:
            try:
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("數量必須大於 0")
                else:
                    if item_name in cart:
                        cart[item_name] += quantity
                    else:
                        cart[item_name] = quantity
                    print(f"{item_name} 已加入購物車。")
            except ValueError:
                print("數量必須是整數")
        else:
            print("商品不存在，請重新輸入。")
            
    # 3. 移除購物車商品
    elif choice == '3':
        if len(cart) > 0:
            item_name = input("請輸入要移除的商品名稱：")
            if item_name in cart:
                del cart[item_name]
                print(f"{item_name} 已從購物車移除。")
            else:
                print("商品不在購物車中。")
        else:
            print("\n購物車是空的。")
            
    # 4. 查看購物車
    elif choice == '4':
        if len(cart) > 0:
            print("\n====== 購物車 ======")
            total = 0
            for item, quantity in cart.items():
                price = catalog[item]
                subtotal = price * quantity
                total += subtotal
                print(f"{item:<6}\t{price} 元 x {quantity} = {subtotal} 元")
            print("--------------------")
            print(f"總金額：{total} 元")
        else:
            print("\n購物車是空的。")
            
    # 5. 結帳並產生 CSV 訂單
    elif choice == '5':
        if len(cart) == 0:
            print("\n購物車是空的，不可結帳。")
            continue
            
        # 1. 時間戳記
        now = datetime.now()
        order_time_str = now.strftime("%Y%m%d_%H%M%S_%f")
        base_filename = f"order_{order_time_str}"
        filename = f"{base_filename}.csv"
        filepath = os.path.join(ORDER_DIR, filename)
        
        # 2. 自動流水號防呆機制
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base_filename}_{counter}.csv"
            filepath = os.path.join(ORDER_DIR, filename)
            counter += 1
        
        # 計算總金額
        total = sum(catalog[item] * qty for item, qty in cart.items())
        
        # 寫入 CSV 檔案
        try:
            with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["訂單時間", "商品名稱", "單價", "數量", "小計"])
                
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                for item, quantity in cart.items():
                    price = catalog[item]
                    subtotal = price * quantity
                    writer.writerow([current_time, item, price, quantity, subtotal])
                    
                
                writer.writerow(["總計", "", "", "", total])
                    
            print(f"訂單已成功建立：{filepath}")
            cart.clear()  # 結帳成功清空購物車
        except OSError as error:
            print(f"寫入訂單失敗：{error}")
            
    # 6. 列出訂單檔案
    elif choice == '6':
        try:
            files = os.listdir(ORDER_DIR)
            csv_files = [file_name for file_name in files if file_name.endswith(".csv")]
            
            if not csv_files:
                print("目前沒有任何訂單檔案")
            else:
                print("\n====== 訂單檔案清單 ======")
                for file_name in csv_files:
                    print(file_name)
        except OSError as error:
            print(f"讀取訂單資料夾失敗：{error}")
            
    # 7. 讀取指定訂單 CSV 並顯示
    elif choice == '7':
        filename = input("請輸入要查看的訂單檔名 (例如 order_20260527_093015_123456.csv)：")
        filepath = os.path.join(ORDER_DIR, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                print("\n====== 訂單內容 ======")
                for row in reader:
                    print("\t".join(row))
        except FileNotFoundError:
            print("找不到指定的訂單檔案，請確認檔名是否輸入正確（需包含完整檔名與擴充檔名）。")
        except OSError as error:
            print(f"讀取訂單失敗：{error}")
            
    # 0. 離開
    elif choice == '0':
        print("謝謝使用，再見！")
        break
        
    else:
        print("無效的選項，請重新輸入。")
