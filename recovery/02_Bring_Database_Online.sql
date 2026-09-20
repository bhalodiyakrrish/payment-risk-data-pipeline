USE master;
GO

ALTER DATABASE PaymentRiskDW
SET ONLINE;
GO

SELECT
    name,
    physical_name,
    state_desc
FROM sys.master_files
WHERE database_id = DB_ID('PaymentRiskDW');
GO

SELECT
    name,
    state_desc
FROM sys.databases
WHERE name = 'PaymentRiskDW';
GO
