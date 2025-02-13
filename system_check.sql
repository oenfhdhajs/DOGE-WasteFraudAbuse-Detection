-- Check for database size
SELECT 
    pg_size_pretty(pg_database_size('government_spending_db')) AS db_size;

-- Check for table bloat (inefficiency in storage)
SELECT 
    schemaname, 
    tablename, 
    pg_size_pretty(pg_relation_size(relid)) AS table_size,
    pgstattuple(relid) 
FROM pg_stat_user_tables 
WHERE schemaname = 'public';

-- Check for long running transactions
SELECT 
    pid, 
    now() - xact_start as transaction_duration,
    query 
FROM pg_stat_activity 
WHERE state = 'active' AND now() - xact_start > interval '5 minutes';

-- Check for locks
SELECT 
    locktype, 
    database, 
    relation::regclass, 
    mode, 
    granted 
FROM pg_locks 
WHERE NOT granted;
