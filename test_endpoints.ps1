$ErrorActionPreference = "Stop"

Write-Host "=== TEST 1: Registration Module (CO3) ==="
$regResp = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/registration/" -UseBasicParsing
Write-Host "Registration page HTTP:" $regResp.StatusCode

Write-Host "=== TEST 2: PHP Admin Login Page (CO4) ==="
$phpLogin = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/php-admin/login.php" -UseBasicParsing
Write-Host "PHP Admin login page HTTP:" $phpLogin.StatusCode

Write-Host "=== TEST 3: Java Portal Login Page (CO5) ==="
$javaLogin = Invoke-WebRequest -Uri "http://localhost:8082/student-portal/login" -UseBasicParsing
Write-Host "Java portal login page HTTP:" $javaLogin.StatusCode

Write-Host "=== ALL INITIAL HTTP RESPONSES 200 OK ==="
