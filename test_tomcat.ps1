$ErrorActionPreference = "Continue"
$env:JAVA_HOME = "C:\Program Files\Java\jdk-24"
$env:JRE_HOME = "C:\Program Files\Java\jdk-24"
$env:CATALINA_HOME = "C:\xampp\tomcat"
$env:CATALINA_BASE = "C:\xampp\tomcat"

Write-Host "Running Tomcat configtest..."
& "C:\xampp\tomcat\bin\catalina.bat" configtest
Write-Host "Configtest exit code: $LASTEXITCODE"
