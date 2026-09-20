USE PaymentRiskDW;
GO

IF OBJECT_ID('etl.PipelineExecutionLog', 'U') IS NULL
BEGIN
    CREATE TABLE etl.PipelineExecutionLog
    (
        ExecutionID       BIGINT IDENTITY(1,1) NOT NULL,
        PipelineName      VARCHAR(100) NOT NULL,
        StepName          VARCHAR(100) NOT NULL,
        StartTime         DATETIME2(3) NOT NULL,
        EndTime           DATETIME2(3) NULL,
        Status             VARCHAR(20) NOT NULL,
        RowsAffected       INT NULL,
        ErrorMessage       VARCHAR(4000) NULL,
        CONSTRAINT PK_PipelineExecutionLog PRIMARY KEY (ExecutionID)
    );
END;
GO

SELECT TOP 20 *
FROM etl.PipelineExecutionLog
ORDER BY ExecutionID DESC;
GO
