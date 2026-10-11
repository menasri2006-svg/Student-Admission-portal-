<?php
/**
 * Admin Logout Endpoint
 * Safely invalidates session data and removes session cookies
 */
require_once __DIR__ . '/includes/auth.php';

// Unset all session variables
$_SESSION = [];

// Delete session cookie if present
if (ini_get('session.use_cookies')) {
    $params = session_get_cookie_params();
    setcookie(
        session_name(),
        '',
        time() - 42000,
        $params['path'],
        $params['domain'],
        $params['secure'],
        $params['httponly']
    );
}

// Destroy session
session_destroy();

// Redirect back to login
session_start();
$_SESSION['flash_success'] = 'You have been successfully logged out.';
header('Location: login.php');
exit;
