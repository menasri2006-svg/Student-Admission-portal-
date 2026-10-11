<?php
/**
 * Add New Student (Admin Panel)
 * Supports student creation, password hashing, and multiple document uploads
 */
$pageTitle = 'Enroll New Student';
$activePage = 'add_student';

require_once __DIR__ . '/includes/header.php';

$errors = [];
$name = '';
$rollNumber = '';
$email = '';
$course = '';
$status = 'Approved';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!validateCsrfToken($_POST['csrf_token'] ?? '')) {
        $errors['csrf'] = 'Invalid CSRF token session. Please submit the form again.';
    } else {
        $name = trim($_POST['name'] ?? '');
        $rollNumber = trim($_POST['roll_number'] ?? '');
        $email = trim($_POST['email'] ?? '');
        $course = trim($_POST['course'] ?? '');
        $status = in_array($_POST['status'] ?? '', ['Approved', 'Pending', 'Rejected']) ? $_POST['status'] : 'Approved';
        $password = $_POST['password'] ?? '';

        // Validation
        if (empty($name) || strlen($name) < 3) {
            $errors['name'] = 'Full name must be at least 3 characters.';
        }
        if (empty($rollNumber) || !preg_match('/^[A-Za-z0-9-_]{3,20}$/', $rollNumber)) {
            $errors['roll_number'] = 'Roll number must be 3-20 alphanumeric characters.';
        }
        if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $errors['email'] = 'A valid email address is required.';
        }
        if (empty($course)) {
            $errors['course'] = 'Please select a valid degree course.';
        }
        if (empty($password) || strlen($password) < 6) {
            $errors['password'] = 'Password must be at least 6 characters.';
        }

        // Duplicate checks
        if (empty($errors)) {
            $pdo = getDbConnection();
            $checkStmt = $pdo->prepare("SELECT id FROM students WHERE roll_number = :roll OR email = :email LIMIT 1");
            $checkStmt->execute([':roll' => $rollNumber, ':email' => $email]);
            if ($checkStmt->fetch()) {
                $errors['general'] = 'A student with this Roll Number or Email already exists in the system.';
            }
        }

        // Process profile image upload
        $storedProfilePic = null;
        if (empty($errors) && isset($_FILES['profile_pic']) && $_FILES['profile_pic']['error'] !== UPLOAD_ERR_NO_FILE) {
            $pic = $_FILES['profile_pic'];
            if ($pic['error'] === UPLOAD_ERR_OK && $pic['size'] <= 2 * 1024 * 1024) {
                $finfo = new finfo(FILEINFO_MIME_TYPE);
                $mime = $finfo->file($pic['tmp_name']);
                $allowed = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];
                if (isset($allowed[$mime])) {
                    $ext = $allowed[$mime];
                    $storedProfilePic = 'std_' . bin2hex(random_bytes(10)) . '.' . $ext;
                    $dest = __DIR__ . '/uploads/profile_images/' . $storedProfilePic;
                    move_uploaded_file($pic['tmp_name'], $dest);
                } else {
                    $errors['profile_pic'] = 'Profile image must be JPEG, PNG, or WebP.';
                }
            } elseif ($pic['size'] > 2 * 1024 * 1024) {
                $errors['profile_pic'] = 'Profile image must be less than 2MB.';
            }
        }

        // Insert Student if all clear
        if (empty($errors)) {
            try {
                $pdo = getDbConnection();
                $passHash = password_hash($password, PASSWORD_BCRYPT);
                $insert = $pdo->prepare("INSERT INTO students (name, roll_number, email, course, password_hash, profile_image, status, registration_date) 
                                         VALUES (:name, :roll, :email, :course, :pass, :pic, :status, NOW())");
                $insert->execute([
                    ':name'   => $name,
                    ':roll'   => $rollNumber,
                    ':email'  => $email,
                    ':course' => $course,
                    ':pass'   => $passHash,
                    ':pic'    => $storedProfilePic,
                    ':status' => $status
                ]);
                $newId = (int)$pdo->lastInsertId();

                // Record profile picture in student_documents
                if ($storedProfilePic) {
                    $docStmt = $pdo->prepare("INSERT INTO student_documents (student_id, original_filename, stored_filename, file_path, mime_type, file_size, document_category) 
                                              VALUES (:sid, :orig, :stored, :path, :mime, :size, 'profile_image')");
                    $docStmt->execute([
                        ':sid'    => $newId,
                        ':orig'   => basename($_FILES['profile_pic']['name']),
                        ':stored' => $storedProfilePic,
                        ':path'   => 'uploads/profile_images/' . $storedProfilePic,
                        ':mime'   => $mime ?? 'image/jpeg',
                        ':size'   => (int)$_FILES['profile_pic']['size']
                    ]);
                }

                // Process optional ID Proof / Document
                if (isset($_FILES['student_doc']) && $_FILES['student_doc']['error'] !== UPLOAD_ERR_NO_FILE) {
                    $docFile = $_FILES['student_doc'];
                    if ($docFile['error'] === UPLOAD_ERR_OK && $docFile['size'] <= 5 * 1024 * 1024) {
                        $finfo = new finfo(FILEINFO_MIME_TYPE);
                        $dMime = $finfo->file($docFile['tmp_name']);
                        $allowedDocs = [
                            'application/pdf' => 'pdf',
                            'image/jpeg'      => 'jpg',
                            'image/png'       => 'png'
                        ];
                        if (isset($allowedDocs[$dMime])) {
                            $dExt = $allowedDocs[$dMime];
                            $storedDocName = 'doc_' . bin2hex(random_bytes(10)) . '.' . $dExt;
                            $destDoc = __DIR__ . '/uploads/documents/' . $storedDocName;
                            if (move_uploaded_file($docFile['tmp_name'], $destDoc)) {
                                $category = in_array($_POST['doc_category'] ?? '', ['id_proof', 'certificate']) ? $_POST['doc_category'] : 'id_proof';
                                $docStmt = $pdo->prepare("INSERT INTO student_documents (student_id, original_filename, stored_filename, file_path, mime_type, file_size, document_category) 
                                                          VALUES (:sid, :orig, :stored, :path, :mime, :size, :cat)");
                                $docStmt->execute([
                                    ':sid'    => $newId,
                                    ':orig'   => basename($docFile['name']),
                                    ':stored' => $storedDocName,
                                    ':path'   => 'uploads/documents/' . $storedDocName,
                                    ':mime'   => $dMime,
                                    ':size'   => (int)$docFile['size'],
                                    ':cat'    => $category
                                ]);
                            }
                        }
                    }
                }

                setFlash('success', 'Student record created successfully for ' . $name . ' (' . $rollNumber . ').');
                header('Location: view_student.php?id=' . $newId);
                exit;

            } catch (PDOException $e) {
                $errors['general'] = 'Database error: ' . $e->getMessage();
            }
        }
    }
}
?>

<div class="card">
    <div class="card-header-bar">
        <h2 class="card-title">Enroll New Student</h2>
        <a href="dashboard.php" class="btn-sm btn-view">&larr; Back to Student List</a>
    </div>

    <div class="card-body">
        <?php if (!empty($errors['general'])): ?>
            <div class="alert alert-error">&#9888; <?= e($errors['general']) ?></div>
        <?php endif; ?>

        <form method="POST" action="add_student.php" enctype="multipart/form-data" class="admin-form">
            <?php csrfInput(); ?>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="name">Student Full Name *</label>
                    <input type="text" id="name" name="name" class="input-admin" required value="<?= e($name) ?>" placeholder="e.g. Diya Sharma">
                    <?php if (!empty($errors['name'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['name']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="roll_number">Roll / Application Number *</label>
                    <input type="text" id="roll_number" name="roll_number" class="input-admin" required value="<?= e($rollNumber) ?>" placeholder="e.g. CS2026-108">
                    <?php if (!empty($errors['roll_number'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['roll_number']) ?></span><?php endif; ?>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="email">Student Email *</label>
                    <input type="email" id="email" name="email" class="input-admin" required value="<?= e($email) ?>" placeholder="student@example.edu">
                    <?php if (!empty($errors['email'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['email']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="course">Degree Program *</label>
                    <select id="course" name="course" class="input-admin" required>
                        <option value="" disabled <?= empty($course) ? 'selected' : '' ?>>-- Select Program --</option>
                        <option value="B.Tech Computer Science" <?= ($course === 'B.Tech Computer Science') ? 'selected' : '' ?>>B.Tech Computer Science</option>
                        <option value="B.Tech Information Technology" <?= ($course === 'B.Tech Information Technology') ? 'selected' : '' ?>>B.Tech Information Technology</option>
                        <option value="B.Tech Electronics & Comm" <?= ($course === 'B.Tech Electronics & Comm') ? 'selected' : '' ?>>B.Tech Electronics & Comm</option>
                        <option value="B.Tech Artificial Intelligence" <?= ($course === 'B.Tech Artificial Intelligence') ? 'selected' : '' ?>>B.Tech Artificial Intelligence</option>
                        <option value="M.Tech Software Engineering" <?= ($course === 'M.Tech Software Engineering') ? 'selected' : '' ?>>M.Tech Software Engineering</option>
                        <option value="MCA Computer Applications" <?= ($course === 'MCA Computer Applications') ? 'selected' : '' ?>>MCA Computer Applications</option>
                    </select>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="password">Account Password *</label>
                    <input type="password" id="password" name="password" class="input-admin" required placeholder="Minimum 6 characters">
                    <?php if (!empty($errors['password'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['password']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="status">Admission Status</label>
                    <select id="status" name="status" class="input-admin">
                        <option value="Approved" <?= ($status === 'Approved') ? 'selected' : '' ?>>Approved</option>
                        <option value="Pending" <?= ($status === 'Pending') ? 'selected' : '' ?>>Pending Review</option>
                        <option value="Rejected" <?= ($status === 'Rejected') ? 'selected' : '' ?>>Rejected</option>
                    </select>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="profile_pic">Candidate Profile Picture</label>
                    <input type="file" id="profile_pic" name="profile_pic" accept="image/jpeg,image/png,image/webp" class="input-admin">
                    <span style="font-size: 0.78rem; color: var(--text-secondary);">JPEG, PNG, WebP up to 2MB</span>
                    <?php if (!empty($errors['profile_pic'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['profile_pic']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="student_doc">Identity Proof / Academic Document</label>
                    <input type="file" id="student_doc" name="student_doc" accept=".pdf,image/jpeg,image/png" class="input-admin">
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.35rem;">
                        <select name="doc_category" class="input-admin" style="padding: 0.35rem 0.6rem; font-size: 0.8rem;">
                            <option value="id_proof">Category: ID Proof (Aadhaar / Passport)</option>
                            <option value="certificate">Category: Certificate / Marksheet</option>
                            <option value="other">Category: Other Document</option>
                        </select>
                    </div>
                </div>
            </div>

            <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                <button type="submit" class="btn-teal">Save Student Record</button>
                <a href="dashboard.php" class="btn-primary" style="background: #e2e8f0; color: #334155;">Cancel</a>
            </div>
        </form>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
