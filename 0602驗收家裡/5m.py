import pymysql
import random
from datetime import datetime, timedelta

print("🚀 開始連線至 MySQL 並生成 500 萬筆訂單資料...")

# 建立連線（如果你是用 VS Code 遠端 SSH 開檔案，維持 127.0.0.1 即可）
conn = pymysql.connect(
    host='10.1.1.18',
    user='mydba',
    password='Mydba@Pass123',
    database='mydb',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 模擬狀態與日期範圍
statuses = ['COMPLETED', 'PENDING', 'CANCELLED', 'SHIPPED']
start_date = datetime(2023, 1, 1)

# 分批插入優化（5 萬筆塞一次，效能最高）
batch_size = 50000
total_records = 5000000
data_batch = []

try:
    for i in range(1, total_records + 1):
        # 隨機生成符合邏輯的訂單資料
        customer_id = random.randint(1, 50000)      # 假設有 5 萬名客戶
        product_id = random.randint(1, 3)          # 關聯先前建立的 3 筆飲料商品 (1:紅茶, 2:奶茶, 3:綠茶)
        
        # 根據商品給予對應的單價
        if product_id == 1: price = 20.00
        elif product_id == 2: price = 50.00
        else: price = 30.00
        
        quantity = random.randint(1, 10)
        amount = price * quantity
        
        # 隨機分散在 2023 ~ 2025 年之間
        random_days = random.randint(0, 365 * 3 - 1)
        order_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        status = random.choice(statuses)
        
        data_batch.append((customer_id, product_id, order_date, amount, status))
        
        # 達到批次量就寫入一次資料庫，並清空暫存
        if i % batch_size == 0:
            sql = "INSERT INTO orders_large (customer_id, product_id, order_date, amount, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, data_batch)
            conn.commit()
            data_batch = []
            print(f"⏳ 已成功寫入 {i} 筆資料...")

except Exception as e:
    conn.rollback()
    print(f"❌ 發生錯誤: {e}")
finally:
    cursor.close()
    conn