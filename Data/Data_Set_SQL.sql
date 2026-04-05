DROP DATABASE IF EXISTS finance_db;
CREATE DATABASE finance_db;
USE finance_db;

CREATE TABLE income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    source VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_mode VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE savings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE budget (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(7) NOT NULL,
    category VARCHAR(100) NOT NULL,
    allocated_amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE goal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_amount DECIMAL(10,2) NOT NULL
);


SELECT 
    b.month,
    b.category,
    b.allocated_amount,
    IFNULL(SUM(e.amount), 0) AS spent,
    (b.allocated_amount - IFNULL(SUM(e.amount), 0)) AS remaining,
    ROUND(
        (IFNULL(SUM(e.amount), 0) / b.allocated_amount) * 100,
        2
    ) AS percent_used
FROM budget b
LEFT JOIN expenses e
    ON b.category = e.category
    AND DATE_FORMAT(e.date, '%Y-%m') = b.month
WHERE b.month = DATE_FORMAT(CURDATE(), '%Y-%m')
GROUP BY b.month, b.category, b.allocated_amount;

CREATE OR REPLACE VIEW monthly_financial_summary AS
SELECT 
    month_data.month,

    IFNULL(income_data.total_income, 0) AS total_income,
    IFNULL(expense_data.total_expense, 0) AS total_expense,
    IFNULL(saving_data.total_saving, 0) AS total_saving,

    IFNULL(income_data.total_income, 0)
    - IFNULL(expense_data.total_expense, 0)
    - IFNULL(saving_data.total_saving, 0) AS net_balance

FROM
(
    SELECT DATE_FORMAT(date, '%Y-%m') AS month
    FROM income
    UNION
    SELECT DATE_FORMAT(date, '%Y-%m') FROM expenses
    UNION
    SELECT DATE_FORMAT(date, '%Y-%m') FROM savings
) AS month_data

LEFT JOIN
(
    SELECT DATE_FORMAT(date, '%Y-%m') AS month,
           SUM(amount) AS total_income
    FROM income
    GROUP BY DATE_FORMAT(date, '%Y-%m')
) AS income_data
ON month_data.month = income_data.month

LEFT JOIN
(
    SELECT DATE_FORMAT(date, '%Y-%m') AS month,
           SUM(amount) AS total_expense
    FROM expenses
    GROUP BY DATE_FORMAT(date, '%Y-%m')
) AS expense_data
ON month_data.month = expense_data.month

LEFT JOIN
(
    SELECT DATE_FORMAT(date, '%Y-%m') AS month,
           SUM(amount) AS total_saving
    FROM savings
    GROUP BY DATE_FORMAT(date, '%Y-%m')
) AS saving_data
ON month_data.month = saving_data.month;

SELECT SUM(amount)
FROM income
WHERE DATE_FORMAT(date, '%Y-%m') = '2026-02';

SELECT category, SUM(amount)
FROM expenses
GROUP BY category;
SELECT 
    b.category, 
    b.allocated_amount, 
    IFNULL(SUM(e.amount),0) AS spent
FROM budget b
LEFT JOIN expenses e
ON b.category = e.category
GROUP BY b.category, b.allocated_amount;




SELECT * FROM monthly_financial_summary;

