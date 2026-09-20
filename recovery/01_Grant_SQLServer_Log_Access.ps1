# Run PowerShell as Administrator.
# This grants the default SQL Server Database Engine service account
# Modify permission on the folder containing the PaymentRiskDW log.
#
# IMPORTANT:
# Use the actual folder recorded by SQL Server. In the current setup
# the SQL Server error log reported: E:\SQL Data

$folder = "E:\SQL Data"
$account = "NT SERVICE\MSSQLSERVER"

icacls $folder /grant "$account:(OI)(CI)M" /T
Write-Host "Permission update completed for $account on $folder"
