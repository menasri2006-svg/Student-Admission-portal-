-- ====================================================================
-- STUDENT ADMISSION PORTAL - SHARED DATABASE SCHEMA
-- Compatible with MySQL 8.0+ and MariaDB 10.4+ (XAMPP default)
-- Shared across: PHP Registration, PHP Admin Panel, and Java Servlet/JSP
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `student_portal` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `student_portal`;

-- --------------------------------------------------------------------
-- 1. Table: admin_users
-- Stores administrator credentials for PHP Admin & Java Admin portals
-- Passwords stored exclusively as secure bcrypt hashes
-- --------------------------------------------------------------------
DROP TABLE IF EXISTS `admin_users`;
CREATE TABLE `admin_users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `role` VARCHAR(20) NOT NULL DEFAULT 'admin',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_admin_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------------
-- 2. Table: students
-- Main student registry storing academic profile and credentials
-- --------------------------------------------------------------------
DROP TABLE IF EXISTS `student_documents`;
DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `roll_number` VARCHAR(30) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `course` VARCHAR(80) NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `profile_image` VARCHAR(255) DEFAULT NULL,
    `status` ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Approved',
    `registration_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_roll_number` (`roll_number`),
    INDEX `idx_student_email` (`email`),
    INDEX `idx_student_course` (`course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------------
-- 3. Table: student_documents
-- Metadata for student documents: profile photos, ID proofs, certificates
-- Physical files stored on disk using unguessable randomized filenames
-- --------------------------------------------------------------------
CREATE TABLE `student_documents` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `original_filename` VARCHAR(255) NOT NULL,
    `stored_filename` VARCHAR(255) NOT NULL UNIQUE,
    `file_path` VARCHAR(255) NOT NULL,
    `mime_type` VARCHAR(100) NOT NULL,
    `file_size` BIGINT NOT NULL,
    `document_category` ENUM('profile_image', 'id_proof', 'certificate', 'other') NOT NULL DEFAULT 'other',
    `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_docs_student` FOREIGN KEY (`student_id`) 
        REFERENCES `students` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `idx_docs_student_id` (`student_id`),
    INDEX `idx_docs_category` (`document_category`),
    INDEX `idx_stored_filename` (`stored_filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------------
-- 4. Initial Seed Data
-- Default Admin Account:
-- Username: admin
-- Password: Password@123
-- (Bcrypt hash generated via password_hash('Password@123', PASSWORD_BCRYPT))
-- --------------------------------------------------------------------
INSERT INTO `admin_users` (`username`, `password_hash`, `full_name`, `email`, `role`) VALUES
('admin', '$2y$10$pqlfs4UhUDhaSV2HirlmiOfB2d3UowuIeayCU77dfJzV48AG4U8qG', 'Admission Administrator', 'admin@admission.edu', 'admin')
ON DUPLICATE KEY UPDATE `username` = `username`;

-- --------------------------------------------------------------------
-- Sample Students
-- Default student password: Student@123
-- Bcrypt hash generated via password_hash('Student@123', PASSWORD_BCRYPT)
-- --------------------------------------------------------------------
INSERT INTO `students` (`id`, `roll_number`, `name`, `email`, `course`, `password_hash`, `profile_image`, `status`) VALUES
(1, 'CS2026-001', 'Aarav Sharma', 'aarav.sharma@example.com', 'B.Tech Computer Science', '$2y$10$YAkbEInvYwX4WDTGTH3yweMXGsW5ccVBbuQH6G3GZcfc/Z39JAb5W', 'sample_aarav.jpg', 'Approved'),
(2, 'CS2026-002', 'Diya Patel', 'diya.patel@example.com', 'B.Tech Information Technology', '$2y$10$YAkbEInvYwX4WDTGTH3yweMXGsW5ccVBbuQH6G3GZcfc/Z39JAb5W', 'sample_diya.jpg', 'Approved'),
(3, 'CS2026-003', 'Rohan Verma', 'rohan.verma@example.com', 'B.Tech Computer Science', '$2y$10$YAkbEInvYwX4WDTGTH3yweMXGsW5ccVBbuQH6G3GZcfc/Z39JAb5W', NULL, 'Pending'),
(4, 'EC2026-015', 'Ananya Iyer', 'ananya.iyer@example.com', 'B.Tech Electronics & Comm', '$2y$10$YAkbEInvYwX4WDTGTH3yweMXGsW5ccVBbuQH6G3GZcfc/Z39JAb5W', NULL, 'Approved')
ON DUPLICATE KEY UPDATE `roll_number` = `roll_number`;

-- Sample Document Metadata for Students
INSERT INTO `student_documents` (`id`, `student_id`, `original_filename`, `stored_filename`, `file_path`, `mime_type`, `file_size`, `document_category`) VALUES
(1, 1, 'aarav_photo.jpg', 'doc_aarav_profile_sample.jpg', 'uploads/profile_images/doc_aarav_profile_sample.jpg', 'image/jpeg', 145200, 'profile_image'),
(2, 1, 'aarav_aadhaar.pdf', 'doc_aarav_id_proof_sample.pdf', 'uploads/documents/doc_aarav_id_proof_sample.pdf', 'application/pdf', 312000, 'id_proof'),
(3, 2, 'diya_photo.jpg', 'doc_diya_profile_sample.jpg', 'uploads/profile_images/doc_diya_profile_sample.jpg', 'image/jpeg', 178400, 'profile_image'),
(4, 2, 'diya_marksheet.pdf', 'doc_diya_cert_sample.pdf', 'uploads/documents/doc_diya_cert_sample.pdf', 'application/pdf', 542100, 'certificate')
ON DUPLICATE KEY UPDATE `id` = `id`;
