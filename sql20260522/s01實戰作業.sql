1. **建置環境**：執行 DDL 建立 `ecommerce_db` 及三張表。
2. **數據測試**：
    - 新增 3 個用戶。
    - 新增 2 個商品，其中一個包含 `{"origin": "Japan"}` 的 JSON 屬性。
3. **JSON 查詢**：找出所有產地為 Japan 的商品名稱。
4. **交易模擬**：
    - 手動執行一次 `START TRANSACTION`。
    - 扣減庫存並新增訂單。
    - 執行 `ROLLBACK`。
    - **檢查點**：查詢資料表，確認庫存和訂單是否真的**沒有**變化？

CREATE TABLE users2 (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '登入帳號',
    name VARCHAR(50) NOT NULL COMMENT '用戶暱稱',
    -- CURRENT_TIMESTAMP: 插入時若沒給時間，自動填入當下時間
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='用戶主檔';

CREATE TABLE products2 (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL COMMENT '售價',
    stock INT NOT NULL DEFAULT 0 COMMENT '庫存數量',
    origins JSON COMMENT '商品產地 (JSON格式)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否上架',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='商品主檔';

CREATE TABLE orders2 (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL COMMENT '購買當下單價',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders2_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_orders2_product FOREIGN KEY (product_id) REFERENCES products(id)
);

--新增3個用戶
INSERT INTO users2 (email, name) VALUES 
('alex@example.com', 'Alex'),
('ben@example.com', 'Ben'),
('carol@example.com', 'Carol');

INSERT INTO products2 (name, price, stock, origins) VALUES
('tshirt', 299, 10, '{"origin": "Japan"}'),
('shoes', 2490, 15, '{"origin": "Japan"}');
SELECT name FROM products2
WHERE origins ->> '$.origin' = 'Japan';

START TRANSACTION;

-- 2. 執行一連串 SQL
-- 假設 Alex (user_id=1) 買 iPhone (product_id=1)
UPDATE products2 SET stock = stock - 1 WHERE id = 1;
INSERT INTO orders2 (user_id, product_id, quantity, price_at_purchase) VALUES (1, 1, 1, 299);

-- 3. 判斷與提交
-- 這裡通常由程式碼 (Python/PHP) 判斷有沒有錯誤
-- 如果都沒錯：
COMMIT;

-- 如果有錯 (例如庫存變負數，或外鍵錯誤)：
ROLLBACK;
