# Payment Risk & Data Quality Pipeline — Finalization

## Current architecture

Raw CSV
→ Profiling
→ Validation
→ Rejected/Error layer
→ Silver
→ SSIS
→ SQL Server staging
→ Star-schema data warehouse

## Current expected trusted counts

- Customers: 9,920
- Merchants: 970
- Transactions: 95,188

## Warehouse

- `dwh.DimCustomer`
- `dwh.DimMerchant`
- `dwh.DimDate`
- `dwh.FactTransaction`
- `etl.PipelineExecutionLog`

## Important recovery note

The current SQL Server error log showed that `PaymentRiskDW_log.ldf`
was configured at `E:\SQL Data\PaymentRiskDW_log.ldf` and SQL Server
reported OS error 5 (Access is denied).

Before running the warehouse load:

1. Ensure the SQL Server service account has Modify permission on the
   actual log folder.
2. Bring `PaymentRiskDW` online.
3. Verify the database is ONLINE.
4. Run `01_Create_DWH_Tables.sql` only if needed.
5. Run `02_Load_Dimensions.sql`.
6. Run `03_Load_Fact_Batched.sql`.
7. Run `04_Warehouse_Validation.sql`.

The batched fact load is deliberately used instead of one giant INSERT
because the original 95,188-row insert filled the transaction log while
holding an ACTIVE_TRANSACTION.

## Analytics

Analytics/Gold/Power BI work is intentionally deferred. The project
focuses on data engineering, data quality, ETL, dimensional modeling,
SQL Server and incremental-safe loading.
