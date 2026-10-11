<?php
header('Content-Type: text/plain; charset=utf-8');

$host = '127.0.0.1';
$port = 3306;
$user = 'root';
$pass = '';

echo "Connecting to MySQL server on $host:$port...\n";

try {
    $dsn = "mysql:host=$host;port=$port;charset=utf8mb4";
    $pdo = new PDO($dsn, $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_TIMEOUT => 5
    ]);
    echo "Connected successfully to MySQL server!\n";

    $sqlFile = __DIR__ . '/database/student_portal.sql';
    if (!file_exists($sqlFile)) {
        die("Error: SQL file not found at $sqlFile\n");
    }

    $sql = file_get_contents($sqlFile);
    $pdo->exec($sql);
    echo "Successfully executed student_portal.sql schema and seed data!\n";

    // Verify
    $pdo->exec("USE `student_portal`");
    $tables = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
    echo "Tables in student_portal: " . implode(', ', $tables) . "\n";
    foreach ($tables as $t) {
        $count = $pdo->query("SELECT COUNT(*) FROM `$t`")->fetchColumn();
        echo " - Table $t has $count rows.\n";
    }
    echo "DATABASE_SETUP_SUCCESSFUL\n";

} catch (Exception $e) {
    echo "DATABASE_SETUP_ERROR: " . $e->getMessage() . "\n";
}
