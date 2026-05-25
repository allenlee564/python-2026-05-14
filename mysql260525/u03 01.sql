--2. **索引優化**：
    - 建立索引 `CREATE INDEX idx_user ON audit_logs(user_id)`。
    - 再次 `EXPLAIN`，確認 `type` 變為 `ref`。
    - 記錄執行時間，計算效能提升倍數。
3. **覆蓋索引實驗**：
    - 查詢 `SELECT action FROM audit_logs WHERE user_id = 123`。
    - 建立複合索引 `CREATE INDEX idx_user_action ON audit_logs(user_id, action)`。
    - 驗證 `EXPLAIN` 的 `Extra` 欄位是否出現 `Using index`。
4. **深分頁優化 (進階挑戰)**：
    - 模擬分頁：`SELECT * FROM audit_logs LIMIT 10 OFFSET 90000` (翻到第 9000 頁)。
    - 觀察耗時。
    - 嘗試使用 **延遲關聯 (Deferred Join)** 技巧優化：
    `sql SELECT t1.* FROM audit_logs t1 JOIN (SELECT id FROM audit_logs LIMIT 10 OFFSET 90000) t2 ON t1.id = t2.id;`
    - 比較兩者效能差異。

create INDEX idx_user ON audit_logs(user_id);
create INDEX idx_user_action ON audit_logs(user_id, action);
explain SELECT action FROM audit_logs WHERE user_id = 123;
explain SELECT * FROM audit_logs LIMIT 10 OFFSET 90000;
SELECT t1.* FROM audit_logs t1 JOIN (SELECT id FROM audit_logs LIMIT 10 OFFSET 90000) t2 ON t1.id = t2.id;

EXPLAIN SELECT t1.* FROM audit_logs t1 JOIN (SELECT id FROM audit_logs LIMIT 10 OFFSET 90000) t2 ON t1.id = t2.id;
select max(create_time) , MIN(create_time) from audit_logs

select count(*) from audit_logs where create_time between '2021-01-01' and '2022-01-01'

select count(*) from audit_logs where create_time between '2022-01-01' and '2023-01-01'

select count(*) from audit_logs where create_time between '2023-01-01' and

    '2024-01-01'

select count(*) from orders_partitioned where order_date < '2024-01-01';
 