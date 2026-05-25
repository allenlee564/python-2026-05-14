select * from products;

select concat(name, stock) as newstr from products;


CREATE TABLE ProductCategory (
    CategoryID   VARCHAR(50)   NOT NULL PRIMARY KEY,   -- 分類唯一識別碼
    CategoryName VARCHAR(100)  NOT NULL,               -- 分類名稱
    ParentID     VARCHAR(50)   NULL,                   -- 上層分類ID，最高層為NULL
    Level        INT           NOT NULL,               -- 分類層級
    Description  TEXT          NULL,                   -- 分類描述（可選）
    CreatedAt    DATETIME      DEFAULT CURRENT_TIMESTAMP, -- 建立時間
    UpdatedAt    DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新時間
    CONSTRAINT fk_parent FOREIGN KEY (ParentID) REFERENCES ProductCategory(CategoryID)
);

INSERT INTO ProductCategory (CategoryID, CategoryName, ParentID, Level)
VALUES 
('p1', '日用品', NULL, 1),
('p1-1', '衛生紙', 'p1', 2),
('p1-1-1', '抽取式', 'p1-1', 3);

select * from `ProductCategory`

select t1.`CategoryID`,t1.`CategoryName`,t1.`Level`,t1.`ParentID`, t2.`CategoryName` from `ProductCategory` as t1
left join `ProductCategory` as t2
on t1.`ParentID` = t2.`CategoryID`

select t1.`CategoryID`,t1.`CategoryName`,t1.`Level`,t1.`ParentID`, 
t2.`CategoryName` ,t2.`ParentID`, t3.`CategoryName`, t3.`ParentID`,
concat(t3.`CategoryName`, ' > ', t2.`CategoryName`, ' > ', t1.`CategoryName`) as bread,
CONCAT_WS(' > ',t3.`CategoryName`,  t2.`CategoryName`,  t1.`CategoryName`) as bread2
from `ProductCategory` as t1
left join `ProductCategory` as t2
on t1.`ParentID` = t2.`CategoryID`
left join `ProductCategory` as t3
on t2.`ParentID` = t3.`CategoryID`


select * from users;

select * from orders where user_id = 1;

select * from products where id in (1, 3, 5);

select pname from view_full_orders_v2 where uid = 1;

-- 列出每位用戶買過的所有商品名稱，用逗號隔開
-- 結果：Alice | iPhone, MacBook, AirPods
-- 列出每位用戶買過的所有商品名稱，用逗號隔開
-- 結果：Alice | iPhone, MacBook, AirPods
SELECT
    u.name,
    GROUP_CONCAT(p.name SEPARATOR ', ') as bought_items
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id
GROUP BY u.id;

SELECT
    o.id,
    u.name as '購買人姓名',
    p.name as '商品名稱',
    o.quantity as '購買數量'
FROM orders as o
join users as u on o.user_id = u.id
join products as p on o.product_id = p.id

--如何計算出每個消費者的消費總金額
select
o.user_id,
sum(o.price_at_purchase) as '消費總金額'
from as orders as o
where o.status in ('PAID', 'SHIPPED')
group by o.user_id
HAVING sum(o.price_at_purchase) > 50000
ORDER BY `消費總金額` DESc;

select t1*, t2.name from view_over_50000_spent_total as t1
join users as t2 ON t1.user_id = t2.id


--會因為清單中提供了null所以是空集合回傳
select * from users id
where id not in (1, 3, null)

--只要使用in或是not in, 其後的清單值一定要過濾null值的資料
select * from users 
where id not IN(
    select user_id from vip_list where user_id is not null
)
