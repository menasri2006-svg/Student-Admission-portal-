<?php
/**
 * View Student Profile & Document Management
 * Displays full student profile details, associated documents, and upload interface
 */
$pageTitle = 'Student Profile';
$activePage = 'students';

require_once __DIR__ . '/includes/header.php';

$pdo = getDbConnection();
$studentId = (int)($_GET['id'] ?? 0);

if ($studentId <= 0) {
    setFlash('error', 'Invalid student identifier provided.');
    header('Location: dashboard.php');
    exit;
}

// Fetch Student
$stmt = $pdo->prepare("SELECT * FROM students WHERE id = :id LIMIT 1");
$stmt->execute([':id' => $studentId]);
$student = $stmt->fetch();

if (!$student) {
    setFlash('error', 'Student record not found.');
    header('Location: dashboard.php');
    exit;
}

// Fetch all documents associated with this student
$docStmt = $pdo->prepare("SELECT * FROM student_documents WHERE student_id = :id ORDER BY uploaded_at DESC");
$docStmt->execute([':id' => $studentId]);
$documents = $docStmt->fetchAll();
?>

<div style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
    <a href="dashboard.php" class="btn-sm btn-view">&larr; Back to Student Records</a>
    <div style="display: flex; gap: 0.5rem;">
        <a href="edit_student.php?id=<?= $studentId ?>" class="btn-sm btn-edit">&#9998; Edit Student</a>
        <form method="POST" action="delete_student.php" style="display: inline;" 
              onsubmit="return confirmDelete('<?= addslashes(e($student['name'])) ?>', '<?= addslashes(e($student['roll_number'])) ?>');">
            <?php csrfInput(); ?>
            <input type="hidden" name="id" value="<?= $studentId ?>">
            <button type="submit" class="btn-sm btn-delete">&#128465; Delete Student</button>
        </form>
    </div>
</div>

<div class="profile-view-layout">
    
    <!-- Left Column: Student Avatar & Summary -->
    <div class="profile-card-side">
        <?php if (!empty($student['profile_image'])): ?>
            <img src="download_document.php?profile=<?= urlencode($student['profile_image']) ?>" 
                 alt="<?= e($student['name']) ?>" 
                 class="profile-avatar-large"
                 onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'130\' height=\'130\' fill=\'%23cbd5e1\' viewBox=\'0 0 16 16\'><circle cx=\'8\' cy=\'8\' r=\'8\'/></svg>'">
        <?php else: ?>
            <div class="profile-avatar-large" style="display: flex; align-items: center; justify-content: center; background: #e2e8f0; font-size: 3rem; color: #475569; font-weight: bold;">
                <?= strtoupper(substr($student['name'], 0, 1)) ?>
            </div>
        <?php endif; ?>

        <h2 class="profile-name"><?= e($student['name']) ?></h2>
        <div class="profile-roll">Roll No: <code><?= e($student['roll_number']) ?></code></div>
        
        <?php
            $statusClass = 'badge-pending';
            if ($student['status'] === 'Approved') $statusClass = 'badge-approved';
            elseif ($student['status'] === 'Rejected') $statusClass = 'badge-rejected';
        ?>
        <div style="margin-bottom: 1.5rem;">
            <span class="badge <?= $statusClass ?>" style="font-size: 0.85rem; padding: 0.4rem 0.9rem;">
                <?= e($student['status']) ?>
            </span>
        </div>

        <div style="text-align: left; font-size: 0.86rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--text-secondary); display: block;">System ID:</span>
                <strong>#<?= (int)$student['id'] ?></strong>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--text-secondary); display: block;">Email:</span>
                <strong style="word-break: break-all;"><?= e($student['email']) ?></strong>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--text-secondary); display: block;">Program / Branch:</span>
                <strong><?= e($student['course']) ?></strong>
            </div>
            <div>
                <span style="color: var(--text-secondary); display: block;">Registered On:</span>
                <strong><?= date('F j, Y, g:i A', strtotime($student['registration_date'])) ?></strong>
            </div>
        </div>
    </div>

    <!-- Right Column: Documents and Uploads -->
    <div>
        
        <!-- Document Upload Card -->
        <div class="card" style="margin-bottom: 1.5rem;">
            <div class="card-header-bar">
                <h3 class="card-title">+ Attach New Student Document</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="upload_document.php" enctype="multipart/form-data" style="display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-end;">
                    <?php csrfInput(); ?>
                    <input type="hidden" name="student_id" value="<?= $studentId ?>">

                    <div style="flex: 1; min-width: 180px;">
                        <label style="font-size: 0.82rem; font-weight: 600; display: block; margin-bottom: 0.3rem;">Document Category</label>
                        <select name="category" class="input-admin" style="width: 100%;" required>
                            <option value="id_proof">Identity Proof (Aadhaar / Voter ID)</option>
                            <option value="certificate">Academic Certificate / Marksheet</option>
                            <option value="profile_image">Profile Photograph</option>
                            <option value="other">Other Official Document</option>
                        </select>
                    </div>

                    <div style="flex: 2; min-width: 220px;">
                        <label style="font-size: 0.82rem; font-weight: 600; display: block; margin-bottom: 0.3rem;">Select File (PDF, JPG, PNG &le; 5MB)</label>
                        <input type="file" name="document_file" class="input-admin" style="width: 100%;" required accept=".pdf,image/jpeg,image/png,image/webp">
                    </div>

                    <div>
                        <button type="submit" class="btn-teal" style="padding: 0.65rem 1.25rem;">Upload File</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Associated Documents List -->
        <div class="card">
            <div class="card-header-bar">
                <h3 class="card-title">Stored Documents &amp; Credentials (<?= count($documents) ?>)</h3>
            </div>
            <div class="card-body" style="padding: 0;">
                <?php if (empty($documents)): ?>
                    <div class="empty-state" style="padding: 2.5rem 1rem;">
                        <div class="empty-state-icon">&#128193;</div>
                        <h4>No Documents Uploaded Yet</h4>
                        <p>Upload the candidate's certificates or ID proofs using the form above.</p>
                    </div>
                <?php else: ?>
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Document Category</th>
                                    <th>Original Name</th>
                                    <th>MIME Type</th>
                                    <th>Size</th>
                                    <th>Uploaded At</th>
                                    <th style="text-align: right;">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($documents as $doc): ?>
                                    <tr>
                                        <td>#<?= (int)$doc['id'] ?></td>
                                        <td>
                                            <span class="badge" style="background: #e0f2fe; color: #0369a1; text-transform: uppercase; font-size: 0.72rem;">
                                                <?= e(str_replace('_', ' ', $doc['document_category'])) ?>
                                            </span>
                                        </td>
                                        <td>
                                            <strong><?= e($doc['original_filename']) ?></strong>
                                            <div style="font-size: 0.72rem; color: #94a3b8;"><?= e($doc['stored_filename']) ?></div>
                                        </td>
                                        <td><code><?= e($doc['mime_type']) ?></code></td>
                                        <td><?= number_format($doc['file_size'] / 1024, 1) ?> KB</td>
                                        <td style="font-size: 0.82rem; color: var(--text-secondary);">
                                            <?= date('M d, Y H:i', strtotime($doc['uploaded_at'])) ?>
                                        </td>
                                        <td style="text-align: right;">
                                            <div class="action-btn-group" style="justify-content: flex-end;">
                                                <!-- Safe Stream / Preview Link -->
                                                <a href="download_document.php?id=<?= (int)$doc['id'] ?>" target="_blank" class="btn-sm btn-view" title="Preview File">
                                                    &#128065; Preview
                                                </a>
                                                <!-- Safe Force Download Link -->
                                                <a href="download_document.php?id=<?= (int)$doc['id'] ?>&download=1" class="btn-sm btn-edit" title="Download File">
                                                    &#128190; Download
                                                </a>
                                                <!-- Delete Document -->
                                                <form method="POST" action="upload_document.php" style="display: inline;" 
                                                      onsubmit="return confirmDocDelete('<?= addslashes(e($doc['original_filename'])) ?>');">
                                                    <?php csrfInput(); ?>
                                                    <input type="hidden" name="action" value="delete">
                                                    <input type="hidden" name="doc_id" value="<?= (int)$doc['id'] ?>">
                                                    <input type="hidden" name="student_id" value="<?= $studentId ?>">
                                                    <button type="submit" class="btn-sm btn-delete" title="Delete Document">&#128465;</button>
                                                </form>
                                            </div>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                <?php endif; ?>
            </div>
        </div>

    </div>

</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
