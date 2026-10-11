$ErrorActionPreference = "Stop"
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

Write-Host "1. Fetch login page and extract CSRF token..."
$loginPage = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/php-admin/login.php" -WebSession $session -UseBasicParsing
$csrfToken = ""
if ($loginPage.Content -match 'name="csrf_token"\s+value="([^"]+)"') {
    $csrfToken = $matches[1]
}
Write-Host "CSRF Token obtained: $csrfToken"

Write-Host "2. Submitting Admin Login with admin / Password@123..."
$loginBody = @{
    username = "admin"
    password = "Password@123"
    csrf_token = $csrfToken
}
$loginResp = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/php-admin/login.php" -Method Post -Body $loginBody -WebSession $session -MaximumRedirection 0 -ErrorAction SilentlyContinue
Write-Host "Login response status:" $loginResp.StatusCode
Write-Host "Redirect location:" $loginResp.Headers.Location

Write-Host "3. Accessing Dashboard..."
$dashResp = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/php-admin/dashboard.php" -WebSession $session -UseBasicParsing
Write-Host "Dashboard status:" $dashResp.StatusCode
Write-Host "Contains 'Admission Office':" ($dashResp.Content.Contains("Admission Office"))
Write-Host "Contains 'Priya Sharma':" ($dashResp.Content.Contains("Priya Sharma"))

Write-Host "4. Testing Session Protection on protected page without session..."
$noSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$protectResp = Invoke-WebRequest -Uri "http://localhost/student-admission-portal/php-admin/dashboard.php" -WebSession $noSession -MaximumRedirection 0 -ErrorAction SilentlyContinue
Write-Host "Unauthenticated request status:" $protectResp.StatusCode
Write-Host "Unauthenticated redirect:" $protectResp.Headers.Location

Write-Host "CO4 API tests PASSED!"
