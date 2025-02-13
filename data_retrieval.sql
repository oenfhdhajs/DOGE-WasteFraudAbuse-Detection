-- This script retrieves data for initial analysis

-- Create a view for easier data retrieval
CREATE VIEW government_spending_view AS
SELECT 
    transaction_id,
    department,
    category,
    amount,
    date,
    description,
    CASE 
        WHEN flagged = TRUE THEN 1
        ELSE 0
    END AS fraud_flag
FROM government_spending_data;

-- Query to fetch all data from the view for analysis
SELECT * FROM government_spending_view;

-- Query to fetch specific data, like transactions over a certain amount
SELECT * FROM government_spending_view
WHERE amount > 10000
ORDER BY amount DESC
LIMIT 100;

-- Query to get summary statistics
SELECT 
    department,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    SUM(amount) as total_amount
FROM government_spending_view
GROUP BY department
ORDER BY total_amount DESC;
