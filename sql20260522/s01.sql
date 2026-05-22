-- Active: 1779345108638@@10.167.223.51@3306@mydb260521



-- 1. 用戶表
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '登入帳號',
    name VARCHAR(50) NOT NULL COMMENT '用戶暱稱',
    -- CURRENT_TIMESTAMP: 插入時若沒給時間，自動填入當下時間
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='用戶主檔';

select * from users;

-- 2. 商品表
CREATE TABLE products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL COMMENT '售價',
    stock INT NOT NULL DEFAULT 0 COMMENT '庫存數量',
    specs JSON COMMENT '商品規格 (JSON格式)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否上架',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='商品主檔';

 -- 定義外鍵
    -- CONSTRAINT [命名]: 建議命名，方便日後刪除或除錯
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL COMMENT '購買當下單價',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_orders_product FOREIGN KEY (product_id) REFERENCES products(id)
);

--講義練習
INSERT INTO users (email, name) VALUES 
('alex@example.com', 'Alex');

INSERT INTO products (name, price, stock) VALUES
('iPhone 15', 29900, '10'),
('Samsung Galaxy S21', 24900, 15);
select * from products where stock = '10';

select * from users
where email like 'irene%';

select * from products
where specs ->> '$.color' = 'black';

-- 補貨：將 Laptop 的庫存 +3
UPDATE products
SET stock = stock + 3
WHERE name like 'Laptop%';

DELETE FROM users WHERE email = 'bob@example.com';

START TRANSACTION;
UPDATE products SET stock = stock - 1 WHERE id = 1;

INSERT INTO orders (user_id, product_id, quantity, price_at_purchase) VALUES
(1, 1, 1, 29999.00);
COMMIT;
SELECT * FROM orders;