-- Template for a monthly fraud report
CREATE OR REPLACE VIEW monthly_fraud_report AS
SELECT 
    EXTRACT(YEAR FROM date) as year,
    EXTRACT(MONTH FROM date) as month,
    department,
    COUNT(*) FILTER (WHERE fraud_flag = 1) as fraud_cases,
    SUM(amount) FILTER (WHERE fraud_flag = 1) as total_fraud_amount
FROM government_spending_view
GROUP BY year, month, department
ORDER BY year, month, total_fraud_amount DESC;

-- Template for a detailed waste report
CREATE OR REPLACE VIEW detailed_waste_report AS
SELECT 
    department,
    category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_waste,
    AVG(amount) as avg_waste_per_transaction
FROM government_spending_view
WHERE category IN ('Office Supplies', 'Travel', 'Entertainment')
GROUP BY department, category
HAVING SUM(amount) > 10000
ORDER BY total_waste DESC;

-- Query to generate a summary of all reports
SELECT 
    'Fraud Report' as report_type,
    COUNT(*) as total_entries
FROM monthly_fraud_report
UNION ALL
SELECT 
    'Waste Report' as report_type,
    COUNT(*) as total_entries
FROM detailed_waste_report;
