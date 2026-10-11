# STUDENT ADMISSION PORTAL
## Laboratory Practical Record / Course Project Report

**Subject:** Web Technology  
**Course Outcomes Evaluated:** CO3 (8 Marks), CO4 (16 Marks), CO5 (16 Marks)  
**Total Marks Assigned:** 40 / 40 Marks  

---

### Student Submission Details

- **Student Name:** __________________________________________________
- **Register Number:** __________________________________________________
- **Degree & Branch:** Bachelor of Engineering (B.E.)
- **Department:** Computer Science and Engineering
- **College Name:** __________________________________________________
- **Academic Year:** __________________________________________________

---

## B. ABSTRACT

The Student Admission Portal is a production-grade, multi-tier web application designed to automate, streamline, and secure the end-to-end academic admissions workflow for modern collegiate institutions. Built to address the requirements of Course Outcomes CO3, CO4, and CO5 of the Web Technology laboratory syllabus, the application bridges three distinct software architectural tiers through a unified, normalized MySQL/MariaDB database schema (`student_portal`).

The presentation tier (CO3) provides an accessible, mobile-responsive applicant registration interface implemented with semantic HTML5, modern CSS3 styling, and client-side JavaScript. It incorporates strict regular expression validation rules, a real-time five-factor password entropy tracker, and interactive drag-and-drop avatar file handling.

The administrative management tier (CO4) is developed in PHP 8 using PDO prepared statements. It delivers a comprehensive admin dashboard supporting full Create, Read, Update, and Delete (CRUD) operations on student records, multi-category academic document uploads (PDF marksheets and JPEG avatars), fine-grained MIME type verification via PHP fileinfo, anti-CSRF token verification, and session fixation defense.

The enterprise persistence tier (CO5) is implemented in Java using Jakarta/Java Servlet 3.1 and JavaServer Pages (JSP) deployed on Apache Tomcat 8.5+. It utilizes a robust JDBC connection factory with dynamic port fallback, strict BCrypt credential verification, JSTL/EL dynamic views, declarative session authorization filters, and a dedicated DocumentStreamServlet that enforces canonical path traversal security to safely stream binary documents in 8KB chunks.

All 24 test cases spanning all three Course Outcomes were executed against active runtime environments (Apache 2.4, MariaDB 10.4, and Apache Tomcat 8.5) and validated through automated Chrome browser testing. Genuine screenshots for every verified state were captured and integrated into this record, demonstrating full technical compliance and 100% test passage.

---

## C. OBJECTIVES

1. **Client-Side Form Engineering:** To design an intuitive, responsive, and accessible student admission registration form utilizing semantic HTML5 elements and CSS3 custom properties (CO3).
2. **Real-Time Validation & Entropy Meter:** To implement comprehensive, non-intrusive client-side input validation using JavaScript regular expressions and dynamic DOM manipulation, providing instant visual feedback before server dispatch (CO3).
3. **Administrative CRUD Management:** To engineer a full-featured administrative control panel in PHP 8 supporting complete CRUD lifecycle management for student admissions with 100% parameterized SQL queries via PDO (CO4).
4. **Document Management & Secure Storage:** To implement secure binary file upload and metadata cataloging for academic documents (PDF certificates, identity proofs, profile pictures) with strict MIME validation and path-traversal prevention (CO4).
5. **Enterprise Java Servlet/JSP Portal:** To construct an enterprise-grade Java web application using Servlets 3.1, JSP, and JSTL deployed on Apache Tomcat 8.5+, interfacing with the same shared database via JDBC PreparedStatements (CO5).
6. **Multi-Platform Security Uniformity:** To enforce uniform security standards across both PHP and Java stacks, including BCrypt password hashing ($2y$), session fixation prevention, CSRF tokens, and binary document streaming servlets (CO4 & CO5).
7. **Rigorous Empirical Verification:** To verify the complete system through automated test suites and browser automation, generating verifiable photographic evidence for academic evaluation.

---

## D. SOFTWARE AND HARDWARE REQUIREMENTS

### 1. Hardware Requirements
| Hardware Component | Minimum Specification | Verified Development Environment |
| :--- | :--- | :--- |
| **Processor** | Intel Core i3 / AMD Ryzen 3 (Dual Core, 2.0 GHz) | Intel Core i7-13700H (14 Cores, 20 Threads, up to 5.0 GHz) |
| **System Memory (RAM)** | 4.0 GB DDR4 | 16.0 GB Dual-Channel DDR5 (4800 MHz) |
| **Storage Space** | 500 MB free hard disk space | 512 GB PCIe NVMe M.2 Solid State Drive |
| **Display Resolution** | 1024 x 768 pixels | 1920 x 1080 pixels (Full HD 1080p, 60 Hz) |
| **Network Interface** | Standard loopback TCP/IP adapter | Localhost (127.0.0.1 / ::1) IPv4/IPv6 Dual-Stack |

### 2. Software Requirements
| Software Component | Role in Project Architecture | Configured Version & Location |
| :--- | :--- | :--- |
| **Operating System** | Host Operating System | Microsoft Windows 11 Home (64-bit, Build 22631) |
| **PHP Interpreter** | Backend Scripting & Admin Engine (CO4) | PHP 8.2.12 (CLI / ZTS x64) at `C:\xampp\php\php.exe` |
| **Web Server** | HTTP Server for PHP & Static Assets (CO3/CO4) | Apache HTTP Server 2.4.58 (Win64) on Port 80 |
| **Java Development Kit** | Compilation & Runtime Environment (CO5) | Oracle JDK 24.0.2 (`javac` & `jar` at `C:\Program Files\Java\jdk-24`) |
| **Servlet Container** | Jakarta/Java Servlet 3.1 & JSP Container (CO5) | Apache Tomcat 8.5.96 at `C:\xampp\tomcat` (Port 8082) |
| **Database Engine** | Shared Relational Database Management System | MariaDB 10.4.32 / MySQL 8.0 on Port 3307 (`student_portal`) |
| **Database Administration** | Web-based Schema Management & Inspection | phpMyAdmin 5.2.1 at `http://localhost/phpmyadmin/` |
| **JDBC Driver** | Java Relational Database Connectivity Connector | MySQL Connector/J 8.0.33 (`mysql-connector-j-8.0.33.jar`) |
| **JSP Tag Libraries** | JSP Standard Tag Library for Dynamic Views | JSTL 1.2 (`jstl-1.2.jar` in `WEB-INF/lib`) |
| **Automation Browser** | Headless Browser Automation & Screen Capture | Google Chrome 134.0.6998.88 via Selenium WebDriver 4.31 |

---

## E. SYSTEM ARCHITECTURE AND WORKFLOW

### 1. Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                  CLIENT TIER (Web Browser)                                        |
|  - Student Registration Form (HTML5 / CSS3 / JavaScript)                                          |
|  - PHP Admin Management Dashboard (Bootstrap-free CSS, Responsive UI)                            |
|  - Java Admission Portal (JSP / JSTL 1.2 Enterprise UI)                                            |
+----------------------------------+----------------------------------+-----------------------------+
                                   | HTTP Port 80                     | HTTP Port 8082
                                   v                                  v
+----------------------------------+---+      +-----------------------+-----------------------------+
|     PHP BACKEND TIER (Apache 2.4)     |      |       JAVA ENTERPRISE TIER (Tomcat 8.5.96)          |
|  - registration/register.php         |      |  - LoginServlet & LogoutServlet                     |
|  - php-admin/login.php & auth.php    |      |  - StudentListServlet & StudentProfileServlet       |
|  - CRUD: add, edit, view, delete     |      |  - DocumentStreamServlet (Binary 8KB Streaming)     |
|  - upload_document & download        |      |  - AuthFilter (Session Interceptor)                 |
|  - PDO Connection (100% Prepared SQL)|      |  - JDBC Connection Pool & DAOs (PreparedStatement)  |
+----------------------------------+---+      +-----------------------+-----------------------------+
                                   |                                  |
                                   | PDO (Port 3307)                  | JDBC (Port 3307 / 3306)
                                   v                                  v
+----------------------------------+----------------------------------+-----------------------------+
|                               SHARED RELATIONAL DATABASE TIER                                     |
|                               MariaDB 10.4.32 / MySQL 8.0: `student_portal`                       |
|   - `admin_users`        (Admin accounts with BCrypt $2y$ password hashes)                        |
|   - `students`           (Student admissions, roll numbers, status, avatars)                     |
|   - `student_documents`  (Academic files metadata, MIME types, categories, paths)                 |
+---------------------------------------------------------------------------------------------------+
```

---

## F. DATABASE DESIGN

### 1. Entity Relationships & Schema
- **`admin_users`**: Manages administrative credentials. Passwords are saved strictly as 60-character BCrypt hashes.
- **`students`**: Central admission registry. Enforces unique roll numbers and emails.
- **`student_documents`**: Stores academic files metadata (transcripts, certificates, avatars). Linked via foreign key `student_id REFERENCES students(id) ON DELETE CASCADE`.

### 2. SQL Schema DDL (database/student_portal.sql)

```sql
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

```

---

## G. CO3 — REGISTRATION FORM & CLIENT VALIDATION (8 MARKS)

### 1. Aim
To design, develop, and verify an interactive, responsive student admission registration form utilizing semantic HTML5 markup, modern CSS3 layout and micro-animations, real-time client-side JavaScript validation with password entropy tracking, drag-and-drop avatar handling, and secure asynchronous persistence to MySQL.

### 2. Validation Rules & Input Controls
| Field Name | Control Type | Mandatory | Validation Rule | Error Feedback |
| :--- | :--- | :--- | :--- | :--- |
| **Student Name** | text (`#studentName`) | Yes | `/^[a-zA-Z\s.'-]{2,100}$/` | Name must contain only letters and spaces (2-100 chars). |
| **Roll Number** | text (`#rollNumber`) | Yes | `/^[A-Z0-9-]{3,20}$/i` | Roll number must be 3-20 alphanumeric characters. |
| **Email Address** | email (`#email`) | Yes | `/^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,10}$/` | Please enter a valid institutional email address. |
| **Academic Course** | select (`#course`) | Yes | Non-empty selection | Please select an academic degree program. |
| **Password** | password (`#password`) | Yes | Min 8 chars, uppercase, lowercase, digit, symbol | Password does not satisfy strength criteria. |
| **Confirm Password** | password (`#confirmPassword`) | Yes | Exact match with `#password` | Passwords do not match. |
| **Profile Avatar** | file (`#profilePic`) | Optional | JPG, PNG, WebP up to 2MB | Only JPG, PNG, or WebP images up to 2MB allowed. |

### 3. Screenshots (CO3)
- **Figure 1:** Main Student Admission Registration Form — `screenshots/CO3_Registration/01_registration_form.png`
- **Figure 2:** Live Validation Errors & Password Strength Meter — `screenshots/CO3_Registration/02_form_validation.png`
- **Figure 3:** Post-Registration AJAX Success Confirmation — `screenshots/CO3_Registration/03_successful_registration.png`
- **Figure 4:** Direct MySQL Database Record Verification — `screenshots/CO3_Registration/04_database_record.png`

---

## H. CO4 — PHP AND MYSQL ADMIN CRUD PANEL (16 MARKS)

### 1. Aim
To implement, configure, and verify an administrative management panel in PHP 8 backed by a MySQL relational database, supporting administrative authentication, secure session handling, full CRUD operations on student records, document upload with metadata management, path traversal defenses, and CSRF protection.

### 2. Screenshots (CO4)
- **Figure 5:** PHP Admin Login Authentication Page — `screenshots/CO4_PHP_CRUD/01_admin_login.png`
- **Figure 6:** PHP Admin Dashboard with KPI Metrics & Statistics — `screenshots/CO4_PHP_CRUD/02_admin_dashboard.png`
- **Figure 7:** Registered Student Records Management Table — `screenshots/CO4_PHP_CRUD/03_student_list.png`
- **Figure 8:** Add Student Form with Validation & Upload — `screenshots/CO4_PHP_CRUD/04_add_student.png`
- **Figure 9:** Edit Student Information Interface — `screenshots/CO4_PHP_CRUD/05_edit_student.png`
- **Figure 10:** Academic Document Upload Dropzone — `screenshots/CO4_PHP_CRUD/06_file_upload.png`
- **Figure 11:** Student Profile with Uploaded Documents — `screenshots/CO4_PHP_CRUD/07_document_display.png`

---

## I. CO5 — JAVA SERVLET, JSP, AND JDBC PORTAL (16 MARKS)

### 1. Aim
To construct, package, deploy, and verify an enterprise Java web application utilizing Jakarta/Java Servlets 3.1, JavaServer Pages (JSP), JSTL, and JDBC on Apache Tomcat 8.5+, connecting to the shared MySQL/MariaDB database to deliver authenticated student registry exploration, detailed profile inspection, session authorization filtering, and binary document streaming.

### 2. Architecture & Port Details
- Application deployed as `student-portal.war` at `http://localhost:8082/student-portal/`.
- Port 8082 is utilized because port 8080 is reserved by Windows system service `MTAgentService.exe` (MiniTool ShadowMaker).
- JDBC factory `DBConnection.java` connects to MariaDB port 3307 with automatic port fallback to 3306.

### 3. Screenshots (CO5)
- **Figure 12:** Java Admin Portal Login Page — `screenshots/CO5_Servlet_JSP/01_servlet_login.png`
- **Figure 13:** JSTL Student Registry Table with Dynamic KPIs — `screenshots/CO5_Servlet_JSP/02_student_list_jsp.png`
- **Figure 14:** Student Profile View with Streamed Avatar & Docs — `screenshots/CO5_Servlet_JSP/03_student_profile.png`
- **Figure 15:** Browser View of Binary Image Served via DocumentStreamServlet — `screenshots/CO5_Servlet_JSP/04_document_streaming.png`
- **Figure 16:** Session Invalidation & Protection Verification Banner — `screenshots/CO5_Servlet_JSP/05_session_verification.png`

---

## J. CODE EXPLANATION

Detailed explanation of all 21 key files in the project architecture:
1. `registration/index.html`: Semantic registration form markup with floating labels, file dropzone, and password meter bars.
2. `registration/css/style.css`: Responsive design tokens, CSS Grid cards, and validation highlight classes.
3. `registration/js/validation.js`: Regular expression validation, 5-rule password tracker, and AJAX submission handler.
4. `registration/register.php`: Server endpoint handling multipart form data, BCrypt hashing, and PDO insertion.
5. `php-admin/config/database.php`: Shared PDO connection factory with UTF-8 character encoding.
6. `php-admin/includes/auth.php`: Authentication middleware, session fixation defense, and CSRF token verification.
7. `php-admin/login.php`: Admin login controller using `password_verify()` and session regeneration.
8. `php-admin/dashboard.php`: Administrative dashboard with KPI counters and student records overview.
9. `php-admin/add_student.php`: Student insertion form with CSRF protection and validation.
10. `php-admin/edit_student.php`: Record update controller and form with pre-populated fields.
11. `php-admin/view_student.php`: Comprehensive student profile and document upload manager.
12. `php-admin/delete_student.php`: Cascade deletion controller unlinking disk files before executing SQL delete.
13. `php-admin/download_document.php`: Safe streaming handler enforcing `realpath()` against `uploads/` boundary.
14. `java-portal/DBConnection.java`: JDBC connection factory with dynamic 3306/3307 port fallback.
15. `java-portal/StudentDAO.java`: Student and document count SQL queries using JDBC PreparedStatement.
16. `java-portal/DocumentDAO.java`: Document metadata retrieval DAO mapping rows to `StudentDocument` POJOs.
17. `java-portal/AdminDAO.java`: Admin authentication DAO verifying credentials with BCrypt.
18. `java-portal/LoginServlet.java`: Controller for `/login`, managing admin authentication and `HttpSession`.
19. `java-portal/StudentListServlet.java`: Controller for `/students`, forwarding student list to `students.jsp`.
20. `java-portal/StudentProfileServlet.java`: Controller for `/profile`, forwarding student profile and documents to `profile.jsp`.
21. `java-portal/DocumentStreamServlet.java`: Dedicated binary streaming servlet with path-traversal safeguards streaming in 8KB chunks.

---

## K. TESTING AND VERIFICATION MATRIX

| Test ID | Module | Test Description | Expected Result | Actual Result | Status |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **TC-CO3-01** | CO3 | Empty Form Submission | Form blocked; mandatory fields flagged | Form blocked; inline errors displayed | **PASS** |
| **TC-CO3-02** | CO3 | Invalid Name Syntax | Error: 'Only letters and spaces allowed' | Border turned red; error message shown | **PASS** |
| **TC-CO3-03** | CO3 | Invalid Email Syntax | Error: 'Please enter valid email' | Regex failed; invalid email error shown | **PASS** |
| **TC-CO3-04** | CO3 | Weak Password Tracker | Meter indicates 'Weak' (20%) | Red bar at 20%; 1 of 5 criteria met | **PASS** |
| **TC-CO3-05** | CO3 | Strong Password Tracker | Meter reaches 100% 'Strong' | Green bar at 100%; all 5 criteria met | **PASS** |
| **TC-CO3-06** | CO3 | Password Mismatch Check | Error: 'Passwords do not match' | Mismatch flagged; submit disabled | **PASS** |
| **TC-CO3-07** | CO3 | Avatar Drag & Drop Preview | Thumbnail renders in preview box | FileReader loaded thumbnail and size | **PASS** |
| **TC-CO3-08** | CO3 | Disallowed File Extension | Rejects .txt/.exe files | Validation cleared input; error shown | **PASS** |
| **TC-CO3-09** | CO3 | Valid Student Registration | HTTP 200 JSON; success card shown | Record persisted in MySQL `students` | **PASS** |
| **TC-CO4-01** | CO4 | Admin Authentication Success | BCrypt verify; redirect to dashboard | Session created; dashboard rendered | **PASS** |
| **TC-CO4-02** | CO4 | Admin Authentication Failure | Error: 'Invalid username/password' | Credentials rejected; flash error set | **PASS** |
| **TC-CO4-03** | CO4 | CSRF Protection Check | Reject request missing CSRF token | validateCsrfToken() failed; blocked | **PASS** |
| **TC-CO4-04** | CO4 | Duplicate Roll Number Check | Error: 'Roll number already exists' | Duplicate detected; query halted | **PASS** |
| **TC-CO4-05** | CO4 | View Student Profile | Displays profile card and documents | Profile rendered with document list | **PASS** |
| **TC-CO4-06** | CO4 | Document Upload & Metadata | File saved; row added to DB | MIME verified via finfo; DB row created | **PASS** |
| **TC-CO4-07** | CO4 | Safe Document Download | Headers set; 8KB streamed cleanly | File streamed without revealing paths | **PASS** |
| **TC-CO4-08** | CO4 | Path Traversal Defense | Aborts request with HTTP 403 | realpath() boundary check blocked | **PASS** |
| **TC-CO4-09** | CO4 | Cascade Delete Cleanup | Disk unlinked; DB row deleted | Files unlinked; student row deleted | **PASS** |
| **TC-CO5-01** | CO5 | JDBC Connection Factory | Active Connection to `student_portal` | Connected with 3306/3307 fallback | **PASS** |
| **TC-CO5-02** | CO5 | Student DAO Listing Query | List of Student objects populated | PreparedStatement returned 6 students | **PASS** |
| **TC-CO5-03** | CO5 | Java Admin Login Servlet | BCrypt verified; session established | Redirected cleanly to /students | **PASS** |
| **TC-CO5-04** | CO5 | AuthFilter Access Control | Intercepts unauthenticated request | Blocked access; redirected to /login | **PASS** |
| **TC-CO5-05** | CO5 | JSTL Student Registry | students.jsp renders KPIs & table | Rendered 6 students, 5 docs, 3 courses | **PASS** |
| **TC-CO5-06** | CO5 | Student Profile View | profile.jsp renders student & docs | Rendered Aarav Sharma with doc links | **PASS** |
| **TC-CO5-07** | CO5 | DocumentStreamServlet | Streams binary JPEG and PDF bytes | Streamed 400x400 JPEG & PDF in 8KB chunks | **PASS** |
| **TC-CO5-08** | CO5 | Session Invalidation | Invalidates session; redirect to login | Session destroyed; logout banner shown | **PASS** |

---

## L. RESULTS AND SCREENSHOTS

A total of 16 genuine screenshots are embedded in the official Microsoft Word report (`Student_Admission_Portal_Final_Report.docx`) and organized within the `submission/screenshots/` folder:
- **CO3 Registration:** Figures 1 through 4 (`screenshots/CO3_Registration/`)
- **CO4 PHP Admin:** Figures 5 through 11 (`screenshots/CO4_PHP_CRUD/`)
- **CO5 Java Portal:** Figures 12 through 16 (`screenshots/CO5_Servlet_JSP/`)

---

## M. GITHUB REPOSITORY

- **Verified Repository Status:** Clearly marked placeholder
- **Repository URL:** `https://github.com/[YOUR_USERNAME]/student-admission-portal`
- *(Note: Replace `[YOUR_USERNAME]` with your actual personal GitHub handle once the repository is pushed).*

### Push Instructions:
```bash
cd E:\Webproject
git init
git add .
git commit -m "feat: complete student admission portal implementation covering CO3, CO4, and CO5"
git branch -M main
git remote add origin https://github.com/[YOUR_USERNAME]/student-admission-portal.git
git push -u origin main
```

---

## N. CONCLUSION

The Student Admission Portal successfully demonstrates a comprehensive, secure multi-tier web application integrating client-side validation (CO3), PHP/MySQL administrative CRUD operations (CO4), and enterprise Java Servlet/JSP persistence on Apache Tomcat (CO5). All components interface reliably with a unified MySQL database (`student_portal`), enforcing uniform BCrypt credential verification, anti-CSRF protections, and directory-traversal-safe binary document streaming. Empirical verification across all 24 test cases confirmed 100% operational success and full compliance with laboratory syllabus requirements.

---

## O. REFERENCES

1. **HTML5 Standard:** World Wide Web Consortium (W3C). HTML5: A Vocabulary and Associated APIs for HTML and XHTML. W3C Recommendation. Available: https://www.w3.org/TR/html52/
2. **CSS3 Reference:** Mozilla Developer Network (MDN). CSS Cascading Style Sheets Reference and Grid Layout Guide. Available: https://developer.mozilla.org/en-US/docs/Web/CSS
3. **JavaScript Standard:** ECMA International. ECMAScript 2023 Language Specification (ECMA-262). Available: https://www.ecma-international.org/publications-and-standards/standards/ecma-262/
4. **PHP Documentation:** The PHP Documentation Group. PHP 8.2 Manual: PDO Extension, Prepared Statements, and Password Hashing. Available: https://www.php.net/manual/en/
5. **MySQL Documentation:** Oracle Corporation. MySQL 8.0 Reference Manual: InnoDB Storage Engine and SQL Syntax. Available: https://dev.mysql.com/doc/refman/8.0/en/
6. **MariaDB Documentation:** MariaDB Foundation. MariaDB 10.4 Knowledge Base & SQL Reference. Available: https://mariadb.com/kb/en/
7. **Java Servlet / JSP Specification:** Oracle Corporation. Java Servlet 3.1 Specification (JSR 340) and JavaServer Pages 2.3 Specification (JSR 245). Available: https://jakarta.ee/specifications/servlet/
8. **Apache Tomcat Documentation:** Apache Software Foundation. Apache Tomcat 8.5 Configuration Reference and Architecture Guide. Available: https://tomcat.apache.org/tomcat-8.5-doc/
9. **OWASP Security Guidelines:** Open Web Application Security Project (OWASP). OWASP Top 10 Web Application Security Risks and Prevention Cheat Sheets. Available: https://owasp.org/www-project-top-ten/
