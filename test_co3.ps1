$ErrorActionPreference = "Continue"

Write-Host "--- Test A: Empty Fields (Required validation) ---"
$emptyBody = @{
    name = ""
    roll_number = ""
    email = ""
    course = ""
    password = ""
    confirm_password = ""
}
try {
    $resp = Invoke-RestMethod -Uri "http://localhost/student-admission-portal/registration/register.php" -Method Post -Body $emptyBody
    Write-Host "Unexpected success: $($resp | ConvertTo-Json)"
} catch {
    Write-Host "Correctly rejected empty submission: Status" $_.Exception.Response.StatusCode.value__
}

Write-Host "--- Test B: Invalid Email ---"
$invalidEmailBody = @{
    name = "Test Student"
    roll_number = "TEST-999"
    email = "invalid-email-format"
    course = "B.Tech Computer Science"
    password = "Password@123"
    confirm_password = "Password@123"
}
try {
    $resp = Invoke-RestMethod -Uri "http://localhost/student-admission-portal/registration/register.php" -Method Post -Body $invalidEmailBody
    Write-Host "Unexpected success: $($resp | ConvertTo-Json)"
} catch {
    Write-Host "Correctly rejected invalid email: Status" $_.Exception.Response.StatusCode.value__
}

Write-Host "--- Test C: Weak Password ---"
$weakPwdBody = @{
    name = "Test Student"
    roll_number = "TEST-999"
    email = "test.weak@example.com"
    course = "B.Tech Computer Science"
    password = "weak"
    confirm_password = "weak"
}
try {
    $resp = Invoke-RestMethod -Uri "http://localhost/student-admission-portal/registration/register.php" -Method Post -Body $weakPwdBody
    Write-Host "Unexpected success: $($resp | ConvertTo-Json)"
} catch {
    Write-Host "Correctly rejected weak password: Status" $_.Exception.Response.StatusCode.value__
}

Write-Host "--- Test D: Valid Registration Submission ---"
$validBody = @{
    name = "Priya Sharma"
    roll_number = "CS2026-101"
    email = "priya.sharma@example.com"
    course = "B.Tech Computer Science"
    password = "Password@123"
    confirm_password = "Password@123"
}
try {
    $resp = Invoke-RestMethod -Uri "http://localhost/student-admission-portal/registration/register.php" -Method Post -Body $validBody
    Write-Host "Valid registration response:" ($resp | ConvertTo-Json)
} catch {
    Write-Host "Error on valid registration:" $_.Exception.Message
}
