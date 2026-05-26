-- 1. 建立商品表
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    stock INT NOT NULL
);

-- 塞入初始資料：筆記本 100 本
INSERT INTO products (name, stock) VALUES ('筆記本', 100);

-- 2. 建立訂單表
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) -- 建立外鍵關聯
);

CREATE TRIGGER order_stock_check
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  update products
  set stock = stock - NEW.quantity
    where id = NEW.product_id;
  END ;

-- A. 檢查原本庫存（此時筆記本 stock 應為 100）
SELECT * FROM products;

-- B. 新增一筆訂單：購買 5 本筆記本 (product_id = 1)
INSERT INTO orders (product_id, quantity) VALUES (1, 5);

-- C. 再次檢查商品庫存（此時筆記本 stock 自動減少到 95）
SELECT * FROM products;