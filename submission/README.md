# Student Admission Portal — Submission Package

**Course:** Web Technology Laboratory Assignment / Practical Record  
**Assignment Coverage:**  
- **CO3:** HTML5, CSS3, JavaScript Client-Side Registration & Form Validation (8 Marks)  
- **CO4:** PHP 8, MySQL Admin Dashboard, CRUD Operations & Document Management (16 Marks)  
- **CO5:** Java Servlet 3.1, JSP, JDBC, JSTL, and Session Security on Apache Tomcat (16 Marks)  
**Total Assignment Marks:** 40 / 40 Marks  

---

## 1. System Requirements & Prerequisites

- **Web Server:** Apache HTTP Server 2.4+ (included with XAMPP)
- **Database Engine:** MariaDB 10.4+ / MySQL 8.0+ running on port `3306` (or `3307`)
- **PHP Environment:** PHP 8.2+ with PDO, PDO_MySQL, and fileinfo extensions
- **Java Runtime:** JDK 8+ or JDK 24 (`javac` and `jar`)
- **Servlet Container:** Apache Tomcat 8.5+ / 9.0+
- **Browser:** Any modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge)

---

## 2. Directory Layout in Submission Package

```
submission/
├── Student_Admission_Portal_Final_Report.docx   # Master formatted Word assignment report
├── Student_Admission_Portal_Final_Report.md     # Full academic markdown report
├── database_schema.sql                          # MySQL schema, table DDL, and sample seeds
├── README.md                                    # This project setup and run guide
└── screenshots/                                 # 16 genuine application screenshots
    ├── CO3_Registration/                        # 4 form validation and submission screenshots
    ├── CO4_PHP_CRUD/                            # 7 PHP admin panel and CRUD screenshots
    └── CO5_Servlet_JSP/                         # 5 Java servlet, JSP, and stream screenshots
```

---

## 3. Quick Run Instructions

### Step 1: Database Setup
1. Start MySQL/MariaDB in XAMPP or service manager.
2. Create database `student_portal` with `utf8mb4_unicode_ci`.
3. Import `database_schema.sql` via phpMyAdmin (`http://localhost/phpmyadmin`) or CLI:
   ```bash
   mysql -u root -p student_portal < database_schema.sql
   ```

### Step 2: Running PHP Modules (CO3 & CO4)
1. Deploy project directory to XAMPP web root: `C:\xampp\htdocs\student-admission-portal\`.
2. Start Apache via XAMPP Control Panel.
3. Access endpoints:
   - **Student Registration (CO3):** `http://localhost/student-admission-portal/registration/`
   - **PHP Admin Login (CO4):** `http://localhost/student-admission-portal/php-admin/login.php`
   - **PHP Admin Dashboard (CO4):** `http://localhost/student-admission-portal/php-admin/dashboard.php`
4. Default credentials:
   - **Admin Username:** `admin`
   - **Admin Password:** `Password@123`

### Step 3: Running Java Portal (CO5)
1. Deploy `java-portal/target/student-portal.war` to Tomcat's `webapps` folder (`C:\xampp\tomcat\webapps\student-portal.war`).
2. Start Apache Tomcat:
   - Standalone: `C:\xampp\tomcat\bin\catalina.bat run`
   - Port note: Configured on port `8082` if port `8080` is reserved by system utilities.
3. Access Java Portal endpoints:
   - **Java Admin Login (CO5):** `http://localhost:8082/student-portal/login`
   - **Java Student Registry (CO5):** `http://localhost:8082/student-portal/students`
   - **Java Student Profile (CO5):** `http://localhost:8082/student-portal/profile?id=1`
   - **Document Stream Servlet (CO5):** `http://localhost:8082/student-portal/document?profile=doc_aarav_profile_sample.jpg`

---

## 4. Academic Documentation Files

- **Microsoft Word Report:** Open `Student_Admission_Portal_Final_Report.docx` for the official faculty submission document with embedded figures, tables, code listings, and formatted headings.
- **Markdown Report:** Reference `Student_Admission_Portal_Final_Report.md` for text review.
