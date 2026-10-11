param([string]$targetPort = "8082")
$xmlPath = "C:\xampp\tomcat\conf\server.xml"
$content = Get-Content $xmlPath -Raw
if ($targetPort -eq "8082") {
    $content = $content.Replace('port="8080" protocol="HTTP/1.1"', 'port="8082" protocol="HTTP/1.1"')
} else {
    $content = $content.Replace('port="8082" protocol="HTTP/1.1"', 'port="8080" protocol="HTTP/1.1"')
}
Set-Content -Path $xmlPath -Value $content
Write-Host "Updated server.xml port to $targetPort"
