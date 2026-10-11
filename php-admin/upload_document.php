<?php
/**
 * Student Document Upload & Document Deletion Handler
 * Handles file validation, MIME checking, metadata storage, and safe unlinking
 */
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/config/database.php';

requireAdminLogin();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: dashboard.php');
    exit;
}

if (!validateCsrfToken($_POST['csrf_token'] ?? '')) {
    setFlash('error', 'CSRF verification failed. Action rejected.');
    header('Location: dashboard.php');
    exit;
}

$action = $_POST['action'] ?? 'upload';
$studentId = (int)($_POST['student_id'] ?? 0);

if ($studentId <= 0) {
    setFlash('error', 'Invalid student ID.');
    header('Location: dashboard.php');
    exit;
}

$pdo = getDbConnection();

// Action 1: Delete a specific document
if ($action === 'delete') {
    $docId = (int)($_POST['doc_id'] ?? 0);
    if ($docId <= 0) {
        setFlash('error', 'Invalid document ID.');
        header('Location: view_student.php?id=' . $studentId);
        exit;
    }

    try {
        $stmt = $pdo->prepare("SELECT file_path, original_filename FROM student_documents WHERE id = :id AND student_id = :sid LIMIT 1");
        $stmt->execute([':id' => $docId, ':sid' => $studentId]);
        $doc = $stmt->fetch();

        if ($doc) {
            $realPath = realpath(__DIR__ . '/' . $doc['file_path']);
            $baseDir = realpath(__DIR__ . '/uploads');
            if ($realPath && $baseDir && strpos($realPath, $baseDir) === 0 && file_exists($realPath)) {
                @unlink($realPath);
            }

            $delStmt = $pdo->prepare("DELETE FROM student_documents WHERE id = :id");
            $delStmt->execute([':id' => $docId]);

            setFlash('success', 'Document "' . $doc['original_filename'] . '" removed successfully.');
        } else {
            setFlash('error', 'Document not found.');
        }
    } catch (PDOException $e) {
        setFlash('error', 'Database error: ' . $e->getMessage());
    }

    header('Location: view_student.php?id=' . $studentId);
    exit;
}

// Action 2: Upload a new document
if (empty($_FILES['document_file']) || $_FILES['document_file']['error'] === UPLOAD_ERR_NO_FILE) {
    setFlash('error', 'Please select a file to upload.');
    header('Location: view_student.php?id=' . $studentId);
    exit;
}

$file = $_FILES['document_file'];
if ($file['error'] !== UPLOAD_ERR_OK) {
    setFlash('error', 'File upload error code: ' . $file['error']);
    header('Location: view_student.php?id=' . $studentId);
    exit;
}

// Size check (5MB max)
$maxBytes = 5 * 1024 * 1024;
if ($file['size'] > $maxBytes) {
    setFlash('error', 'File exceeds the 5MB size limit.');
    header('Location: view_student.php?id=' . $studentId);
    exit;
}

// MIME & Extension check using fileinfo
$finfo = new finfo(FILEINFO_MIME_TYPE);
$mime = $finfo->file($file['tmp_name']);

$allowedMimes = [
    'application/pdf'  => 'pdf',
    'image/jpeg'       => 'jpg',
    'image/pjpeg'      => 'jpg',
    'image/png'        => 'png',
    'image/webp'       => 'webp'
];

if (!array_key_exists($mime, $allowedMimes)) {
    setFlash('error', 'Disallowed file type (' . e($mime) . '). Only PDF and standard image files (JPG, PNG, WebP) are permitted.');
    header('Location: view_student.php?id=' . $studentId);
    exit;
}

// Allowed category check
$category = in_array($_POST['category'] ?? '', ['profile_image', 'id_proof', 'certificate', 'other']) 
            ? $_POST['category'] 
            : 'other';

$ext = $allowedMimes[$mime];
$subfolder = ($category === 'profile_image') ? 'profile_images' : 'documents';
$storedName = 'doc_' . bin2hex(random_bytes(10)) . '.' . $ext;
$targetDir = __DIR__ . '/uploads/' . $subfolder;

if (!is_dir($targetDir)) {
    mkdir($targetDir, 0755, true);
}

$targetFile = $targetDir . '/' . $storedName;
$relativePath = 'uploads/' . $subfolder . '/' . $storedName;

if (!move_uploaded_file($file['tmp_name'], $targetFile)) {
    setFlash('error', 'Failed to store uploaded file on server disk.');
    header('Location: view_student.php?id=' . $studentId);
    exit;
}

try {
    $insertDoc = $pdo->prepare("INSERT INTO student_documents 
                                (student_id, original_filename, stored_filename, file_path, mime_type, file_size, document_category, uploaded_at)
                                VALUES (:sid, :orig, :stored, :path, :mime, :size, :cat, NOW())");
    $insertDoc->execute([
        ':sid'    => $studentId,
        ':orig'   => basename($file['name']),
        ':stored' => $storedName,
        ':path'   => $relativePath,
        ':mime'   => $mime,
        ':size'   => (int)$file['size'],
        ':cat'    => $category
    ]);

    // If uploading a new profile image, also update students.profile_image
    if ($category === 'profile_image') {
        $updateStd = $pdo->prepare("UPDATE students SET profile_image = :pic WHERE id = :sid");
        $updateStd->execute([':pic' => $storedName, ':sid' => $studentId]);
    }

    setFlash('success', 'Document "' . basename($file['name']) . '" uploaded successfully.');
} catch (PDOException $e) {
    // If DB insert failed, remove orphaned file
    @unlink($targetFile);
    setFlash('error', 'Database error recording document metadata: ' . $e->getMessage());
}

header('Location: view_student.php?id=' . $studentId);
exit;
