-- Check for compliance with data retention policies
SELECT 
    table_name, 
    pg_size_pretty(pg_total_relation_size(table_name)) AS size,
    last_analyzed
FROM pg_stat_user_tables
WHERE last_analyzed < CURRENT_DATE - INTERVAL '1 year'
ORDER BY size DESC;

-- Check for compliance with data encryption (example for PostgreSQL)
SELECT 
    schemaname, 
    tablename, 
    attname, 
    description 
FROM pg_catalog.pg_attribute a
JOIN pg_catalog.pg_description d ON a.attrelid = d.objoid AND a.attnum = d.objsubid
JOIN pg_catalog.pg_stat_all_tables t ON a.attrelid = t.relid
WHERE attname IN ('data_encrypted') 
    AND description LIKE '%encrypted%'
ORDER BY schemaname, tablename;

-- Check for compliance with access control policies
SELECT 
    r.rolname, 
    r.rolsuper, 
    r.rolcreaterole, 
    r.rolcreatedb, 
    r.rolcanlogin, 
    ARRAY(SELECT b.rolname
          FROM pg_catalog.pg_auth_members m
          JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
          WHERE m.member = r.oid) as memberof
FROM pg_catalog.pg_roles r
ORDER BY r.rolname;

-- Query to check if sensitive data is properly masked or anonymized
SELECT 
    department, 
    COUNT(*) FILTER (WHERE sensitive_data IS NOT NULL AND sensitive_data NOT LIKE '***%') as unmasked_sensitive_data_count
FROM government_spending_view
GROUP BY department
HAVING COUNT(*) FILTER (WHERE sensitive_data IS NOT NULL AND sensitive_data NOT LIKE '***%') > 0;
