<?php
/**
 * Authentication, Session Security & Core Utilities
 */

// Configure secure session cookie attributes before starting
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', '1');
    ini_set('session.use_only_cookies', '1');
    ini_set('session.cookie_samesite', 'Lax');
    session_start();
}

// Upload base directory
define('UPLOAD_BASE_DIR', realpath(__DIR__ . '/../uploads') ?: (__DIR__ . '/../uploads'));

/**
 * HTML Output Escaping against Cross-Site Scripting (XSS)
 */
function e(?string $value): string {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

/**
 * Checks if current user is logged in as an administrator
 */
function isAdminLoggedIn(): bool {
    return !empty($_SESSION['admin_user_id']) && !empty($_SESSION['admin_username']);
}

/**
 * Enforces admin authentication; redirects to login page if unauthenticated
 */
function requireAdminLogin(): void {
    if (!isAdminLoggedIn()) {
        $_SESSION['flash_error'] = 'Please log in to access the administration panel.';
        header('Location: login.php');
        exit;
    }
}

/**
 * Returns current logged-in admin data
 */
function getCurrentAdmin(): ?array {
    if (!isAdminLoggedIn()) {
        return null;
    }
    return [
        'id'        => $_SESSION['admin_user_id'],
        'username'  => $_SESSION['admin_username'],
        'full_name' => $_SESSION['admin_full_name'] ?? 'Administrator',
        'email'     => $_SESSION['admin_email'] ?? '',
        'role'      => $_SESSION['admin_role'] ?? 'admin'
    ];
}

/**
 * Generates or retrieves existing CSRF token
 */
function getCsrfToken(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Validates submitted CSRF token
 */
function validateCsrfToken(?string $token): bool {
    if (empty($token) || empty($_SESSION['csrf_token'])) {
        return false;
    }
    return hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Renders hidden CSRF token input field
 */
function csrfInput(): void {
    echo '<input type="hidden" name="csrf_token" value="' . e(getCsrfToken()) . '">';
}

/**
 * Sets a flash message to be shown on subsequent request
 */
function setFlash(string $type, string $message): void {
    $_SESSION['flash_' . $type] = $message;
}

/**
 * Retrieves and clears flash messages
 */
function getFlashes(): array {
    $flashes = [];
    $types = ['success', 'error', 'warning', 'info'];
    foreach ($types as $type) {
        $key = 'flash_' . $type;
        if (!empty($_SESSION[$key])) {
            $flashes[$type] = $_SESSION[$key];
            unset($_SESSION[$key]);
        }
    }
    return $flashes;
}
