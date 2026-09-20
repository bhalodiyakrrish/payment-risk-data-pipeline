USE PaymentRiskDW;
GO

/* Customer dimension */
INSERT INTO dwh.DimCustomer
(
    CustomerID, CustomerName, CustomerEmail, Country,
    RegistrationDate, CustomerStatus
)
SELECT
    s.customer_id, s.customer_name, s.customer_email, s.country,
    s.registration_date, s.customer_status
FROM stg.Customers s
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.DimCustomer d
    WHERE d.CustomerID = s.customer_id
);
GO

/* Merchant dimension */
INSERT INTO dwh.DimMerchant
(
    MerchantID, MerchantName, MerchantCategory, Country,
    OnboardingDate, MerchantStatus
)
SELECT
    s.merchant_id, s.merchant_name, s.merchant_category, s.country,
    s.onboarding_date, s.merchant_status
FROM stg.Merchants s
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.DimMerchant d
    WHERE d.MerchantID = s.merchant_id
);
GO

/* Date dimension */
DECLARE @MinDate DATE, @MaxDate DATE;

SELECT
    @MinDate = MIN(CAST(transaction_timestamp AS DATE)),
    @MaxDate = MAX(CAST(transaction_timestamp AS DATE))
FROM stg.Transactions;

;WITH DateRange AS
(
    SELECT @MinDate AS FullDate
    UNION ALL
    SELECT DATEADD(DAY, 1, FullDate)
    FROM DateRange
    WHERE FullDate < @MaxDate
)
INSERT INTO dwh.DimDate
(
    DateKey, FullDate, Year, Quarter, Month, MonthName,
    Day, DayOfWeek, DayName
)
SELECT
    CONVERT(INT, CONVERT(CHAR(8), FullDate, 112)),
    FullDate,
    YEAR(FullDate),
    DATEPART(QUARTER, FullDate),
    MONTH(FullDate),
    DATENAME(MONTH, FullDate),
    DAY(FullDate),
    DATEPART(WEEKDAY, FullDate),
    DATENAME(WEEKDAY, FullDate)
FROM DateRange dr
WHERE NOT EXISTS
(
    SELECT 1 FROM dwh.DimDate d WHERE d.FullDate = dr.FullDate
)
OPTION (MAXRECURSION 0);
GO
