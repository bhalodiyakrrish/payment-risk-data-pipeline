USE PaymentRiskDW;
GO

/* Run only if these tables do not already exist. */

IF OBJECT_ID('dwh.DimCustomer', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.DimCustomer
    (
        CustomerKey       INT IDENTITY(1,1) NOT NULL,
        CustomerID        VARCHAR(20)     NOT NULL,
        CustomerName      VARCHAR(100)    NOT NULL,
        CustomerEmail     VARCHAR(255)    NOT NULL,
        Country           CHAR(2)         NOT NULL,
        RegistrationDate  DATE            NOT NULL,
        CustomerStatus    VARCHAR(20)     NOT NULL,
        CONSTRAINT PK_DimCustomer PRIMARY KEY CLUSTERED (CustomerKey),
        CONSTRAINT UQ_DimCustomer_CustomerID UNIQUE (CustomerID)
    );
END;
GO

IF OBJECT_ID('dwh.DimMerchant', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.DimMerchant
    (
        MerchantKey       INT IDENTITY(1,1) NOT NULL,
        MerchantID        VARCHAR(20)     NOT NULL,
        MerchantName      VARCHAR(100)    NOT NULL,
        MerchantCategory  VARCHAR(30)     NOT NULL,
        Country           CHAR(2)         NOT NULL,
        OnboardingDate    DATE            NOT NULL,
        MerchantStatus    VARCHAR(20)     NOT NULL,
        CONSTRAINT PK_DimMerchant PRIMARY KEY CLUSTERED (MerchantKey),
        CONSTRAINT UQ_DimMerchant_MerchantID UNIQUE (MerchantID)
    );
END;
GO

IF OBJECT_ID('dwh.DimDate', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.DimDate
    (
        DateKey      INT          NOT NULL,
        FullDate     DATE         NOT NULL,
        Year         INT          NOT NULL,
        Quarter      INT          NOT NULL,
        Month        INT          NOT NULL,
        MonthName    VARCHAR(20)  NOT NULL,
        Day          INT          NOT NULL,
        DayOfWeek    INT          NOT NULL,
        DayName      VARCHAR(20)  NOT NULL,
        CONSTRAINT PK_DimDate PRIMARY KEY CLUSTERED (DateKey),
        CONSTRAINT UQ_DimDate_FullDate UNIQUE (FullDate)
    );
END;
GO

IF OBJECT_ID('dwh.FactTransaction', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.FactTransaction
    (
        TransactionKey       BIGINT IDENTITY(1,1) NOT NULL,
        TransactionID        VARCHAR(30)      NOT NULL,
        CustomerKey          INT              NOT NULL,
        MerchantKey         INT              NOT NULL,
        DateKey              INT              NOT NULL,
        TransactionTimestamp DATETIME2(3)     NOT NULL,
        Amount               DECIMAL(18,2)    NOT NULL,
        Currency             CHAR(3)          NOT NULL,
        PaymentMethod        VARCHAR(30)      NOT NULL,
        TransactionStatus    VARCHAR(20)      NOT NULL,
        Country              CHAR(2)         NOT NULL,
        Gateway              VARCHAR(30)     NOT NULL,
        ResponseCode         CHAR(2)         NOT NULL,
        DeviceType           VARCHAR(20)     NOT NULL,
        CONSTRAINT PK_FactTransaction PRIMARY KEY CLUSTERED (TransactionKey),
        CONSTRAINT UQ_FactTransaction_TransactionID UNIQUE (TransactionID),
        CONSTRAINT FK_FactTransaction_Customer FOREIGN KEY (CustomerKey)
            REFERENCES dwh.DimCustomer(CustomerKey),
        CONSTRAINT FK_FactTransaction_Merchant FOREIGN KEY (MerchantKey)
            REFERENCES dwh.DimMerchant(MerchantKey),
        CONSTRAINT FK_FactTransaction_Date FOREIGN KEY (DateKey)
            REFERENCES dwh.DimDate(DateKey)
    );
END;
GO
