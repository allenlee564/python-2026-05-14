SELECT * FROM mydb.orders_large 
WHERE customer_id = 888 
LIMIT 100;

SELECT COUNT(*) AS 總訂單數, SUM(amount) AS 總銷售金額 
FROM mydb.orders_large 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

SELECT status AS 訂單狀態, COUNT(*) AS 訂單數量, SUM(amount) AS 總金額 
FROM mydb.orders_large 
GROUP BY status;

SELECT * FROM mydb.orders_large 
ORDER BY amount DESC 
LIMIT 5;

SELECT o.order_id, o.customer_id, p.product_name, o.amount, o.order_date 
FROM mydb.orders_large o
INNER JOIN mydb.products p ON o.product_id = p.product_id
LIMIT 100;

SELECT p.product_name AS 商品名稱, 
       COUNT(o.order_id) AS 總訂單數, 
       SUM(o.amount) AS 總收入, 
       AVG(o.amount) AS 平均訂單金額
FROM mydb.products p
LEFT JOIN mydb.orders_large o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name;

SELECT customer_id AS 客戶ID, COUNT(*) AS 購買次數, SUM(amount) AS 累積消費金額
FROM mydb.orders_large
GROUP BY customer_id
ORDER BY 購買次數 DESC
LIMIT 10;

SELECT p.product_name AS 商品名稱, 
       p.stock AS 目前庫存量, 
       COUNT(o.order_id) AS 已售出訂單數,
       SUM(o.amount) AS 創造總業績
FROM mydb.products p
LEFT JOIN mydb.orders_large o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.stock;

---任務三---
EXPLAIN SELECT * FROM mydb.orders_large 
WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30';

SELECT YEAR(order_date) AS 年份, 
       COUNT(*) AS 總訂單數, 
       SUM(amount) AS 總銷售金額 
FROM mydb.orders_large 
GROUP BY YEAR(order_date);

SELECT DATE_FORMAT(order_date, '%Y-%m') AS 月份, 
       COUNT(*) AS 該月訂單數, 
       SUM(amount) AS 該月總營業額
FROM mydb.orders_large 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY 月份 ASC;

SELECT customer_id AS 客戶ID, 
       SUM(amount) AS 2025年累積消費金額
FROM mydb.orders_large 
WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY customer_id
ORDER BY 2025年累積消費金額 DESC 
LIMIT 5;

SELECT COUNT(*) AS 刪除前的2023年訂單數 
FROM mydb.orders_large 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';

ALTER TABLE mydb.orders_large DROP PARTITION p2023;

SELECT COUNT(*) AS 刪除後的2023年訂單數 
FROM mydb.orders_large 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';

---任務四---
EXPLAIN SELECT SQL_NO_CACHE * FROM mydb.orders_large 
WHERE customer_id = 12345;

SELECT SQL_NO_CACHE * FROM mydb.orders_large 
WHERE customer_id = 12345;

CREATE INDEX idx_customer_date_amount 
ON mydb.orders_large (customer_id, order_date, amount);

EXPLAIN SELECT SQL_NO_CACHE * FROM mydb.orders_large 
WHERE customer_id = 12345;

SELECT SQL_NO_CACHE * FROM mydb.orders_large 
WHERE customer_id = 12345;

SELECT order_id, customer_id, order_date, amount, status 
FROM mydb.orders_large 
WHERE customer_id = 8888 
ORDER BY order_date DESC 
LIMIT 10;

SELECT order_id, customer_id, order_date, amount, status 
FROM mydb.orders_large 
WHERE customer_id = 9999 
  AND order_date BETWEEN '2024-01-01' AND '2024-06-30';
  
SELECT customer_id, order_id, order_date, amount, status 
FROM mydb.orders_large 
WHERE customer_id = 7777 
  AND amount > 200.00
ORDER BY amount DESC;

---任務五---

WITH Customer_Total AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM mydb.orders_large
    GROUP BY customer_id
)
SELECT customer_id, total_spent
FROM Customer_Total
WHERE total_spent > 5000.00
ORDER BY total_spent DESC
LIMIT 10;

WITH Customer_Stats AS (
    SELECT customer_id, AVG(amount) AS avg_amount, COUNT(*) AS order_count
    FROM mydb.orders_large
    GROUP BY customer_id
)
SELECT customer_id, avg_amount, order_count
FROM Customer_Stats
WHERE avg_amount > (SELECT AVG(amount) FROM mydb.orders_large)
ORDER BY avg_amount DESC
LIMIT 10;

WITH Customer_Rank_Base AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM mydb.orders_large
    GROUP BY customer_id
    LIMIT 20  -- 限制前 20 名來做視窗排名
)
SELECT customer_id, total_spent,
       ROW_NUMBER() OVER (ORDER BY total_spent DESC) AS rnk_num
FROM Customer_Rank_Base;

WITH Same_Amount_Base AS (
    SELECT order_id, customer_id, amount
    FROM mydb.orders_large
    WHERE amount > 450.00
    LIMIT 20
)
SELECT order_id, customer_id, amount,
       RANK() OVER (ORDER BY amount DESC) AS 'RANK跳號排名',
       DENSE_RANK() OVER (ORDER BY amount DESC) AS 'DENSE不跳號排名'
FROM Same_Amount_Base;

WITH Customer_Timeline AS (
    SELECT order_id, customer_id, order_date, amount
    FROM mydb.orders_large
    WHERE customer_id = 8888  -- 固定看某一位客戶的消費軌跡
    ORDER BY order_date ASC
)
SELECT order_id, order_date, amount AS 本次消費,
       LAG(amount, 1) OVER (ORDER BY order_date ASC) AS 上次消費,
       (amount - LAG(amount, 1) OVER (ORDER BY order_date ASC)) AS 金額差額
FROM Customer_Timeline;

WITH Customer_Rolling AS (
    SELECT order_id, customer_id, order_date, amount
    FROM mydb.orders_large
    WHERE customer_id = 6666  -- 看特定客戶
)
SELECT order_id, 
       order_date, 
       amount AS 當筆金額,
       -- ✨ 修正核心：加入 order_id 排序，確保每筆訂單獨立精準累加
       SUM(amount) OVER (ORDER BY order_date ASC, order_id ASC) AS 帳戶累積總消費
FROM Customer_Rolling
ORDER BY order_date ASC, order_id ASC;