# Student Admission Portal

A secure, multi-tier web application for student admissions, registration, document management, and administrative records. Built with **HTML5/CSS3/JavaScript** (CO3), **PHP 8 & MySQL** (CO4), and **Jakarta Servlet/JSP on Apache Tomcat** (CO5).

---

## 📌 Architecture Overview

```
                      +---------------------------------------+
                      |       Shared MySQL / MariaDB         |
                      |          `student_portal`             |
                      +---------------------------------------+
                                  ▲               ▲
                                  │ (PDO)         │ (JDBC)
                   +--------------┴----+     +----┴-------------------+
                   |   PHP Backend     |     |   Java Servlet / JSP   |
                   |   (Apache / XAMPP)|     |   (Tomcat 8.5+ / 8080) |
                   +-------------------+     +------------------------+
                             ▲                           ▲
                             │                           │
                   +---------┴---------+                 │
                   | Student Register  |                 │
                   | (HTML5 / CSS / JS)|                 │
                   +-------------------+                 │
                             ▲                           ▲
                             └───────────┬───────────────┘
                                         │
                                  End Users / Admin
```

---

## 🚀 System Modules & Assignment Mapping

| Module | Outcome | Tech Stack | Target URL | Key Responsibilities |
| :--- | :---: | :--- | :--- | :--- |
| **Registration Portal** | **CO3** | HTML5, CSS3, JavaScript, PHP API | `http://localhost/student-admission-portal/registration/` | Responsive form, 5-rule password strength meter, client-side validation, drag-and-drop avatar upload. |
| **PHP Admin Panel** | **CO4** | PHP 8 (PDO), MySQL, CSS3 | `http://localhost/student-admission-portal/php-admin/` | Admin authentication, Student CRUD, document uploads (PDF/Images), secure download streaming, CSRF & XSS protection. |
| **Java Servlet/JSP Portal** | **CO5** | Java 8+, Servlets 3.1, JSP, JDBC | `http://localhost:8080/student-portal/` | JDBC PreparedStatement DAO, JSTL student registry, image streaming servlet, session authorization filter. |
| **Shared Database** | **All** | MySQL 8.0+ / MariaDB 10.4+ | Port `3306` (`student_portal`) | Normalized schema (`admin_users`, `students`, `student_documents`), foreign keys, bcrypt credentials. |

---

## 🔑 Default Credentials

- **Admin Username:** `admin`
- **Admin Password:** `Password@123`
- **Sample Student Password:** `Student@123`

---

## 🛠️ Prerequisites & Installation

1. **XAMPP** (with Apache, MySQL/MariaDB, and PHP 8.x)
2. **Java JDK 8 or higher** (Oracle JDK, OpenJDK, or Eclipse Temurin)
3. **Apache Tomcat 8.5+ / 9.0+** (included in XAMPP Tomcat or standalone)

---

## 📖 Step-by-Step Setup Guide

### 1. Database Setup (MySQL via phpMyAdmin or CLI)
1. Start **Apache** and **MySQL** in the XAMPP Control Panel.
2. Open **phpMyAdmin** at `http://localhost/phpmyadmin/`.
3. Create a new database named `student_portal` with collation `utf8mb4_unicode_ci`.
4. Click **Import**, select `database/student_portal.sql` from this repository, and click **Go**.

---

### 2. PHP Applications Deployment (XAMPP Apache)
1. Copy or link this project folder to your XAMPP web root:
   ```
   C:\xampp\htdocs\student-admission-portal\
   ```
2. Verify PHP database credentials in `php-admin/config/database.php` (default: host `127.0.0.1`, port `3306`, user `root`, password `""`).
3. Access the portals:
   - **Student Registration:** [http://localhost/student-admission-portal/registration/](http://localhost/student-admission-portal/registration/)
   - **PHP Admin Login:** [http://localhost/student-admission-portal/php-admin/login.php](http://localhost/student-admission-portal/php-admin/login.php)
   - **PHP Admin Dashboard:** [http://localhost/student-admission-portal/php-admin/dashboard.php](http://localhost/student-admission-portal/php-admin/dashboard.php)

---

### 3. Java Servlet/JSP Deployment (Apache Tomcat)

#### Option A: Quick WAR Deployment
1. Copy the pre-built `java-portal/target/student-portal.war` into Tomcat's `webapps` directory:
   ```
   C:\xampp\tomcat\webapps\student-portal.war
   ```
2. Start Tomcat via `C:\xampp\tomcat\catalina_start.bat` or XAMPP Control Panel.
3. Access the Java Portal at:
   - **Java Admin Login:** [http://localhost:8080/student-portal/login](http://localhost:8080/student-portal/login)
   - **Java Student Registry:** [http://localhost:8080/student-portal/students](http://localhost:8080/student-portal/students)

#### Option B: Building from Source (Maven / javac)
- **Using Maven:**
  ```bash
  cd java-portal
  mvn clean package
  ```
- **Using standalone javac (Windows PowerShell):**
  ```powershell
  $classpath = "C:\xampp\tomcat\lib\servlet-api.jar;C:\xampp\tomcat\lib\jsp-api.jar"
  $javaFiles = Get-ChildItem -Path "java-portal\src\main\java" -Filter "*.java" -Recurse | Select-Object -ExpandProperty FullName
  javac -encoding UTF-8 -cp $classpath -d java-portal\src\main\webapp\WEB-INF\classes $javaFiles
  cd java-portal\src\main\webapp
  jar -cvf ..\..\target\student-portal.war *
  ```

---

## 📂 Project Directory Structure

```
StudentAdmissionPortal/
├── README.md                           # Master project guide
├── .gitignore                          # Git exclusions
├── database/
│   └── student_portal.sql             # Complete schema, indexes, FKs, and seed data
├── registration/                       # [CO3] Client-side registration module
│   ├── index.html                     # Semantic registration form & success screen
│   ├── css/style.css                  # Responsive design and password meter CSS
│   ├── js/validation.js               # Client validation, regex, dropzone handling
│   └── register.php                   # Server endpoint with bcrypt & PDO insert
├── php-admin/                          # [CO4] PHP Admin CRUD module
│   ├── config/database.php            # Shared PDO connection factory
│   ├── includes/auth.php              # Auth checks, CSRF tokens, XSS escaping
│   ├── includes/header.php            # Admin top navigation bar
│   ├── includes/footer.php            # Admin footer
│   ├── assets/css/admin.css           # Admin dashboard stylesheet
│   ├── login.php                      # Admin login with session fixation defense
│   ├── logout.php                     # Session termination
│   ├── dashboard.php                  # KPI metrics, student table, course summary
│   ├── add_student.php                # Add student form with validation & upload
│   ├── edit_student.php               # Edit student details
│   ├── view_student.php               # Detailed student profile & document manager
│   ├── delete_student.php             # Cascade delete & disk cleanup
│   ├── upload_document.php            # Document upload & delete handler
│   ├── download_document.php          # Secure streaming endpoint (path traversal safe)
│   └── uploads/                       # Unguessable stored files storage
├── java-portal/                        # [CO5] Java Servlet / JSP module
│   ├── pom.xml                        # Maven dependencies & build descriptor
│   ├── target/student-portal.war      # Compiled and packaged deployment WAR
│   └── src/
│       └── main/
│           ├── java/com/studentportal/
│           │   ├── config/DBConnection.java       # Reusable JDBC connection factory
│           │   ├── dao/StudentDAO.java            # Student & doc query operations
│           │   ├── dao/DocumentDAO.java           # Document metadata queries
│           │   ├── dao/AdminDAO.java              # Admin authentication via BCrypt
│           │   ├── model/Student.java             # Student entity POJO
│           │   ├── model/StudentDocument.java     # Document metadata POJO
│           │   ├── model/AdminUser.java           # Administrator POJO
│           │   ├── servlet/LoginServlet.java      # Auth controller
│           │   ├── servlet/StudentListServlet.java# Registry controller
│           │   ├── servlet/StudentProfileServlet.java # Profile controller
│           │   ├── servlet/DocumentStreamServlet.java # Secure image & doc streaming
│           │   ├── servlet/LogoutServlet.java     # Session destruction
│           │   ├── filter/AuthFilter.java         # Access control filter
│           │   └── util/BCrypt.java               # Pure Java BCrypt verifier
│           └── webapp/
│               ├── css/portal.css                 # Java portal stylesheet
│               └── WEB-INF/
│                   ├── web.xml                    # Servlet 3.1 web deployment descriptor
│                   └── jsp/
│                       ├── login.jsp              # Administrator login view
│                       ├── students.jsp           # Students listing & metric cards
│                       └── profile.jsp            # Student details & document links
└── docs/
    ├── project-audit.md               # Quality, security, and requirement audit
    ├── project-report.md              # Complete academic report with viva guide
    ├── test-cases.md                  # Comprehensive test matrix (CO3, CO4, CO5)
    └── screenshots/
        └── README.md                  # Screenshot capture guide & captions
```

---

## 🔒 Security Implementations

1. **Password Security:** Passwords hashed with standard **BCrypt** ($2y$) in both PHP and Java. No plaintext passwords stored.
2. **SQL Injection Defense:** 100% parameter binding through **PDO Prepared Statements** in PHP and **PreparedStatement** in Java.
3. **Cross-Site Scripting (XSS):** All dynamic strings escaped with `htmlspecialchars(..., ENT_QUOTES, 'UTF-8')` in PHP and `c:out` / JSTL in JSP.
4. **Cross-Site Request Forgery (CSRF):** Form submissions protected by cryptographically randomized session tokens verified using `hash_equals()`.
5. **Session Fixation Prevention:** Session IDs regenerated via `session_regenerate_id(true)` upon successful login in PHP, and old session invalidated in Java.
6. **Path Traversal Defense:** File streaming strictly enforces `realpath()` / `getCanonicalPath()` verification against the `uploads/` directory boundary, blocking `../` traversal attacks.
7. **Active Script Upload Block:** Uploaded filenames randomized (`bin2hex(random_bytes(10))`), MIME types validated using `fileinfo` / `Files.probeContentType`, and streaming of `.php`, `.jsp`, `.exe`, `.sh` files explicitly rejected.

---

## 👥 Authors & Academic Context

- **Author:** BE Computer Science Student
- **Course:** Web Technology Laboratory Assignment
- **Outcomes Covered:** CO3 (HTML/CSS/JS Form), CO4 (PHP/MySQL Admin CRUD), CO5 (Java Servlet/JSP/JDBC Portal)
