<?php
/**
 * Edit Student Profile (Admin Panel)
 * Supports updating personal details, status, photo, and password
 */
$pageTitle = 'Edit Student Record';
$activePage = 'students';

require_once __DIR__ . '/includes/header.php';

$pdo = getDbConnection();
$studentId = (int)($_GET['id'] ?? 0);

if ($studentId <= 0) {
    setFlash('error', 'Invalid student identifier provided.');
    header('Location: dashboard.php');
    exit;
}

// Fetch existing student record
$stmt = $pdo->prepare("SELECT * FROM students WHERE id = :id LIMIT 1");
$stmt->execute([':id' => $studentId]);
$student = $stmt->fetch();

if (!$student) {
    setFlash('error', 'Student record not found.');
    header('Location: dashboard.php');
    exit;
}

$errors = [];
$name = $student['name'];
$rollNumber = $student['roll_number'];
$email = $student['email'];
$course = $student['course'];
$status = $student['status'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!validateCsrfToken($_POST['csrf_token'] ?? '')) {
        $errors['csrf'] = 'Invalid CSRF token. Please resubmit the form.';
    } else {
        $name = trim($_POST['name'] ?? '');
        $rollNumber = trim($_POST['roll_number'] ?? '');
        $email = trim($_POST['email'] ?? '');
        $course = trim($_POST['course'] ?? '');
        $status = in_array($_POST['status'] ?? '', ['Approved', 'Pending', 'Rejected']) ? $_POST['status'] : $student['status'];
        $newPassword = $_POST['new_password'] ?? '';

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
            $errors['course'] = 'Please select a degree program.';
        }

        // Check duplicates excluding this student
        if (empty($errors)) {
            $dupCheck = $pdo->prepare("SELECT id FROM students WHERE (roll_number = :roll OR email = :email) AND id != :id LIMIT 1");
            $dupCheck->execute([':roll' => $rollNumber, ':email' => $email, ':id' => $studentId]);
            if ($dupCheck->fetch()) {
                $errors['general'] = 'Another student is already using this Roll Number or Email address.';
            }
        }

        // Handle profile picture update if uploaded
        $storedProfilePic = $student['profile_image'];
        if (empty($errors) && isset($_FILES['profile_pic']) && $_FILES['profile_pic']['error'] !== UPLOAD_ERR_NO_FILE) {
            $pic = $_FILES['profile_pic'];
            if ($pic['error'] === UPLOAD_ERR_OK && $pic['size'] <= 2 * 1024 * 1024) {
                $finfo = new finfo(FILEINFO_MIME_TYPE);
                $mime = $finfo->file($pic['tmp_name']);
                $allowed = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];
                if (isset($allowed[$mime])) {
                    $ext = $allowed[$mime];
                    $newPicName = 'std_' . bin2hex(random_bytes(10)) . '.' . $ext;
                    $dest = __DIR__ . '/uploads/profile_images/' . $newPicName;
                    if (move_uploaded_file($pic['tmp_name'], $dest)) {
                        $storedProfilePic = $newPicName;

                        // Insert new document record
                        $docStmt = $pdo->prepare("INSERT INTO student_documents (student_id, original_filename, stored_filename, file_path, mime_type, file_size, document_category) 
                                                  VALUES (:sid, :orig, :stored, :path, :mime, :size, 'profile_image')");
                        $docStmt->execute([
                            ':sid'    => $studentId,
                            ':orig'   => basename($pic['name']),
                            ':stored' => $newPicName,
                            ':path'   => 'uploads/profile_images/' . $newPicName,
                            ':mime'   => $mime,
                            ':size'   => (int)$pic['size']
                        ]);
                    }
                } else {
                    $errors['profile_pic'] = 'Only JPG, PNG, and WebP images are permitted.';
                }
            }
        }

        // Update database
        if (empty($errors)) {
            try {
                if (!empty($newPassword)) {
                    $newPassHash = password_hash($newPassword, PASSWORD_BCRYPT);
                    $update = $pdo->prepare("UPDATE students SET name = :name, roll_number = :roll, email = :email, course = :course, 
                                             status = :status, profile_image = :pic, password_hash = :pass WHERE id = :id");
                    $update->execute([
                        ':name'   => $name,
                        ':roll'   => $rollNumber,
                        ':email'  => $email,
                        ':course' => $course,
                        ':status' => $status,
                        ':pic'    => $storedProfilePic,
                        ':pass'   => $newPassHash,
                        ':id'     => $studentId
                    ]);
                } else {
                    $update = $pdo->prepare("UPDATE students SET name = :name, roll_number = :roll, email = :email, course = :course, 
                                             status = :status, profile_image = :pic WHERE id = :id");
                    $update->execute([
                        ':name'   => $name,
                        ':roll'   => $rollNumber,
                        ':email'  => $email,
                        ':course' => $course,
                        ':status' => $status,
                        ':pic'    => $storedProfilePic,
                        ':id'     => $studentId
                    ]);
                }

                setFlash('success', 'Student profile for ' . $name . ' (' . $rollNumber . ') updated successfully.');
                header('Location: view_student.php?id=' . $studentId);
                exit;

            } catch (PDOException $e) {
                $errors['general'] = 'Database update error: ' . $e->getMessage();
            }
        }
    }
}
?>

<div class="card">
    <div class="card-header-bar">
        <div>
            <h2 class="card-title">Edit Student Profile: <?= e($student['name']) ?></h2>
            <span style="font-size: 0.85rem; color: var(--text-secondary);">Student ID #<?= $studentId ?> &bull; Roll: <?= e($student['roll_number']) ?></span>
        </div>
        <a href="view_student.php?id=<?= $studentId ?>" class="btn-sm btn-view">&larr; Back to Profile</a>
    </div>

    <div class="card-body">
        <?php if (!empty($errors['general'])): ?>
            <div class="alert alert-error">&#9888; <?= e($errors['general']) ?></div>
        <?php endif; ?>

        <form method="POST" action="edit_student.php?id=<?= $studentId ?>" enctype="multipart/form-data" class="admin-form">
            <?php csrfInput(); ?>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="name">Student Full Name *</label>
                    <input type="text" id="name" name="name" class="input-admin" required value="<?= e($name) ?>">
                    <?php if (!empty($errors['name'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['name']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="roll_number">Roll / Application Number *</label>
                    <input type="text" id="roll_number" name="roll_number" class="input-admin" required value="<?= e($rollNumber) ?>">
                    <?php if (!empty($errors['roll_number'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['roll_number']) ?></span><?php endif; ?>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group-admin">
                    <label for="email">Email Address *</label>
                    <input type="email" id="email" name="email" class="input-admin" required value="<?= e($email) ?>">
                    <?php if (!empty($errors['email'])): ?><span style="color: var(--danger); font-size: 0.8rem;"><?= e($errors['email']) ?></span><?php endif; ?>
                </div>

                <div class="form-group-admin">
                    <label for="course">Degree Program *</label>
                    <select id="course" name="course" class="input-admin" required>
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
                    <label for="status">Admission Status</label>
                    <select id="status" name="status" class="input-admin">
                        <option value="Approved" <?= ($status === 'Approved') ? 'selected' : '' ?>>Approved</option>
                        <option value="Pending" <?= ($status === 'Pending') ? 'selected' : '' ?>>Pending Review</option>
                        <option value="Rejected" <?= ($status === 'Rejected') ? 'selected' : '' ?>>Rejected</option>
                    </select>
                </div>

                <div class="form-group-admin">
                    <label for="new_password">Change Password (Leave blank to keep unchanged)</label>
                    <input type="password" id="new_password" name="new_password" class="input-admin" placeholder="New password (optional)">
                </div>
            </div>

            <div class="form-group-admin">
                <label for="profile_pic">Update Profile Photo</label>
                <?php if (!empty($student['profile_image'])): ?>
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <img src="download_document.php?profile=<?= urlencode($student['profile_image']) ?>" 
                             alt="Current avatar" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">
                        <span style="font-size: 0.85rem; color: var(--text-secondary);">Current photo: <?= e($student['profile_image']) ?></span>
                    </div>
                <?php endif; ?>
                <input type="file" id="profile_pic" name="profile_pic" accept="image/jpeg,image/png,image/webp" class="input-admin">
                <span style="font-size: 0.78rem; color: var(--text-secondary);">Upload new photo to replace current (Max 2MB)</span>
            </div>

            <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                <button type="submit" class="btn-teal">Save Changes</button>
                <a href="view_student.php?id=<?= $studentId ?>" class="btn-primary" style="background: #e2e8f0; color: #334155;">Cancel</a>
            </div>
        </form>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
