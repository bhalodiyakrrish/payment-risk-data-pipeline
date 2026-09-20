USE PaymentRiskDW;
GO

/*
Purpose:
Load the trusted staging transactions into the fact table in small
autocommit batches. This avoids one very large active transaction.

The NOT EXISTS condition makes the script safe to rerun after an
interrupted load.
*/

SET NOCOUNT ON;

DECLARE @BatchSize INT = 5000;
DECLARE @RowsInserted INT = 1;

WHILE @RowsInserted > 0
BEGIN
    INSERT INTO dwh.FactTransaction
    (
        TransactionID,
        CustomerKey,
        MerchantKey,
        DateKey,
        TransactionTimestamp,
        Amount,
        Currency,
        PaymentMethod,
        TransactionStatus,
        Country,
        Gateway,
        ResponseCode,
        DeviceType
    )
    SELECT TOP (@BatchSize)
        t.transaction_id,
        c.CustomerKey,
        m.MerchantKey,
        d.DateKey,
        t.transaction_timestamp,
        t.amount,
        t.currency,
        t.payment_method,
        t.transaction_status,
        t.country,
        t.gateway,
        t.response_code,
        t.device_type
    FROM stg.Transactions t
    INNER JOIN dwh.DimCustomer c
        ON c.CustomerID = t.customer_id
    INNER JOIN dwh.DimMerchant m
        ON m.MerchantID = t.merchant_id
    INNER JOIN dwh.DimDate d
        ON d.FullDate = CAST(t.transaction_timestamp AS DATE)
    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dwh.FactTransaction f
        WHERE f.TransactionID = t.transaction_id
    )
    ORDER BY t.transaction_id;

    SET @RowsInserted = @@ROWCOUNT;

    PRINT CONCAT('Batch inserted: ', @RowsInserted);
END;
GO
