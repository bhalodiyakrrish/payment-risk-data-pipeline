USE PaymentRiskDW;
GO

SELECT 'DimCustomer' AS table_name, COUNT(*) AS row_count
FROM dwh.DimCustomer
UNION ALL
SELECT 'DimMerchant', COUNT(*)
FROM dwh.DimMerchant
UNION ALL
SELECT 'DimDate', COUNT(*)
FROM dwh.DimDate
UNION ALL
SELECT 'FactTransaction', COUNT(*)
FROM dwh.FactTransaction;
GO

/* Duplicate business keys */
SELECT CustomerID, COUNT(*) AS cnt
FROM dwh.DimCustomer
GROUP BY CustomerID
HAVING COUNT(*) > 1;

SELECT MerchantID, COUNT(*) AS cnt
FROM dwh.DimMerchant
GROUP BY MerchantID
HAVING COUNT(*) > 1;

SELECT TransactionID, COUNT(*) AS cnt
FROM dwh.FactTransaction
GROUP BY TransactionID
HAVING COUNT(*) > 1;
GO

/* Foreign-key integrity checks */
SELECT COUNT(*) AS orphan_customer_keys
FROM dwh.FactTransaction f
LEFT JOIN dwh.DimCustomer d ON d.CustomerKey = f.CustomerKey
WHERE d.CustomerKey IS NULL;

SELECT COUNT(*) AS orphan_merchant_keys
FROM dwh.FactTransaction f
LEFT JOIN dwh.DimMerchant d ON d.MerchantKey = f.MerchantKey
WHERE d.MerchantKey IS NULL;

SELECT COUNT(*) AS orphan_date_keys
FROM dwh.FactTransaction f
LEFT JOIN dwh.DimDate d ON d.DateKey = f.DateKey
WHERE d.DateKey IS NULL;
GO

/* Expected final counts for the current synthetic dataset */
SELECT
    CASE WHEN (SELECT COUNT(*) FROM dwh.DimCustomer) = 9920
         THEN 'PASS' ELSE 'CHECK' END AS DimCustomer_Check,
    CASE WHEN (SELECT COUNT(*) FROM dwh.DimMerchant) = 970
         THEN 'PASS' ELSE 'CHECK' END AS DimMerchant_Check,
    CASE WHEN (SELECT COUNT(*) FROM dwh.FactTransaction) = 95188
         THEN 'PASS' ELSE 'CHECK' END AS FactTransaction_Check;
GO
