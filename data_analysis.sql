-- This script performs more in-depth analysis on the data

-- Query to find potential fraud patterns by frequency of transactions
SELECT 
    department,
    category,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount
FROM government_spending_view
GROUP BY department, category
HAVING COUNT(*) > 100 AND AVG(amount) > 50000
ORDER BY transaction_count DESC;

-- Query to detect unusual patterns in transaction amounts
WITH ranked_transactions AS (
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY department ORDER BY amount DESC) as rn
    FROM government_spending_view
)
SELECT 
    department,
    category,
    amount,
    description,
    date
FROM ranked_transactions
WHERE rn <= 5 AND amount > (SELECT AVG(amount) * 3 FROM government_spending_view);

-- Query to identify departments with high waste (assuming waste is defined as unnecessary spending)
SELECT 
    department,
    SUM(amount) as total_waste
FROM government_spending_view
WHERE category IN ('Office Supplies', 'Travel', 'Entertainment') -- Categories often associated with waste
GROUP BY department
HAVING SUM(amount) > 100000
ORDER BY total_waste DESC;

-- Query to analyze time trends in fraud
SELECT 
    EXTRACT(YEAR FROM date) as year,
    EXTRACT(MONTH FROM date) as month,
    COUNT(*) FILTER (WHERE fraud_flag = 1) as fraud_cases,
    COUNT(*) as total_cases,
    (COUNT(*) FILTER (WHERE fraud_flag = 1)::float / COUNT(*)) * 100 as fraud_percentage
FROM government_spending_view
GROUP BY year, month
ORDER BY year, month;
