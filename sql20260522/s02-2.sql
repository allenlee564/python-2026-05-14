INSERT INTO users (email, name) VALUES
('alice@example.com', 'Alice Chen'),
('bob@example.com', 'Bob Wang'),
('charlie@example.com', 'Charlie Liu'),
('diana@example.com', 'Diana Lee'),
('nobody@test.com', 'Mr. Nobody'),  -- 從沒買過東西的用戶
('rich@test.com', 'Richie Rich');    -- 大戶

INSERT INTO products (name, price, stock) VALUES
('iPhone 15', 29900, 50),
('MacBook Pro', 59900, 30),
('AirPods Pro', 7490, 100),
('iPad Air', 19900, 40),
('Apple Watch', 12900, 60),
('Old Nokia Phone', 1000, 10);  -- 沒人買過的冷門商品

-- Alice 的訂單
-- Bob 的訂單
-- Charlie 的訂單
-- Diana 的訂單
-- Richie Rich 的大額訂單 (用於 HAVING 測試)
INSERT INTO orders (user_id, product_id, quantity, price_at_purchase, status) VALUES
(1, 1, 1, 29900, 'PAID'),      -- iPhone 15
(1, 3, 2, 7490, 'SHIPPED'),    -- 2 個 AirPods
(1, 5, 1, 12900, 'PAID'),      -- Apple Watch

(2, 2, 1, 59900, 'PAID'),      -- MacBook Pro
(2, 4, 1, 19900, 'SHIPPED'),   -- iPad Air

(3, 1, 2, 29900, 'PENDING'),   -- 2 台 iPhone 15
(3, 3, 1, 7490, 'CANCELLED'),  -- AirPods (已取消)

(4, 5, 1, 12900, 'PAID'),      -- Apple Watch

(6, 1, 10, 29900, 'PAID'),     -- 10 台 iPhone 15 (299,000)
(6, 2, 2, 59900, 'PAID');      -- 2 台 MacBook Pro (119,800)

INSERT INTO vip_list (user_id, level, since) VALUES
(1, 'Gold', '2023-01-15'),
(6, 'Platinum', '2022-06-01'),
(NULL, 'Silver', '2024-01-01');  -- 故意插入 NULL

select users.*, orders.id as oid
from users
left join orders
on users.id = orders.user_id
where orders.id is null;  -- 找出從沒買過東西的用戶 (NOT IN 陷阱示範)

-- 多表聯合查詢
select o.*, u.id , u.email, u.name, p.id, p.name, p.price,p.stock  from orders as o
join users as u on o.user_id = u.id
join products as p on o.product_id = p.id

select * from view_full_orders;

-- step1. 2表聯合查詢生成view
select o.*, u.id as uid , u.email, u.name as uname from orders as o
join users as u on o.user_id = u.id

-- step2.  把上面的語法生成view
create view view_orders_users
as 
select o.*, u.id as uid , u.email, u.name as uname from orders as o
join users as u on o.user_id = u.id

-- step3. 2表聯合查詢
select o.id as oid, p.id as pid, p.name as pname, p.price,p.stock  from orders as o
join products as p on o.product_id = p.id

-- step4. 2表聯合查詢生成view
create view view_orders_products
as 
select o.id as oid, p.id as pid, p.name as pname, p.price,p.stock  from orders as o
join products as p on o.product_id = p.id

-- final step , 合成2張view 變一張view
select * from view_orders_users as vou
join view_orders_products as vop
on vou.id = vop.oid

create view view_full_orders_v2
as
select * from view_orders_users as vou
join view_orders_products as vop
on vou.id = vop.oid

select
    (select count(*) from orders where status = 'PENDING') as 'pending筆數',
    (select count(*) from orders where status = 'PAID') as 'paid數量統計',
    (select count(*) from orders where status = 'SHIPPED') as 'shipped數量統計',
    (select count(*) from orders where status = 'CANCELLED') as 'cancelled數量統計';

create view view_order_status_dashboard
as
select
    (select count(*) from orders where status = 'PENDING') as 'pending筆數',
    (select count(*) from orders where status = 'PAID') as 'paid數量統計',
    (select count(*) from orders where status = 'SHIPPED') as 'shipped數量統計',
    (select count(*) from orders where status = 'CANCELLED') as 'cancelled數量統計';

-- group by 群組條件
select 'status', count(*) as '數量統計', sum(orders.price_at_purchase) as '訂單總金額' from orders
where orders.price_at_purchase > 10000
group by 'status'
having count(*) >= 2
  -- HAVING 篩選條件 (用於聚合函數的結果)
