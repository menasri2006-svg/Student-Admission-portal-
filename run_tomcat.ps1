$env:JAVA_HOME = "C:\Program Files\Java\jdk-24"
$env:JRE_HOME = "C:\Program Files\Java\jdk-24"
$env:CATALINA_HOME = "C:\xampp\tomcat"
$env:CATALINA_BASE = "C:\xampp\tomcat"

$env:DB_PORT = "3307"

& "C:\xampp\tomcat\bin\catalina.bat" run
