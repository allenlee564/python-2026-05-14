-- Active: 1779345108638@@10.167.223.51@3306@mysql
-- 建立一個名為 ecommerce_db 的資料庫
-- CHARACTER SET: 指定字元編碼
-- COLLATE: 指定排序規則 (例如：大小寫是否敏感)。unicode_ci 是通用且準確的排序規則。
CREATE DATABASE IF NOT EXISTS ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 告訴 MySQL 接下來的所有操作都要在這個資料庫內進行
USE ecommerce_db;