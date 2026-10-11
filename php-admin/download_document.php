<?php
/**
 * Secure Document & Image Streaming Endpoint
 * Resolves files via database metadata, prevents path traversal, and enforces authorized access
 */
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/config/database.php';

// Profile images can be loaded in views by authenticated admin or publicly for avatars
$isProfileRequest = !empty($_GET['profile']);
$docId = (int)($_GET['id'] ?? 0);
$forceDownload = !empty($_GET['download']);

// If requesting private documents, enforce admin login
if (!$isProfileRequest) {
    requireAdminLogin();
}

$pdo = getDbConnection();
$filePath = null;
$mimeType = 'application/octet-stream';
$originalName = 'document';

if ($isProfileRequest) {
    // Sanitize profile filename (strictly alphanumeric with extension)
    $cleanProfile = basename($_GET['profile']);
    if (!preg_match('/^[a-zA-Z0-9._-]+$/', $cleanProfile)) {
        http_response_code(400);
        exit('Invalid filename requested.');
    }

    $targetFile = __DIR__ . '/uploads/profile_images/' . $cleanProfile;
    if (!file_exists($targetFile)) {
        // Return 404 or a fallback transparent 1x1 image
        http_response_code(404);
        exit('Profile image not found.');
    }

    $filePath = $targetFile;
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $finfo->file($filePath);
    $originalName = $cleanProfile;

} elseif ($docId > 0) {
    // Look up document via database metadata (Prevents user from passing arbitrary filesystem paths)
    $stmt = $pdo->prepare("SELECT original_filename, stored_filename, file_path, mime_type FROM student_documents WHERE id = :id LIMIT 1");
    $stmt->execute([':id' => $docId]);
    $doc = $stmt->fetch();

    if (!$doc) {
        http_response_code(404);
        exit('Document record not found in system database.');
    }

    $targetFile = __DIR__ . '/' . $doc['file_path'];
    if (!file_exists($targetFile)) {
        http_response_code(404);
        exit('Physical document file is missing from server storage.');
    }

    $filePath = $targetFile;
    $mimeType = $doc['mime_type'];
    $originalName = $doc['original_filename'];

} else {
    http_response_code(400);
    exit('No document or profile identifier provided.');
}

// Security Check: Defense against Path Traversal
// Confirm resolved realpath is strictly located inside the uploads directory
$realFilePath = realpath($filePath);
$uploadsBase = realpath(__DIR__ . '/uploads');

if (!$realFilePath || !$uploadsBase || strpos($realFilePath, $uploadsBase) !== 0) {
    http_response_code(403);
    exit('Access denied: Unauthorized file path.');
}

// Disallow streaming executable file extensions
$disallowed = ['php', 'phtml', 'exe', 'bat', 'sh', 'cmd', 'cgi', 'pl', 'py'];
$ext = strtolower(pathinfo($realFilePath, PATHINFO_EXTENSION));
if (in_array($ext, $disallowed, true)) {
    http_response_code(403);
    exit('Executable files cannot be streamed.');
}

// Clear output buffers
if (ob_get_level()) {
    ob_end_clean();
}

$fileSize = filesize($realFilePath);
$disposition = $forceDownload ? 'attachment' : 'inline';

// Send security and delivery headers
header('Content-Type: ' . $mimeType);
header('Content-Length: ' . $fileSize);
header('Content-Disposition: ' . $disposition . '; filename="' . rawurlencode($originalName) . '"');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: private, max-age=3600');

// Stream file in 8KB chunks
$fp = fopen($realFilePath, 'rb');
if ($fp) {
    while (!feof($fp) && !connection_aborted()) {
        echo fread($fp, 8192);
        flush();
    }
    fclose($fp);
}
exit;
