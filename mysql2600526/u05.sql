
SELECT
  name,
  salary,
  CASE
    WHEN salary >= 60000 THEN '高薪'
    WHEN salary >= 40000 THEN '中薪'
    ELSE '低薪'
  END AS level
FROM employees;

CREATE TABLE employees2 (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  salary INT,
  department VARCHAR(30),
  years_of_service INT
);

INSERT INTO employees2 (name, salary, department, years_of_service) VALUES
('Amy', 50000, 'IT', 3),
('Ben', 30000, 'Sales', 1),
('Carol', 70000, 'IT', 5),
('David', 45000, 'HR', 2),
('Emma', 80000, 'Sales', 7);

SELECT
  CASE
    WHEN years_of_service >= 5 THEN '資深'
    WHEN years_of_service >= 2 AND years_of_service < 5 THEN '專家'
    ELSE '新進'
  END AS level,
  COUNT(*) AS count
FROM employees2
GROUP BY
  CASE
    WHEN years_of_service >= 5 THEN '資深'
    WHEN years_of_service >= 2 AND years_of_service < 5 THEN '專家'
    ELSE '新進'
  END;
UPDATE employees2
SET salary =
  CASE
    WHEN years_of_service >= 5 THEN salary * 1.00-- 5年以上加薪15%
    WHEN years_of_service >= 2 AND years_of_service < 5 THEN salary * 1.00-- 3-4年加薪10%
    else  salary * 1.08-- 1-2年加薪5%  
  END;

