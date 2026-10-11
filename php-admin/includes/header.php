<?php
/**
 * Admin Panel Header & Layout Shell
 */
require_once __DIR__ . '/auth.php';
require_once __DIR__ . '/../config/database.php';

requireAdminLogin();

$currentAdmin = getCurrentAdmin();
$activePage = $activePage ?? 'dashboard';
$pageTitle = $pageTitle ?? 'Admin Dashboard';
$flashes = getFlashes();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= e($pageTitle) ?> - Student Admission Portal Admin</title>
    <link rel="stylesheet" href="assets/css/admin.css">
</head>
<body>

    <!-- Sidebar Navigation -->
    <aside class="admin-sidebar" aria-label="Admin Navigation">
        <div class="sidebar-header">
            <div class="sidebar-logo">A</div>
            <div>
                <div class="sidebar-title">Portal Admin</div>
                <div class="sidebar-subtitle">Admission Office</div>
            </div>
        </div>

        <nav class="sidebar-nav">
            <a href="dashboard.php" class="nav-item-link <?= ($activePage === 'dashboard') ? 'active' : '' ?>">
                <span class="nav-icon">&#128202;</span>
                <span class="nav-text">Dashboard</span>
            </a>
            <a href="dashboard.php#students-table" class="nav-item-link <?= ($activePage === 'students') ? 'active' : '' ?>">
                <span class="nav-icon">&#128101;</span>
                <span class="nav-text">Student Records</span>
            </a>
            <a href="add_student.php" class="nav-item-link <?= ($activePage === 'add_student') ? 'active' : '' ?>">
                <span class="nav-icon">&#10133;</span>
                <span class="nav-text">Add Student</span>
            </a>
            <a href="../registration/index.html" class="nav-item-link" target="_blank">
                <span class="nav-icon">&#128221;</span>
                <span class="nav-text">Public Registration</span>
            </a>
            <a href="http://localhost:8080/student-portal/students" class="nav-item-link" target="_blank" rel="noopener">
                <span class="nav-icon">&#9749;</span>
                <span class="nav-text">Java Portal (Tomcat)</span>
            </a>
        </nav>

        <div class="sidebar-footer">
            <div class="user-badge">
                <div class="user-avatar-circle">
                    <?= strtoupper(substr($currentAdmin['username'], 0, 1)) ?>
                </div>
                <div class="user-name">
                    <strong style="color: #ffffff;"><?= e($currentAdmin['username']) ?></strong>
                </div>
            </div>
            <a href="logout.php" class="btn-logout" title="Log out">Sign Out</a>
        </div>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="admin-main-wrap">
        
        <!-- Topbar -->
        <header class="admin-topbar">
            <h1 class="page-heading"><?= e($pageTitle) ?></h1>
            <div class="topbar-actions">
                <span style="font-size: 0.85rem; color: #64748b;">
                    Signed in as <strong><?= e($currentAdmin['full_name']) ?></strong>
                </span>
                <a href="add_student.php" class="btn-teal btn-sm" style="padding: 0.5rem 0.9rem;">+ Enroll Student</a>
            </div>
        </header>

        <!-- Main Body -->
        <main class="admin-content-area">

            <!-- Flash Notifications -->
            <?php if (!empty($flashes['success'])): ?>
                <div class="alert alert-success" role="alert">
                    <span>&#10003; <?= e($flashes['success']) ?></span>
                </div>
            <?php endif; ?>

            <?php if (!empty($flashes['error'])): ?>
                <div class="alert alert-error" role="alert">
                    <span>&#9888; <?= e($flashes['error']) ?></span>
                </div>
            <?php endif; ?>

            <?php if (!empty($flashes['warning'])): ?>
                <div class="alert alert-warning" role="alert">
                    <span>&#9888; <?= e($flashes['warning']) ?></span>
                </div>
            <?php endif; ?>
