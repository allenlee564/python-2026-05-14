import csv
import os
from datetime import datetime

catalog = {
    "御飯糰": 35,
    "礦泉水": 20,
    "布丁": 25,
    "關東煮": 15,
    "飯糰": 30,
}

cart = {}
ORDER_DIR = "orders"

try:
    if not os.path.exists(ORDER_DIR):
        os.makedirs(ORDER_DIR)
        print(f"【系統提示】已建立「{ORDER_DIR}」資料夾。")
except Exception as e:
    print(f"【系統錯誤】建立資料夾失敗: {e}")

def display_menu():
    print("\n" + "="*30)
    print(" 歡迎使用便利商店自助結帳系統！")
    print("="*30)
    print("1. 加入商品到購物車")
    print("2. 查看購物車")
    print("3. 移除購物車中的商品")
    print("4. 結帳")
    print("5. 列出訂單")
    print("6. 查看訂單內容")
    print("7. 離開")
    print("="*30)

def add_to_cart():
    print("\n--- 現正販售商品目錄 ---")
    for item, price in catalog.items():
        print(f"• {item}: {price} 元")
    print("-" * 23)
    
    item_name = input("請輸入要加入購物車的商品名稱：").strip()
    
    if item_name in catalog:
        try:
            quantity = int(input("請輸入數量："))
            if quantity > 0:
                if item_name in cart:
                    cart[item_name] += quantity
                else:
                    cart[item_name] = quantity
                print(f"成功！{quantity} 個「{item_name}」已加入購物車。")
            else:
                print("❌ 數量必須大於 0。")
        except ValueError:
            print("❌ 輸入無效！數量請輸入「半形數字」。")
    else:
        print(f"❌ 商品「{item_name}」不存在，請重新確認。")

def view_cart():
    if cart:
        print("\n--- 目前購物車內容 ---")
        total = 0
        for item, quantity in cart.items():
            price = catalog[item]
            subtotal = price * quantity
            total += subtotal
            print(f"• {item} x {quantity} = {subtotal} 元")
        print("-" * 22)
        print(f"💰 總計金額: {total} 元")
    else:
        print("\n🛒 您的購物車目前是空的喔！")

def remove_from_cart():
    if not cart:
        print("\n🛒 購物車是空的，沒有商品可以移除。")
        return

    print("\n--- 目前購物車內容 ---")
    for item, quantity in cart.items():
        print(f"• {item} x {quantity}")
    print("-" * 22)
    
    item_name = input("請輸入要移除的商品名稱：").strip()
    if item_name in cart:
        del cart[item_name]
        print(f"🗑️ 「{item_name}」已成功從購物車移除。")
    else:
        print(f"❌ 「{item_name}」不在您的購物車中。")

def checkout():
    if not cart:
        print("\n❌ 購物車是空的，無法進行結帳。")
        return
        
    total = sum(catalog[item] * quantity for item, quantity in cart.items())
    print(f"\n您的消費總金額為 {total} 元。")
    confirm = input("確認要結帳嗎？(y/n)：").strip().lower()
    
    if confirm == 'y':
        order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        order_file = os.path.join(ORDER_DIR, f"order_{order_id}.csv")
        try:
            with open(order_file, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["商品名稱", "數量", "單價", "小計"])
                for item, quantity in cart.items():
                    price = catalog[item]
                    subtotal = price * quantity
                    writer.writerow([item, quantity, price, subtotal])
                writer.writerow(["總計", "", "", total])
            print(f"🎉 結帳成功！訂單已儲存至: {order_file}")
            cart.clear()  
        except Exception as e:
            print(f"❌ 儲存訂單失敗: {e}")
    else:
        print("已取消結帳，商品仍保留在購物車中。")

def list_orders():
    try:
        orders = [f for f in os.listdir(ORDER_DIR) if f.endswith('.csv')]
        if orders:
            print("\n--- 目前已儲存的訂單檔案 ---")
            for order in orders:
                print(f"📄 {order}")
            print("-" * 28)
        else:
            print("\n📂 目前沒有任何歷史訂單。")
    except Exception as e:
        print(f"❌ 讀取訂單目錄失敗: {e}")

def view_order():
    order_name = input("請輸入要查看的訂單檔案名稱：").strip()
    if order_name and not order_name.endswith('.csv'):
        order_name += '.csv'
        
    order_file = os.path.join(ORDER_DIR, order_name)
    if os.path.exists(order_file):
        try:
            with open(order_file, mode='r', encoding='utf-8-sig', errors='replace') as file:
                reader = csv.reader(file)
                print(f"\n📜 【訂單明細: {order_name}】")
                print("-" * 40)
                for row in reader:
                    print("\t".join(row))
                print("-" * 40)
        except Exception as e:
            print(f"❌ 讀取檔案內容失敗: {e}")
    else:
        print(f"❌ 找不到該訂單檔案「{order_name}」。")

def main():
    while True:
        display_menu()
        choice = input("請輸入操作選項 (1-7)：").strip()
        if choice == '1':
            add_to_cart()
        elif choice == '2':
            view_cart()
        elif choice == '3':
            remove_from_cart()
        elif choice == '4':
            checkout()
        elif choice == '5':
            list_orders()
        elif choice == '6':
            view_order()
        elif choice == '7':
            print("\n感謝您的光臨！祝您有美好的一天，再見！👋")
            break
        else:
            print("❌ 無效選項！請輸入數字 1 到 7。")

if __name__ == "__main__":
    main()
