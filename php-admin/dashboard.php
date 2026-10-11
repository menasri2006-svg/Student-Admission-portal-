<?php
/**
 * Admin Dashboard & Student Management Table
 * CO4: Student CRUD, Search, Dashboard Stats, Responsive Table
 */
$pageTitle = 'Admission Dashboard';
$activePage = 'dashboard';

require_once __DIR__ . '/includes/header.php';

$pdo = getDbConnection();

// Search keyword
$search = trim($_GET['search'] ?? '');

// 1. Fetch Summary Statistics
$totalStudents = 0;
$totalDocuments = 0;
$courseCounts = [];
$statusCounts = ['Approved' => 0, 'Pending' => 0, 'Rejected' => 0];

try {
    // Total students count
    $totalStudents = (int)$pdo->query("SELECT COUNT(*) FROM students")->fetchColumn();

    // Total documents count
    $totalDocuments = (int)$pdo->query("SELECT COUNT(*) FROM student_documents")->fetchColumn();

    // Status breakdown
    $statusStmt = $pdo->query("SELECT status, COUNT(*) as cnt FROM students GROUP BY status");
    while ($row = $statusStmt->fetch()) {
        $statusCounts[$row['status']] = (int)$row['cnt'];
    }

    // Course summary breakdown
    $courseStmt = $pdo->query("SELECT course, COUNT(*) as cnt FROM students GROUP BY course ORDER BY cnt DESC");
    $courseCounts = $courseStmt->fetchAll();

    // 2. Fetch Students (with optional search)
    if (!empty($search)) {
        $query = "SELECT s.*, 
                         (SELECT COUNT(*) FROM student_documents d WHERE d.student_id = s.id) AS document_count
                  FROM students s
                  WHERE s.name LIKE :search_name OR s.roll_number LIKE :search_roll OR s.email LIKE :search_email
                  ORDER BY s.id DESC";
        $stmt = $pdo->prepare($query);
        $term = '%' . $search . '%';
        $stmt->execute([
            ':search_name' => $term,
            ':search_roll' => $term,
            ':search_email' => $term
        ]);
        $students = $stmt->fetchAll();
    } else {
        $query = "SELECT s.*, 
                         (SELECT COUNT(*) FROM student_documents d WHERE d.student_id = s.id) AS document_count
                  FROM students s
                  ORDER BY s.id DESC";
        $students = $pdo->query($query)->fetchAll();
    }

} catch (PDOException $e) {
    echo '<div class="alert alert-error">Database query error: ' . e($e->getMessage()) . '</div>';
    $students = [];
}
?>

<!-- Statistics Overview Cards -->
<section class="stats-grid" aria-label="Portal Statistics">
    <div class="stat-card">
        <div class="stat-icon icon-blue">&#128101;</div>
        <div class="stat-info">
            <div class="stat-value"><?= number_format($totalStudents) ?></div>
            <div class="stat-title">Total Enrolled Students</div>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-icon icon-teal">&#128196;</div>
        <div class="stat-info">
            <div class="stat-value"><?= number_format($totalDocuments) ?></div>
            <div class="stat-title">Uploaded Documents</div>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-icon icon-amber">&#9203;</div>
        <div class="stat-info">
            <div class="stat-value"><?= number_format($statusCounts['Pending'] ?? 0) ?></div>
            <div class="stat-title">Pending Approvals</div>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-icon icon-indigo">&#9989;</div>
        <div class="stat-info">
            <div class="stat-value"><?= number_format($statusCounts['Approved'] ?? 0) ?></div>
            <div class="stat-title">Verified Admissions</div>
        </div>
    </div>
</section>

<!-- Course Distribution Summary -->
<?php if (!empty($courseCounts)): ?>
<div class="card" style="margin-bottom: 2rem;">
    <div class="card-header-bar">
        <h2 class="card-title">Enrollment Distribution by Degree Program</h2>
    </div>
    <div class="card-body">
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <?php foreach ($courseCounts as $cc): ?>
                <div style="flex: 1; min-width: 200px; background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 0.9rem 1.1rem;">
                    <div style="font-size: 0.82rem; color: var(--text-secondary);"><?= e($cc['course']) ?></div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: var(--primary); margin-top: 0.2rem;">
                        <?= (int)$cc['cnt'] ?> <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-secondary);">students</span>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Student Directory Table Card -->
<div class="card" id="students-table">
    <div class="card-header-bar">
        <div>
            <h2 class="card-title">Student Records Management</h2>
            <p style="font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.15rem;">
                Showing <?= count($students) ?> <?= !empty($search) ? 'filtered results' : 'registered candidates' ?>
            </p>
        </div>

        <!-- Search Bar -->
        <form method="GET" action="dashboard.php" class="search-form">
            <input type="text" name="search" class="search-input" 
                   placeholder="Search name, roll, email..." 
                   value="<?= e($search) ?>">
            <button type="submit" class="btn-primary btn-sm">&#128269; Search</button>
            <?php if (!empty($search)): ?>
                <a href="dashboard.php" class="btn-sm btn-view" title="Clear filter">Clear</a>
            <?php endif; ?>
        </form>
    </div>

    <div class="table-responsive">
        <?php if (empty($students)): ?>
            <div class="empty-state">
                <div class="empty-state-icon">&#128203;</div>
                <h3>No Student Records Found</h3>
                <p><?= !empty($search) ? 'No students matched the query "' . e($search) . '". Try a different search term.' : 'No student applications have been submitted yet.' ?></p>
                <div style="margin-top: 1rem;">
                    <a href="add_student.php" class="btn-teal btn-sm">+ Enroll First Student</a>
                </div>
            </div>
        <?php else: ?>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Student Name & Photo</th>
                        <th>Roll Number</th>
                        <th>Email Address</th>
                        <th>Course / Program</th>
                        <th>Documents</th>
                        <th>Status</th>
                        <th>Registered Date</th>
                        <th style="text-align: right;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($students as $s): ?>
                        <tr>
                            <td>#<?= (int)$s['id'] ?></td>
                            <td>
                                <div class="student-avatar-cell">
                                    <?php if (!empty($s['profile_image'])): ?>
                                        <img src="download_document.php?profile=<?= urlencode($s['profile_image']) ?>" 
                                             alt="<?= e($s['name']) ?>" 
                                             class="student-img-tiny"
                                             onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'38\' height=\'38\' fill=\'%23cbd5e1\' viewBox=\'0 0 16 16\'><circle cx=\'8\' cy=\'8\' r=\'8\'/></svg>'">
                                    <?php else: ?>
                                        <div class="student-img-tiny" style="display: flex; align-items: center; justify-content: center; font-weight: bold; color: #475569; font-size: 0.85rem;">
                                            <?= strtoupper(substr($s['name'], 0, 1)) ?>
                                        </div>
                                    <?php endif; ?>
                                    <div>
                                        <strong><a href="view_student.php?id=<?= (int)$s['id'] ?>" style="color: var(--primary); text-decoration: none;"><?= e($s['name']) ?></a></strong>
                                    </div>
                                </div>
                            </td>
                            <td><code><?= e($s['roll_number']) ?></code></td>
                            <td><?= e($s['email']) ?></td>
                            <td><?= e($s['course']) ?></td>
                            <td>
                                <span style="font-size: 0.85rem; color: #475569;">
                                    &#128206; <?= (int)$s['document_count'] ?> files
                                </span>
                            </td>
                            <td>
                                <?php
                                    $statusClass = 'badge-pending';
                                    if ($s['status'] === 'Approved') $statusClass = 'badge-approved';
                                    elseif ($s['status'] === 'Rejected') $statusClass = 'badge-rejected';
                                ?>
                                <span class="badge <?= $statusClass ?>"><?= e($s['status']) ?></span>
                            </td>
                            <td style="color: var(--text-secondary); font-size: 0.85rem;">
                                <?= date('M d, Y', strtotime($s['registration_date'])) ?>
                            </td>
                            <td style="text-align: right;">
                                <div class="action-btn-group" style="justify-content: flex-end;">
                                    <a href="view_student.php?id=<?= (int)$s['id'] ?>" class="btn-sm btn-view" title="View Profile">View</a>
                                    <a href="edit_student.php?id=<?= (int)$s['id'] ?>" class="btn-sm btn-edit" title="Edit Student">Edit</a>
                                    <form method="POST" action="delete_student.php" style="display: inline;" 
                                          onsubmit="return confirmDelete('<?= addslashes(e($s['name'])) ?>', '<?= addslashes(e($s['roll_number'])) ?>');">
                                        <?php csrfInput(); ?>
                                        <input type="hidden" name="id" value="<?= (int)$s['id'] ?>">
                                        <button type="submit" class="btn-sm btn-delete" title="Delete Student Record">Delete</button>
                                    </form>
                                </div>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
