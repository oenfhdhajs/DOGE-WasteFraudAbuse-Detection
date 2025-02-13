-- This script generates a report on data validation results

-- Create a table to store validation results if not exists
CREATE TABLE IF NOT EXISTS validation_results (
    validation_check TEXT,
    result_count INTEGER,
    validation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert validation results from the CSV report into the table
COPY validation_results(validation_check, result_count)
FROM '/path/to/validation_report.csv' WITH CSV HEADER;

-- Query to generate a summary report
SELECT 
    validation_check,
    result_count,
    validation_date
FROM validation_results
ORDER BY validation_date DESC
LIMIT 10;

-- Query to check if there are any critical issues (e.g., high number of missing values or duplicates)
SELECT 
    validation_check,
    result_count
FROM validation_results
WHERE validation_check LIKE '%missing_values%' OR validation_check LIKE '%duplicates%'
    AND result_count > 0
ORDER BY result_count DESC;
