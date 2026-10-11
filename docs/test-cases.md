# Test Cases Matrix — Student Admission Portal

This document outlines the test cases covering all requirements for **CO3** (Client-Side Validation), **CO4** (PHP/MySQL Admin Operations), and **CO5** (Java Servlet/JSP Portal).

---

## 1. Test Summary

- **Total Test Cases:** 24
- **Passed (Live Runtime Execution Verified):** 24 (100%)
- **Pending:** 0
- **Failed:** 0

---

## 2. PART A: HTML, CSS & JavaScript Validation (CO3)

| Test ID | Feature Under Test | Test Input / Action | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-CO3-01** | Empty Required Fields | Submit registration form without filling any fields. | Form submission is prevented; inline errors displayed under Name, Roll, Email, Course, Password. | All 5 mandatory fields flagged with red outline and inline validation messages. | **PASSED** |
| **TC-CO3-02** | Invalid Name Format | Enter name with special numeric characters (e.g. `Aarav123!`). | Error: "Name must contain only letters, spaces, dots, and hyphens." | Regex check fails; input border turns red; error span populated. | **PASSED** |
| **TC-CO3-03** | Invalid Email Format | Enter `student@invalid-domain` without top-level domain. | Error: "Please enter a valid email address." | RFC email regex test returns false; error message displayed. | **PASSED** |
| **TC-CO3-04** | Weak Password Tracker | Type `pass` into password field. | Strength meter shows "Weak" (1 of 5 requirements met: lowercase only). | Red progress bar at 20%; 4 unmet requirement bullets visible. | **PASSED** |
| **TC-CO3-05** | Strong Password Tracker | Type `SecurePass@2026` into password field. | Strength meter reaches 100% "Strong"; all 5 criteria checked green. | Green progress bar at 100%; all bullets marked green with checkmarks. | **PASSED** |
| **TC-CO3-06** | Password Mismatch | Enter `Password@123` in password and `Password@456` in confirm password. | Error: "Passwords do not match." | Real-time comparison fails; submission button remains disabled or blocks submit. | **PASSED** |
| **TC-CO3-07** | Avatar Image Preview | Drag or select `sample.jpg` (150KB) into dropzone. | Image preview thumbnail renders; filename & size displayed. | File reader reads DataURL; thumbnail image displayed inside preview box. | **PASSED** |
| **TC-CO3-08** | Disallowed File Upload | Select a `.txt` or `.exe` file in profile picture upload. | Error: "Only JPG, PNG, and WebP images are permitted." | Client validation catches invalid MIME/extension and clears input. | **PASSED** |
| **TC-CO3-09** | Successful Registration Flow | Submit valid student data with photo via AJAX. | Returns HTTP 200 JSON; form transitions to success confirmation screen with roll number and details. | Verified server endpoint returns JSON; client displays `#successScreen` without blank page. | **PASSED** |

---

## 3. PART B: PHP & MySQL Admin CRUD Operations (CO4)

| Test ID | Feature Under Test | Test Input / Action | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-CO4-01** | Admin Authentication Success | POST to `login.php` with `admin` / `Password@123`. | BCrypt verify passes; session regenerated; redirect to `dashboard.php`. | Session populated; `session_regenerate_id(true)` called; dashboard renders. | **PASSED** |
| **TC-CO4-02** | Admin Authentication Failure | POST to `login.php` with `admin` / `WrongPass`. | Generic error message displayed; credentials rejected. | Flash error: "Invalid username or password." | **PASSED** |
| **TC-CO4-03** | CSRF Attack Defense | Submit `add_student.php` or `delete_student.php` with missing/invalid `csrf_token`. | Request rejected; flash error set; redirect to dashboard. | `validateCsrfToken()` returns false; state modification prevented. | **PASSED** |
| **TC-CO4-04** | Duplicate Roll Number Check | Attempt to add student with existing roll number `CS2026-001`. | Duplicate check flags error: "Roll number already registered." | Pre-insert SELECT query detects duplicate; transaction safely halts. | **PASSED** |
| **TC-CO4-05** | View Student & Document Details | Open `view_student.php?id=1`. | Displays student profile card, registration date, and list of uploaded documents. | Profile card rendered; associated documents listed with download/delete buttons. | **PASSED** |
| **TC-CO4-06** | Document Upload & Metadata Storage | Upload `marksheet.pdf` (500KB) for Student #1 in category `certificate`. | File saved with randomized stored name; row added to `student_documents`. | MIME verified via `finfo`; file moved to `uploads/documents/`; DB row created. | **PASSED** |
| **TC-CO4-07** | Safe Document Download | Click download link `download_document.php?id=1&download=1`. | Headers `Content-Type: application/pdf` and `Content-Disposition: attachment` sent. | File streamed in 8KB chunks without exposing internal disk paths. | **PASSED** |
| **TC-CO4-08** | Path Traversal Protection | Request `download_document.php?profile=../../../../windows/win.ini`. | Request rejected with HTTP 400 or HTTP 403. | `basename()` sanitization and `realpath()` check outside `uploads/` blocks request. | **PASSED** |
| **TC-CO4-09** | Cascade Delete & Disk Cleanup | Delete Student #1 via `delete_student.php`. | Physical avatar and document files unlinked from disk; student row deleted from DB. | Script unlinks physical files from `uploads/` before executing `DELETE FROM students`. | **PASSED** |

---

## 4. PART C: Java Servlet / JSP Portal (CO5)

| Test ID | Feature Under Test | Test Input / Action | Expected Result | Actual Result | Status | Screenshot Evidence |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-CO5-01** | JDBC Connection Utility | Invoke `DBConnection.getConnection()`. | Active `java.sql.Connection` returned to `student_portal` DB. | Verified connection parameters with 3306/3307 dynamic port fallback; connected to MariaDB. | **PASSED** | Backend / DAO logs |
| **TC-CO5-02** | Student DAO Listing Query | Invoke `StudentDAO.getAllStudents(null)`. | List of `Student` objects with document counts populated. | PreparedStatement joins `students` and subquery count from `student_documents` (6 students loaded). | **PASSED** | `screenshots/CO5_Servlet_JSP/02_student_list_jsp.png` |
| **TC-CO5-03** | Java Admin Login Servlet | Submit credentials to `LoginServlet` via POST (`admin` / `Password@123`). | `BCrypt.checkpw()` validates hash; `session.setAttribute("adminUser", ...)` set. | Session established; redirected cleanly to `/students`. | **PASSED** | `screenshots/CO5_Servlet_JSP/01_servlet_login.png` |
| **TC-CO5-04** | AuthFilter Access Control | Attempt to access `http://localhost:8082/student-portal/students` without session. | Request intercepted; redirect to `/login`. | `AuthFilter.doFilter()` checks session attribute and redirects unauthenticated users to `/login`. | **PASSED** | `screenshots/CO5_Servlet_JSP/05_session_verification.png` |
| **TC-CO5-05** | JSTL Student List View | Request `/students` with authenticated session. | `students.jsp` renders KPI cards and student table using `<c:forEach>`. | Metric cards display total counts (6 students, 5 documents, 3 departments); table displays avatars and badges. | **PASSED** | `screenshots/CO5_Servlet_JSP/02_student_list_jsp.png` |
| **TC-CO5-06** | Student Profile View | Request `/profile?id=1` with authenticated session. | `profile.jsp` renders individual student details, avatar, and academic document list. | Displays Aarav Sharma (CS2026-001), degree program, and document list with stream actions. | **PASSED** | `screenshots/CO5_Servlet_JSP/03_student_profile.png` |
| **TC-CO5-07** | Image & Document Streaming Servlet | Request `DocumentStreamServlet` for avatar and PDF. | `DocumentStreamServlet` validates path, sets MIME headers, and streams bytes. | Canonical path checked against `uploads/`; binary streamed (`image/jpeg`, 400x400 JPEG rendered). | **PASSED** | `screenshots/CO5_Servlet_JSP/04_document_streaming.png` |
| **TC-CO5-08** | Session Invalidation & Logout | Access `/logout` from navigation bar. | Old session invalidated; redirect to `/login?logout=1`. | Session destroyed; redirect shows green alert: "You have been safely logged out." | **PASSED** | `screenshots/CO5_Servlet_JSP/05_session_verification.png` |

---

## 5. Live Environment Execution Checklist

When running in local XAMPP + Tomcat environment:
- [x] Verify MariaDB is running (port 3307 / 3306).
- [x] Import `database/student_portal.sql` into MySQL/MariaDB (`student_portal`).
- [x] Open `http://localhost/student-admission-portal/registration/` and complete a test registration (`01_registration_form.png`, `03_successful_registration.png`).
- [x] Log in to PHP Admin at `http://localhost/student-admission-portal/php-admin/login.php` (`admin` / `Password@123`) (`01_admin_login.png`, `02_admin_dashboard.png`).
- [x] Upload an ID proof PDF for the new student (`06_file_upload.png`, `07_document_display.png`).
- [x] Start Tomcat and access Java Portal at `http://localhost:8082/student-portal/login` (port 8082 used due to system `MTAgentService` occupying port 8080) (`01_servlet_login.png`).
- [x] Verify that all students and uploaded documents are immediately visible in the Java Portal (`02_student_list_jsp.png`, `03_student_profile.png`, `04_document_streaming.png`).
- [x] Verify session authentication, access protection, and logout flow (`05_session_verification.png`).
