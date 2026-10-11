<?php
/**
 * Admin Login Page
 * Handles secure authentication, session fixation prevention, and CSRF protection
 */
require_once __DIR__ . '/includes/auth.php';
require_once __DIR__ . '/config/database.php';

// Redirect if already logged in
if (isAdminLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}

$errorMessage = $_SESSION['flash_error'] ?? '';
unset($_SESSION['flash_error']);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';
    $csrfToken = $_POST['csrf_token'] ?? '';

    if (!validateCsrfToken($csrfToken)) {
        $errorMessage = 'Security validation failed (invalid CSRF token). Please try again.';
    } elseif (empty($username) || empty($password)) {
        $errorMessage = 'Please enter both username and password.';
    } else {
        try {
            $pdo = getDbConnection();
            $stmt = $pdo->prepare("SELECT id, username, password_hash, full_name, email, role FROM admin_users WHERE username = :username LIMIT 1");
            $stmt->execute([':username' => $username]);
            $admin = $stmt->fetch();

            if ($admin && password_verify($password, $admin['password_hash'])) {
                // Prevent session fixation attack
                session_regenerate_id(true);

                // Populate session
                $_SESSION['admin_user_id']   = (int)$admin['id'];
                $_SESSION['admin_username']  = $admin['username'];
                $_SESSION['admin_full_name'] = $admin['full_name'];
                $_SESSION['admin_email']     = $admin['email'];
                $_SESSION['admin_role']      = $admin['role'];

                setFlash('success', 'Welcome back, ' . $admin['full_name'] . '!');
                header('Location: dashboard.php');
                exit;
            } else {
                // Generic error to prevent username enumeration
                $errorMessage = 'Invalid username or password.';
            }
        } catch (PDOException $e) {
            $errorMessage = 'Database connection failure. Please verify MySQL service is running.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Student Admission Portal</title>
    <link rel="stylesheet" href="assets/css/admin.css">
</head>
<body class="login-body">

    <div class="login-card">
        <div class="login-header">
            <div class="sidebar-logo" style="margin: 0 auto 0.75rem auto; width: 44px; height: 44px; font-size: 1.4rem;">A</div>
            <h2>Admission Admin Portal</h2>
            <p>Authorized Academic Staff Access Only</p>
        </div>

        <div class="login-form-wrap">
            <?php if (!empty($errorMessage)): ?>
                <div class="alert alert-error" style="margin-bottom: 1.25rem;">
                    <span>&#9888; <?= e($errorMessage) ?></span>
                </div>
            <?php endif; ?>

            <form method="POST" action="login.php" autocomplete="off">
                <?php csrfInput(); ?>

                <div class="form-group-admin">
                    <label for="username">Admin Username</label>
                    <input type="text" id="username" name="username" class="input-admin" 
                           placeholder="e.g. admin" required autofocus autocomplete="username"
                           value="<?= isset($username) ? e($username) : 'admin' ?>">
                </div>

                <div class="form-group-admin">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" class="input-admin" 
                           placeholder="••••••••••••" required autocomplete="current-password">
                </div>

                <div style="margin-top: 1.5rem;">
                    <button type="submit" class="btn-teal" style="width: 100%; justify-content: center; padding: 0.8rem;">
                        Sign In to Admin Dashboard
                    </button>
                </div>
            </form>

            <div style="margin-top: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: var(--radius-sm); border: 1px dashed var(--border-color); font-size: 0.82rem; color: #64748b;">
                <strong>Demo Credentials:</strong><br>
                Username: <code>admin</code><br>
                Password: <code>Password@123</code>
            </div>

            <div style="margin-top: 1.25rem; text-align: center; font-size: 0.85rem;">
                <a href="../registration/index.html" style="color: var(--primary-light); text-decoration: none;">
                    &larr; Return to Public Student Registration Form
                </a>
            </div>
        </div>
    </div>

</body>
</html>
