-- This script handles data insertion or updates for new or daily data

-- Insert new transaction data
INSERT INTO government_spending_data (transaction_id, department, category, amount, date, description, flagged)
VALUES (DEFAULT, 'Department of XYZ', 'Software', 50000, CURRENT_DATE, 'Purchase of new analytics software', FALSE);

-- Update existing transaction data
UPDATE government_spending_data
SET flagged = TRUE
WHERE transaction_id = 12345 AND description LIKE '%suspicious%';

-- Procedure to insert daily data from a CSV file (assuming you're using PostgreSQL with file_fdw extension)
CREATE OR REPLACE FUNCTION insert_daily_data(p_file_path TEXT)
RETURNS VOID AS $$
DECLARE
    v_sql TEXT;
BEGIN
    -- Create a foreign table to read from CSV
    v_sql := format('CREATE FOREIGN TABLE daily_data_ext (transaction_id INTEGER, department TEXT, category TEXT, amount NUMERIC, date DATE, description TEXT, flagged BOOLEAN)
                     SERVER file_server
                     OPTIONS (format ''csv'', header ''true'', filename %L)', p_file_path);
    EXECUTE v_sql;

    -- Insert data from the foreign table into the main table
    INSERT INTO government_spending_data (transaction_id, department, category, amount, date, description, flagged)
    SELECT * FROM daily_data_ext;

    -- Drop the foreign table after insertion
    DROP FOREIGN TABLE daily_data_ext;
END;
$$ LANGUAGE plpgsql;

-- Example usage of the function
SELECT insert_daily_data('/path/to/daily_data.csv');
