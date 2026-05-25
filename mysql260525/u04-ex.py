import pymysql
import random
import time
from datetime import datetime, timedelta
from faker import Faker

"""
單元四：百萬級數據生成腳本
功能：
1. 自動建立分區表 (orders_partitioned)。
2. 使用 Faker 生成真實感數據。
3. 批量寫入 100 萬筆資料。
"""

# 資料庫連線設定
DB_CONFIG = {
    'host': '10.167.223.51',
    'port': 3306,
    'user': 'alice',
    'password': '12345678',  # 請修改為您的密碼
    'database': 'ecommerce_db',
    'charset': 'utf8mb4'
}

# 初始化 Faker
fake = Faker()

def create_partitioned_table(cursor):
    print("正在建立分區表 orders_partitioned...")
    cursor.execute("DROP TABLE IF EXISTS orders_partitioned")
    sql = """
    CREATE TABLE orders_partitioned (
        id INT AUTO_INCREMENT,
        customer_name VARCHAR(50),
        amount DECIMAL(10, 2),
        order_date DATETIME NOT NULL,
        address VARCHAR(100),
        PRIMARY KEY (id, order_date) -- 注意：分區鍵必須包含在主鍵內
    )
    PARTITION BY RANGE (YEAR(order_date)) (
        PARTITION p2023 VALUES LESS THAN (2024),
        PARTITION p2024 VALUES LESS THAN (2025),
        PARTITION p2025 VALUES LESS THAN (2026),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );
    """
    cursor.execute(sql)

def generate_data(total_rows=1000000):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # === 階段 1: 建立資料表 ===
        table_start = time.time()
        create_partitioned_table(cursor)
        conn.commit()
        table_time = time.time() - table_start
        print(f"✓ 資料表建立完成 ({table_time:.2f} 秒)")
        
        # === 階段 2: 預先生成樣本資料 (關鍵優化!) ===
        print("\n正在預先生成樣本資料...")
        sample_start = time.time()
        sample_size = 1000
        name_samples = [fake.name() for _ in range(sample_size)]
        address_samples = [fake.address().replace('\n', ', ')[:100] for _ in range(sample_size)]
        sample_time = time.time() - sample_start
        print(f"✓ 樣本生成完成 ({sample_time:.2f} 秒)")
        
        print(f"\n開始生成 {total_rows:,} 筆資料...")
        print("=" * 60)
        
        # 優化設定
        cursor.execute("SET autocommit=0")
        cursor.execute("SET unique_checks=0")
        cursor.execute("SET foreign_key_checks=0")
        
        batch_size = 10000  # 大幅增加批次大小
        buffer = []
        total_start = time.time()
        
        # 設定日期範圍 (2023-01-01 到 2025-12-31)
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2025, 12, 31)
        total_days = (end_date - start_date).days
        
        # 計時變數
        last_report_time = time.time()
        last_report_count = 0
        
        for i in range(total_rows):
            # 從樣本中隨機選取 (比呼叫 Faker 快 100 倍以上)
            random_days = random.randint(0, total_days)
            order_date = start_date + timedelta(days=random_days)
            name = name_samples[random.randint(0, sample_size - 1)]
            amount = round(random.uniform(100, 10000), 2)
            address = address_samples[random.randint(0, sample_size - 1)]
            buffer.append((name, amount, order_date, address))
            
            # 批量寫入
            if len(buffer) >= batch_size:
                cursor.executemany("""
                    INSERT INTO orders_partitioned (customer_name, amount, order_date, address)
                    VALUES (%s, %s, %s, %s)
                """, buffer)
                buffer = []
                
                # 每 100,000 筆 commit 一次並顯示進度
                if (i + 1) % 100000 == 0:
                    conn.commit()
                    
                    current_time = time.time()
                    interval_time = current_time - last_report_time
                    interval_count = (i + 1) - last_report_count
                    speed = interval_count / interval_time if interval_time > 0 else 0
                    elapsed = current_time - total_start
                    
                    print(f"進度: {i + 1:,} / {total_rows:,} "
                          f"| 速度: {speed:,.0f} 筆/秒 "
                          f"| 已耗時: {elapsed:.1f} 秒")
                    
                    last_report_time = current_time
                    last_report_count = i + 1
        
        # === 寫入剩餘資料 ===
        if buffer:
            cursor.executemany("""
                INSERT INTO orders_partitioned (customer_name, amount, order_date, address)
                VALUES (%s, %s, %s, %s)
            """, buffer)
        
        conn.commit()
        
        # 恢復設定
        cursor.execute("SET unique_checks=1")
        cursor.execute("SET foreign_key_checks=1")
        cursor.execute("SET autocommit=1")
        
        # === 總結報告 ===
        total_time = time.time() - total_start
        avg_speed = total_rows / total_time if total_time > 0 else 0
        
        print("=" * 60)
        print(f"✅ 完成！")
        print(f"\n📊 效能統計:")
        print(f"  • 總筆數: {total_rows:,} 筆")
        print(f"  • 總耗時: {total_time:.2f} 秒")
        print(f"  • 平均速度: {avg_speed:,.0f} 筆/秒")
        print(f"  • 樣本準備: {sample_time:.2f} 秒")
        print(f"  • 資料表建立: {table_time:.2f} 秒")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_data()
