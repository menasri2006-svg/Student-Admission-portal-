<?php
/**
 * Safe Student Deletion Endpoint
 * Enforces POST method, CSRF validation, and cleans up physical files from disk
 */
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/config/database.php';

requireAdminLogin();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    setFlash('error', 'Invalid request method for record deletion.');
    header('Location: dashboard.php');
    exit;
}

if (!validateCsrfToken($_POST['csrf_token'] ?? '')) {
    setFlash('error', 'Security token mismatch. Action aborted.');
    header('Location: dashboard.php');
    exit;
}

$studentId = (int)($_POST['id'] ?? 0);
if ($studentId <= 0) {
    setFlash('error', 'Invalid student identifier.');
    header('Location: dashboard.php');
    exit;
}

try {
    $pdo = getDbConnection();

    // 1. Fetch student info
    $stmt = $pdo->prepare("SELECT name, roll_number, profile_image FROM students WHERE id = :id LIMIT 1");
    $stmt->execute([':id' => $studentId]);
    $student = $stmt->fetch();

    if (!$student) {
        setFlash('error', 'Student record does not exist or has already been removed.');
        header('Location: dashboard.php');
        exit;
    }

    // 2. Fetch all document file paths to safely unlink from disk
    $docStmt = $pdo->prepare("SELECT file_path FROM student_documents WHERE student_id = :id");
    $docStmt->execute([':id' => $studentId]);
    $docs = $docStmt->fetchAll();

    foreach ($docs as $doc) {
        $realFile = realpath(__DIR__ . '/' . $doc['file_path']);
        $baseDir = realpath(__DIR__ . '/uploads');
        if ($realFile && $baseDir && strpos($realFile, $baseDir) === 0 && file_exists($realFile)) {
            @unlink($realFile);
        }
    }

    // Also remove profile image if present and not already unlinked
    if (!empty($student['profile_image'])) {
        $profileFile = realpath(__DIR__ . '/uploads/profile_images/' . basename($student['profile_image']));
        $baseDir = realpath(__DIR__ . '/uploads');
        if ($profileFile && $baseDir && strpos($profileFile, $baseDir) === 0 && file_exists($profileFile)) {
            @unlink($profileFile);
        }
    }

    // 3. Delete student from database (Foreign Key ON DELETE CASCADE cleans up student_documents)
    $delStmt = $pdo->prepare("DELETE FROM students WHERE id = :id");
    $delStmt->execute([':id' => $studentId]);

    setFlash('success', 'Student record for ' . $student['name'] . ' (' . $student['roll_number'] . ') and all associated files have been permanently deleted.');
    header('Location: dashboard.php');
    exit;

} catch (PDOException $e) {
    setFlash('error', 'Database deletion error: ' . $e->getMessage());
    header('Location: dashboard.php');
    exit;
}
