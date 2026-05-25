import pymysql
import random
import time
from datetime import datetime, timedelta



# 資料庫連線設定
DB_CONFIG = {
    'host': '10.167.223.51',
    'port': 3306,
    'user': 'alice',
    'password': '12345678',  # 請修改為您的密碼
    'database': 'ecommerce_db',
    'charset': 'utf8mb4'
}

def generate_fake_data(num_rows=1000000):
    print(f"正在連線至資料庫... 準備生成 {num_rows} 筆資料")
    
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. 重建表結構 (確保乾淨環境)
        print("重建 audit_logs 資料表...")
        cursor.execute("DROP TABLE IF EXISTS audit_logs")
        cursor.execute("""
            CREATE TABLE audit_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(50) NOT NULL,
                create_time DATETIME NOT NULL,
                description VARCHAR(255)
            )
        """)
        conn.commit()
        
        # 2. 準備數據
        print("正在生成記憶體中的假資料...")
        batch_size = 5000  # 每次寫入 5000 筆，避免記憶體爆掉
        actions = ['LOGIN', 'LOGOUT', 'PURCHASE', 'VIEW', 'ADD_CART']
        
        data_buffer = []
        total_inserted = 0
        
        start_time = datetime.now()
        
        for i in range(num_rows):
            user_id = random.randint(1, 1000)
            action = random.choice(actions)
            # 隨機產生過去三年內的時間
            time_offset = random.randint(0, 365* 3 * 24 * 60 * 60)
            create_time = datetime.now() - timedelta(seconds=time_offset)
            desc = f"User {user_id} performed {action}"
            
            # 將資料加入緩衝區 (Tuple 格式)
            data_buffer.append((user_id, action, create_time, desc))
            
            # 當緩衝區滿了，執行批量寫入
            if len(data_buffer) >= batch_size:
                cursor.executemany("""
                    INSERT INTO audit_logs (user_id, action, create_time, description)
                    VALUES (%s, %s, %s, %s)
                """, data_buffer)
                conn.commit()
                total_inserted += len(data_buffer)
                print(f"已寫入: {total_inserted}/{num_rows}")
                data_buffer = [] # 清空緩衝區

        # 寫入剩下的資料
        if data_buffer:
            cursor.executemany("""
                INSERT INTO audit_logs (user_id, action, create_time, description)
                VALUES (%s, %s, %s, %s)
            """, data_buffer)
            conn.commit()
            
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ 完成！共寫入 {num_rows} 筆資料。")
        print(f"總耗時: {duration:.2f} 秒 (平均每秒 {num_rows/duration:.0f} 筆)")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_fake_data()


