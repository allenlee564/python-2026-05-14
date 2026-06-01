create database IF NOT EXISTS test_database
CHARACTER SET utf8mb4

CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '登入帳號',
    name VARCHAR(50) NOT NULL COMMENT '用戶暱稱',
    -- CURRENT_TIMESTAMP: 插入時若沒給時間，自動填入當下時間
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='用戶主檔';

CREATE TABLE products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL COMMENT '售價',
    stock INT NOT NULL DEFAULT 0 COMMENT '庫存數量',
    origins JSON COMMENT '商品產地 (JSON格式)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否上架',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) COMMENT='商品主檔';

CREATE TABLE inventory_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL COMMENT '購買當下單價',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_log_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_inventory_log_product FOREIGN KEY (product_id) REFERENCES products(id)
);
INSERT INTO products (name, price, stock, origins) VALUES
('tshirt', 299, 10, '{"origin": "Japan"}'),
('hat', 299, 10, '{"origin": "Japan"}'),
('shoes', 2490, 15, '{"origin": "Japan"}');