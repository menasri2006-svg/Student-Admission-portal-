$ErrorActionPreference = "Stop"
$javaHome = "C:\Program Files\Java\jdk-24"
$javac = "$javaHome\bin\javac.exe"
$jar = "$javaHome\bin\jar.exe"

$cp = "C:\xampp\tomcat\lib\servlet-api.jar;C:\xampp\tomcat\lib\jsp-api.jar;E:\Webproject\java-portal\src\main\webapp\WEB-INF\lib\mysql-connector-j-8.0.33.jar"
$src = Get-ChildItem -Path "E:\Webproject\java-portal\src\main\java" -Filter "*.java" -Recurse | Select-Object -ExpandProperty FullName

New-Item -ItemType Directory -Path "E:\Webproject\java-portal\src\main\webapp\WEB-INF\classes" -Force | Out-Null

Write-Host "Compiling Java sources..."
& $javac -cp $cp -d "E:\Webproject\java-portal\src\main\webapp\WEB-INF\classes" $src
if ($LASTEXITCODE -ne 0) {
    Write-Error "javac failed with code $LASTEXITCODE"
}
Write-Host "Java compilation succeeded!"

Write-Host "Packaging WAR..."
New-Item -ItemType Directory -Path "E:\Webproject\java-portal\target" -Force | Out-Null
Set-Location "E:\Webproject\java-portal\src\main\webapp"
& $jar -cvf "E:\Webproject\java-portal\target\student-portal.war" *
Set-Location "E:\Webproject"
Write-Host "WAR packaging completed: E:\Webproject\java-portal\target\student-portal.war"
