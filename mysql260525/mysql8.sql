-- Active: 1779345108638@@10.167.223.51@3306@mysql8_demo
CREATE DATABASE IF NOT EXISTS mysql8_demo
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mysql8_demo;

-- 員工表（含自我參照的 manager_id，用於組織架構）
CREATE TABLE employees (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(50)   NOT NULL,
    department  VARCHAR(50)   NOT NULL,
    salary      DECIMAL(10,2) NOT NULL,
    manager_id  INT           DEFAULT NULL,
    hire_date   DATE          NOT NULL
);

-- 每日銷售表
CREATE TABLE daily_sales (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE          NOT NULL,
    amount    DECIMAL(10,2) NOT NULL
);

-- API 操作紀錄（含 JSON 欄位）
CREATE TABLE api_logs (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    payload    JSON     NOT NULL,
    created_at DATETIME DEFAULT NOW()
);

-- 任務佇列
CREATE TABLE task_queue (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    payload    VARCHAR(255) NOT NULL,
    status     ENUM('PENDING','PROCESSING','DONE') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT NOW()
);

-- 員工測試資料（3 個部門，含多層主管關係）
INSERT INTO employees (name, department, salary, manager_id, hire_date) VALUES
('Alice',   'Engineering', 95000, NULL, '2019-03-01'),
('Bob',     'Engineering', 88000,    1, '2020-06-15'),
('Charlie', 'Engineering', 88000,    1, '2021-01-10'),
('Diana',   'Engineering', 72000,    2, '2022-08-01'),
('Eve',     'Marketing',   80000, NULL, '2018-11-20'),
('Frank',   'Marketing',   75000,    5, '2020-03-05'),
('Grace',   'Marketing',   75000,    5, '2021-07-22'),
('Henry',   'Marketing',   60000,    6, '2023-02-14'),
('Ivy',     'HR',          70000, NULL, '2017-05-30'),
('Jack',    'HR',          65000,    9, '2022-09-01');

-- 每日銷售測試資料
INSERT INTO daily_sales (sale_date, amount) VALUES
('2024-01-01', 12000), ('2024-01-02',  8500), ('2024-01-03', 15000),
('2024-01-04',  9200), ('2024-01-05', 18000), ('2024-01-06', 11000),
('2024-01-07', 22000);

-- API 紀錄測試資料（含巢狀 JSON 與 items 陣列）
INSERT INTO api_logs (payload) VALUES
('{"user_id": 1, "action": "login",    "meta": {"ip": "192.168.1.1", "device": "mobile"}}'),
('{"user_id": 2, "action": "purchase", "meta": {"ip": "10.0.0.5", "device": "desktop"}, "items": [{"product_id": 101, "qty": 2, "price": 299.00}, {"product_id": 205, "qty": 1, "price": 599.00}]}'),
('{"user_id": 1, "action": "logout",   "meta": {"ip": "192.168.1.1", "device": "mobile"}}'),
('{"user_id": 3, "action": "login",    "meta": {"ip": "172.16.0.8",  "device": "tablet"}}'),
('{"user_id": 3, "action": "purchase", "meta": {"ip": "172.16.0.8",  "device": "tablet"}, "items": [{"product_id": 101, "qty": 1, "price": 299.00}]}');

-- 任務佇列測試資料
INSERT INTO task_queue (payload, status) VALUES
('{"type": "send_email",   "to": "alice@example.com"}', 'PENDING'),
('{"type": "resize_image", "file": "photo_001.jpg"}',   'PENDING'),
('{"type": "send_email",   "to": "bob@example.com"}',   'PENDING'),
('{"type": "gen_report",   "month": "2024-01"}',        'PENDING'),
('{"type": "send_email",   "to": "eve@example.com"}',   'DONE');

-- 各部門薪資排名（三種方式對照）
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rnk
FROM employees;

select
    name,
    department,
    salary,
    rank() over(order by salary desc) as rnk
from employees;

select
    sale_date,
    amount,
    sum(amount) over(order by sale_date) as cumulative_sum
    round(
        avg(amount) over(order by sale_date rows between 2 preceding and current row), 0
    )
from daily_sales;

select * from daily_sales where sale_date = '2024-01-02';