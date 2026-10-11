<?php
/**
 * Student Registration Endpoint
 * Performs server-side validation, password hashing, secure file upload,
 * and database insertion into the shared student_portal database.
 */

// Disable direct error display to clients for security, log instead
ini_set('display_errors', '0');
error_reporting(E_ALL);

header('Content-Type: application/json; charset=utf-8');

// Include shared database connection
require_once __DIR__ . '/../php-admin/config/database.php';

$response = [
    'status' => 'error',
    'message' => 'An unexpected error occurred.',
    'errors' => []
];

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    $response['message'] = 'Only POST requests are permitted.';
    echo json_encode($response);
    exit;
}

// 1. Sanitize & Collect Input
$name = trim($_POST['name'] ?? '');
$rollNumber = trim($_POST['roll_number'] ?? '');
$email = trim($_POST['email'] ?? '');
$course = trim($_POST['course'] ?? '');
$password = $_POST['password'] ?? '';
$confirmPassword = $_POST['confirm_password'] ?? '';

$errors = [];

// 2. Server-Side Validation Rules
if (empty($name)) {
    $errors['name'] = 'Full name is required.';
} elseif (strlen($name) < 3) {
    $errors['name'] = 'Full name must be at least 3 characters.';
} elseif (!preg_match("/^[a-zA-Z\s.'-]+$/", $name)) {
    $errors['name'] = 'Name contains invalid characters.';
}

if (empty($rollNumber)) {
    $errors['roll_number'] = 'Roll number is required.';
} elseif (!preg_match('/^[A-Za-z0-9-_]{3,20}$/', $rollNumber)) {
    $errors['roll_number'] = 'Roll number must be 3-20 alphanumeric characters.';
}

if (empty($email)) {
    $errors['email'] = 'Email address is required.';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Invalid email address format.';
}

$validCourses = [
    'B.Tech Computer Science',
    'B.Tech Information Technology',
    'B.Tech Electronics & Comm',
    'B.Tech Artificial Intelligence',
    'M.Tech Software Engineering',
    'MCA Computer Applications'
];
if (empty($course) || !in_array($course, $validCourses, true)) {
    $errors['course'] = 'Please select a valid academic program.';
}

// Password rules: min 8, upper, lower, digit, special
if (empty($password)) {
    $errors['password'] = 'Password is required.';
} else {
    $hasLen = strlen($password) >= 8;
    $hasUpper = preg_match('/[A-Z]/', $password);
    $hasLower = preg_match('/[a-z]/', $password);
    $hasDigit = preg_match('/[0-9]/', $password);
    $hasSpecial = preg_match('/[^A-Za-z0-9]/', $password);

    if (!$hasLen || !$hasUpper || !$hasLower || !$hasDigit || !$hasSpecial) {
        $errors['password'] = 'Password must be at least 8 characters and contain uppercase, lowercase, number, and special character.';
    }
}

if ($password !== $confirmPassword) {
    $errors['confirm_password'] = 'Passwords do not match.';
}

// 3. Handle File Upload (Profile Picture)
$storedFileName = null;
$originalFileName = null;
$fileMimeType = null;
$fileSizeBytes = 0;
$uploadRelativePath = null;

if (isset($_FILES['profile_pic']) && $_FILES['profile_pic']['error'] !== UPLOAD_ERR_NO_FILE) {
    $file = $_FILES['profile_pic'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $errors['profile_pic'] = 'File upload failed with error code ' . $file['error'];
    } else {
        $maxSize = 2 * 1024 * 1024; // 2MB
        if ($file['size'] > $maxSize) {
            $errors['profile_pic'] = 'Uploaded file exceeds the maximum 2MB limit.';
        } else {
            // Verify MIME type using fileinfo
            $finfo = new finfo(FILEINFO_MIME_TYPE);
            $mime = $finfo->file($file['tmp_name']);
            $allowedMimes = [
                'image/jpeg' => 'jpg',
                'image/pjpeg' => 'jpg',
                'image/png'  => 'png',
                'image/webp' => 'webp'
            ];

            if (!array_key_exists($mime, $allowedMimes)) {
                $errors['profile_pic'] = 'Invalid file type. Only JPEG, PNG, and WebP images are permitted.';
            } else {
                $originalFileName = basename($file['name']);
                $ext = $allowedMimes[$mime];
                $storedFileName = 'std_' . bin2hex(random_bytes(10)) . '.' . $ext;
                $uploadDir = __DIR__ . '/../php-admin/uploads/profile_images/';

                if (!is_dir($uploadDir)) {
                    mkdir($uploadDir, 0755, true);
                }

                $targetPath = $uploadDir . $storedFileName;
                if (!move_uploaded_file($file['tmp_name'], $targetPath)) {
                    $errors['profile_pic'] = 'Failed to safely store the uploaded file.';
                } else {
                    $fileMimeType = $mime;
                    $fileSizeBytes = $file['size'];
                    $uploadRelativePath = 'uploads/profile_images/' . $storedFileName;
                }
            }
        }
    }
}

// Return early if validation errors exist
if (!empty($errors)) {
    http_response_code(422);
    $response['errors'] = $errors;
    $response['message'] = reset($errors);
    echo json_encode($response);
    exit;
}

// 4. Database Operations with Prepared Statements
try {
    $pdo = getDbConnection();

    // Check for duplicate Roll Number
    $stmtRoll = $pdo->prepare("SELECT id FROM students WHERE roll_number = :roll_number LIMIT 1");
    $stmtRoll->execute([':roll_number' => $rollNumber]);
    if ($stmtRoll->fetch()) {
        http_response_code(409);
        $response['errors']['roll_number'] = 'This Roll Number is already registered.';
        $response['message'] = 'Roll Number "' . htmlspecialchars($rollNumber) . '" is already registered.';
        echo json_encode($response);
        exit;
    }

    // Check for duplicate Email
    $stmtEmail = $pdo->prepare("SELECT id FROM students WHERE email = :email LIMIT 1");
    $stmtEmail->execute([':email' => $email]);
    if ($stmtEmail->fetch()) {
        http_response_code(409);
        $response['errors']['email'] = 'This Email address is already registered.';
        $response['message'] = 'Email address "' . htmlspecialchars($email) . '" is already registered.';
        echo json_encode($response);
        exit;
    }

    // Hash password securely with BCRYPT
    $passwordHash = password_hash($password, PASSWORD_BCRYPT);

    // Insert student record
    $insertSql = "INSERT INTO students (roll_number, name, email, course, password_hash, profile_image, status, registration_date)
                  VALUES (:roll_number, :name, :email, :course, :password_hash, :profile_image, 'Approved', NOW())";
    
    $stmtInsert = $pdo->prepare($insertSql);
    $stmtInsert->execute([
        ':roll_number'    => $rollNumber,
        ':name'           => $name,
        ':email'          => $email,
        ':course'         => $course,
        ':password_hash'  => $passwordHash,
        ':profile_image'  => $storedFileName
    ]);

    $newStudentId = (int)$pdo->lastInsertId();

    // If an image was uploaded, register it in student_documents table
    if ($storedFileName && $uploadRelativePath) {
        $docSql = "INSERT INTO student_documents 
                   (student_id, original_filename, stored_filename, file_path, mime_type, file_size, document_category, uploaded_at)
                   VALUES (:student_id, :original_filename, :stored_filename, :file_path, :mime_type, :file_size, 'profile_image', NOW())";
        
        $stmtDoc = $pdo->prepare($docSql);
        $stmtDoc->execute([
            ':student_id'        => $newStudentId,
            ':original_filename' => $originalFileName,
            ':stored_filename'   => $storedFileName,
            ':file_path'         => $uploadRelativePath,
            ':mime_type'         => $fileMimeType,
            ':file_size'         => $fileSizeBytes
        ]);
    }

    // Success response
    $response['status'] = 'success';
    $response['message'] = 'Student application successfully registered!';
    $response['student'] = [
        'id' => $newStudentId,
        'roll_number' => $rollNumber,
        'name' => $name,
        'email' => $email,
        'course' => $course,
        'registration_date' => date('Y-m-d H:i:s')
    ];

    echo json_encode($response);
    exit;

} catch (PDOException $e) {
    http_response_code(500);
    $response['message'] = 'Database error: Unable to complete registration. Check database connection.';
    error_log('Registration DB Error: ' . $e->getMessage());
    echo json_encode($response);
    exit;
}
