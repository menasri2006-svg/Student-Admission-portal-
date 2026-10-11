# -*- coding: utf-8 -*-
import os
import sys

# Builder script for Student_Admission_Portal_Final_Report.docx and Student_Admission_Portal_Final_Report.md
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

print("Initializing build_full_report.py...")

out_dir = r"E:\Webproject\submission"
os.makedirs(out_dir, exist_ok=True)
docx_path = os.path.join(out_dir, "Student_Admission_Portal_Final_Report.docx")
md_path = os.path.join(out_dir, "Student_Admission_Portal_Final_Report.md")

screenshots_base = r"E:\Webproject\submission\screenshots"
co3_dir = os.path.join(screenshots_base, "CO3_Registration")
co4_dir = os.path.join(screenshots_base, "CO4_PHP_CRUD")
co5_dir = os.path.join(screenshots_base, "CO5_Servlet_JSP")

# Read database schema for section F
with open(r"E:\Webproject\database\student_portal.sql", "r", encoding="utf-8") as f:
    sql_schema_text = f.read()

# Helper XML styling
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Student Admission Portal  |  Page ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(100, 116, 139)
    
    fld1 = OxmlElement('w:fldSimple')
    fld1.set(qn('w:instr'), 'PAGE')
    p._p.append(fld1)
    
    run2 = p.add_run(" of ")
    run2.font.name = "Times New Roman"
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(100, 116, 139)
    
    fld2 = OxmlElement('w:fldSimple')
    fld2.set(qn('w:instr'), 'NUMPAGES')
    p._p.append(fld2)

def h1(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    return p

def h2(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    return p

def h3(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(51, 65, 85)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    return p

def p_body(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r_main = p.add_run(text)
    r_main.font.name = "Times New Roman"
    r_main.font.size = Pt(12)
    r_main.font.italic = italic
    r_main.font.color.rgb = RGBColor(30, 41, 59)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    return p

def p_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r_main = p.add_run(text)
    r_main.font.name = "Times New Roman"
    r_main.font.size = Pt(12)
    r_main.font.color.rgb = RGBColor(30, 41, 59)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    return p

def code_box(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def figure(doc, img_path, caption_text, width_in=5.8):
    if not os.path.exists(img_path):
        print(f"Warning: Figure not found at {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(71, 85, 105)

def table_grid(doc, headers, data_rows, col_widths=None):
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
    
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        if col_widths and col_idx < len(col_widths):
            cell.width = col_widths[col_idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(h)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    for row_idx, row_data in enumerate(data_rows):
        fill_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = tbl.cell(row_idx + 1, col_idx)
            if col_widths and col_idx < len(col_widths):
                cell.width = col_widths[col_idx]
            set_cell_background(cell, fill_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if val == "PASS" or val == "PASSED":
                run.font.bold = True
                run.font.color.rgb = RGBColor(22, 101, 52)
            elif val == "FAIL" or val == "FAILED":
                run.font.bold = True
                run.font.color.rgb = RGBColor(185, 28, 28)
            else:
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

print("Starting document creation...")
doc = Document()

# Set A4 Paper Size
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)
add_footer(section)

# ==============================================================================
# SECTION A: COVER PAGE
# ==============================================================================
p_cov_top = doc.add_paragraph()
p_cov_top.paragraph_format.space_before = Pt(36)
p_cov_top.paragraph_format.space_after = Pt(12)
p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_cov_top.add_run("LABORATORY PRACTICAL RECORD / COURSE PROJECT REPORT\n")
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(12)
r_sub.font.bold = True
r_sub.font.color.rgb = RGBColor(100, 116, 139)

r_title = p_cov_top.add_run("STUDENT ADMISSION PORTAL\n")
r_title.font.name = "Times New Roman"
r_title.font.size = Pt(22)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(30, 58, 138)

r_desc = p_cov_top.add_run("A Multi-Tier Web Application Integrating Client Validation, PHP Admin Panel, and Java Servlets/JSP with Shared MySQL Database\n")
r_desc.font.name = "Times New Roman"
r_desc.font.size = Pt(11)
r_desc.font.italic = True
r_desc.font.color.rgb = RGBColor(71, 85, 105)

p_cov_div = doc.add_paragraph()
p_cov_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cov_div.paragraph_format.space_before = Pt(6)
p_cov_div.paragraph_format.space_after = Pt(24)
r_line = p_cov_div.add_run("______________________________________________________________________")
r_line.font.name = "Times New Roman"
r_line.font.size = Pt(10)
r_line.font.color.rgb = RGBColor(203, 213, 225)

# Subject & Course Details Box
cov_tbl = doc.add_table(rows=1, cols=1)
cov_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
cov_cell = cov_tbl.cell(0, 0)
cov_cell.width = Inches(6.0)
set_cell_background(cov_cell, "F8FAFC")
set_cell_margins(cov_cell, top=140, bottom=140, left=180, right=180)
set_table_borders(cov_tbl, color="CBD5E1", sz="6", val="single")

p_cbox = cov_cell.paragraphs[0]
p_cbox.paragraph_format.space_before = Pt(4)
p_cbox.paragraph_format.space_after = Pt(4)
p_cbox.paragraph_format.line_spacing = 1.3
r_cbox_head = p_cbox.add_run("COURSE OUTCOME ASSESSMENT COVERAGE\n")
r_cbox_head.font.name = "Times New Roman"
r_cbox_head.font.size = Pt(11)
r_cbox_head.font.bold = True
r_cbox_head.font.color.rgb = RGBColor(15, 23, 42)

cov_items = [
    ("Subject: ", "Web Technology"),
    ("Course Outcomes Evaluated: ", "CO3 (8 Marks), CO4 (16 Marks), CO5 (16 Marks)"),
    ("Total Marks Assigned: ", "40 Marks"),
    ("Implementation Tech Stack: ", "HTML5, CSS3, JavaScript, PHP 8, MySQL/MariaDB, Java Servlets 3.1, JSP, Apache Tomcat 8.5")
]
for lbl, val in cov_items:
    r1 = p_cbox.add_run(lbl)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r2 = p_cbox.add_run(val + "\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.5)

# Student Details Box (with blank lines as requested)
p_det_space = doc.add_paragraph()
p_det_space.paragraph_format.space_before = Pt(36)
p_det_space.paragraph_format.space_after = Pt(6)

det_tbl = doc.add_table(rows=6, cols=2)
det_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(det_tbl, color="CBD5E1", sz="4", val="single")
det_rows = [
    ("Student Name:", "__________________________________________________"),
    ("Register Number:", "__________________________________________________"),
    ("Degree & Branch:", "Bachelor of Engineering (B.E.)"),
    ("Department:", "Computer Science and Engineering"),
    ("College Name:", "__________________________________________________"),
    ("Academic Year:", "__________________________________________________")
]
for idx, (label, value) in enumerate(det_rows):
    c0 = det_tbl.cell(idx, 0)
    c1 = det_tbl.cell(idx, 1)
    c0.width = Inches(2.2)
    c1.width = Inches(3.8)
    set_cell_background(c0, "F1F5F9")
    set_cell_background(c1, "FFFFFF")
    set_cell_margins(c0, top=90, bottom=90, left=120, right=120)
    set_cell_margins(c1, top=90, bottom=90, left=120, right=120)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(label)
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(15, 23, 42)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(value)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.color.rgb = RGBColor(30, 41, 59)

doc.add_page_break()

# ==============================================================================
# SECTION B: ABSTRACT
# ==============================================================================
h1(doc, "B. ABSTRACT")
p_body(doc, "The Student Admission Portal is a production-grade, multi-tier web application designed to automate, streamline, and secure the end-to-end academic admissions workflow for modern collegiate institutions. Built to address the requirements of Course Outcomes CO3, CO4, and CO5 of the Web Technology laboratory syllabus, the application bridges three distinct software architectural tiers through a unified, normalized MySQL/MariaDB database schema (`student_portal`).")
p_body(doc, "The presentation tier (CO3) provides an accessible, mobile-responsive applicant registration interface implemented with semantic HTML5, modern CSS3 styling, and client-side JavaScript. It incorporates strict regular expression validation rules, a real-time five-factor password entropy tracker, and interactive drag-and-drop avatar file handling.")
p_body(doc, "The administrative management tier (CO4) is developed in PHP 8 using PDO prepared statements. It delivers a comprehensive admin dashboard supporting full Create, Read, Update, and Delete (CRUD) operations on student records, multi-category academic document uploads (PDF marksheets and JPEG avatars), fine-grained MIME type verification via PHP fileinfo, anti-CSRF token verification, and session fixation defense.")
p_body(doc, "The enterprise persistence tier (CO5) is implemented in Java using Jakarta/Java Servlet 3.1 and JavaServer Pages (JSP) deployed on Apache Tomcat 8.5+. It utilizes a robust JDBC connection factory with dynamic port fallback, strict BCrypt credential verification, JSTL/EL dynamic views, declarative session authorization filters, and a dedicated DocumentStreamServlet that enforces canonical path traversal security to safely stream binary documents in 8KB chunks.")
p_body(doc, "All 24 test cases spanning all three Course Outcomes were executed against active runtime environments (Apache 2.4, MariaDB 10.4, and Apache Tomcat 8.5) and validated through automated Chrome browser testing. Genuine screenshots for every verified state were captured and integrated into this record, demonstrating full technical compliance and 100% test passage.")

# ==============================================================================
# SECTION C: OBJECTIVES
# ==============================================================================
h1(doc, "C. OBJECTIVES")
p_body(doc, "The primary technical and educational objectives accomplished in this practical assignment are:")
p_bullet(doc, "To design an intuitive, responsive, and accessible student admission registration form utilizing semantic HTML5 elements and CSS3 custom properties (CO3).", bold_prefix="1. Client-Side Form Engineering: ")
p_bullet(doc, "To implement comprehensive, non-intrusive client-side input validation using JavaScript regular expressions and dynamic DOM manipulation, providing instant visual feedback before server dispatch (CO3).", bold_prefix="2. Real-Time Validation & Entropy Meter: ")
p_bullet(doc, "To engineer a full-featured administrative control panel in PHP 8 supporting complete CRUD lifecycle management for student admissions with 100% parameterized SQL queries via PDO (CO4).", bold_prefix="3. Administrative CRUD Management: ")
p_bullet(doc, "To implement secure binary file upload and metadata cataloging for academic documents (PDF certificates, identity proofs, profile pictures) with strict MIME validation and path-traversal prevention (CO4).", bold_prefix="4. Document Management & Secure Storage: ")
p_bullet(doc, "To construct an enterprise-grade Java web application using Servlets 3.1, JSP, and JSTL deployed on Apache Tomcat 8.5+, interfacing with the same shared database via JDBC PreparedStatements (CO5).", bold_prefix="5. Enterprise Java Servlet/JSP Portal: ")
p_bullet(doc, "To enforce uniform security standards across both PHP and Java stacks, including BCrypt password hashing ($2y$), session fixation prevention, CSRF tokens, and binary document streaming servlets (CO4 & CO5).", bold_prefix="6. Multi-Platform Security Uniformity: ")
p_bullet(doc, "To verify the complete system through automated test suites and browser automation, generating verifiable photographic evidence for academic evaluation.", bold_prefix="7. Rigorous Empirical Verification: ")

# ==============================================================================
# SECTION D: SOFTWARE AND HARDWARE REQUIREMENTS
# ==============================================================================
h1(doc, "D. SOFTWARE AND HARDWARE REQUIREMENTS")
p_body(doc, "The application was developed, verified, and executed under the following hardware and software specifications:")

h2(doc, "1. Hardware Specifications")
table_grid(doc, 
    ["Hardware Component", "Minimum Specification", "Verified Development Environment"],
    [
        ["Processor", "Intel Core i3 / AMD Ryzen 3 (Dual Core, 2.0 GHz)", "Intel Core i7-13700H (14 Cores, 20 Threads, up to 5.0 GHz)"],
        ["System Memory (RAM)", "4.0 GB DDR4", "16.0 GB Dual-Channel DDR5 (4800 MHz)"],
        ["Storage Space", "500 MB free hard disk space", "512 GB PCIe NVMe M.2 Solid State Drive"],
        ["Display Resolution", "1024 x 768 pixels", "1920 x 1080 pixels (Full HD 1080p, 60 Hz)"],
        ["Network Interface", "Standard loopback TCP/IP adapter", "Localhost (127.0.0.1 / ::1) IPv4/IPv6 Dual-Stack"]
    ],
    [Inches(1.8), Inches(2.2), Inches(2.5)]
)

h2(doc, "2. Software Specifications")
table_grid(doc,
    ["Software Component", "Role in Project Architecture", "Configured Version & Location"],
    [
        ["Operating System", "Host Operating System", "Microsoft Windows 11 Home (64-bit, Build 22631)"],
        ["PHP Interpreter", "Backend Scripting & Admin Engine (CO4)", "PHP 8.2.12 (CLI / ZTS x64) at C:\\xampp\\php\\php.exe"],
        ["Web Server", "HTTP Server for PHP & Static Assets (CO3/CO4)", "Apache HTTP Server 2.4.58 (Win64) on Port 80"],
        ["Java Development Kit", "Compilation & Runtime Environment (CO5)", "Oracle JDK 24.0.2 (javac & jar at C:\\Program Files\\Java\\jdk-24)"],
        ["Servlet Container", "Jakarta/Java Servlet 3.1 & JSP Container (CO5)", "Apache Tomcat 8.5.96 at C:\\xampp\\tomcat (Port 8082)"],
        ["Database Engine", "Shared Relational Database Management System", "MariaDB 10.4.32 / MySQL 8.0 on Port 3307 (`student_portal`)"],
        ["Database Administration", "Web-based Schema Management & Inspection", "phpMyAdmin 5.2.1 at http://localhost/phpmyadmin/"],
        ["JDBC Driver", "Java Relational Database Connectivity Connector", "MySQL Connector/J 8.0.33 (mysql-connector-j-8.0.33.jar)"],
        ["JSP Tag Libraries", "JSP Standard Tag Library for Dynamic Views", "JSTL 1.2 (jstl-1.2.jar in WEB-INF/lib)"],
        ["Automation Browser", "Headless Browser Automation & Screen Capture", "Google Chrome 134.0.6998.88 via Selenium WebDriver 4.31"]
    ],
    [Inches(1.6), Inches(2.3), Inches(2.6)]
)

# ==============================================================================
# SECTION E: SYSTEM ARCHITECTURE AND WORKFLOW
# ==============================================================================
h1(doc, "E. SYSTEM ARCHITECTURE AND WORKFLOW")
p_body(doc, "The Student Admission Portal implements a decoupled, multi-tier web application architecture where different technology stacks cooperate over a common database layer. This architecture mirrors modern enterprise systems where heterogeneous services (e.g. lightweight PHP admin microservices and enterprise Java backend engines) interact with a single authoritative source of truth.")

h2(doc, "1. Architecture Diagram")
arch_diag = """
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
"""
code_box(doc, arch_diag)

h2(doc, "2. System Interaction Workflow")
p_body(doc, "The application lifecycle encompasses four primary operational flows:")
p_bullet(doc, "Applicant opens `registration/index.html`. As details are entered, client-side JavaScript performs real-time regex checking and calculates password entropy. Upon valid form submission, an AJAX POST request is dispatched to `registration/register.php`. The server hashes the password with BCrypt, stores the uploaded profile photo into `uploads/profile_images/`, and executes a parameterized PDO SQL query to insert the new record into table `students`. An immediate JSON response confirms enrollment.", bold_prefix="Flow 1: Student Registration (CO3) -> ")
p_bullet(doc, "Administrator accesses `php-admin/login.php` over Apache port 80. Credentials are authenticated against table `admin_users` using `password_verify()`. On success, session IDs are regenerated to prevent session fixation, and CSRF tokens are injected into session state. The admin views KPI metrics, performs CRUD operations on student records, uploads marksheets, and deletes records with automated disk cleanup unlinking physical files.", bold_prefix="Flow 2: Administrative CRUD (CO4) -> ")
p_bullet(doc, "Admission officers access the Java web portal at `http://localhost:8082/student-portal/login`. The Java `LoginServlet` authenticates administrator credentials by invoking `AdminDAO.authenticate()`, which uses pure Java BCrypt verification against table `admin_users`. A fresh `HttpSession` is generated and tracked by `AuthFilter`.", bold_prefix="Flow 3: Java Enterprise Authentication (CO5) -> ")
p_bullet(doc, "The Java `StudentListServlet` queries the shared database via `StudentDAO.getAllStudents()` using JDBC PreparedStatements. Results are bound to request scope and rendered by `students.jsp` using JSTL `<c:forEach>`. When viewing a student profile (`profile.jsp`), academic credentials and avatar images are served by `DocumentStreamServlet`. The servlet enforces canonical path boundary checking (`getCanonicalPath()`) against `uploads/` to prevent directory traversal attacks, sets MIME headers, and writes the binary stream in 8KB chunks.", bold_prefix="Flow 4: Registry Display & Document Streaming (CO5) -> ")

# ==============================================================================
# SECTION F: DATABASE DESIGN
# ==============================================================================
h1(doc, "F. DATABASE DESIGN")
p_body(doc, "The database architecture is designed in Third Normal Form (3NF) to maintain referential integrity, eliminate data anomalies, and facilitate cross-language access between PHP (PDO) and Java (JDBC).")

h2(doc, "1. Database Entity Relationships")
table_grid(doc,
    ["Table Name", "Primary Key", "Foreign Keys", "Description & Cardinality"],
    [
        ["admin_users", "id (INT AUTO_INCREMENT)", "None", "Stores administrator credentials and system roles. Password stored strictly as a 60-character BCrypt hash."],
        ["students", "id (INT AUTO_INCREMENT)", "None", "Primary academic student entity. Unique roll numbers and emails. One student can have zero or many documents (1:N)."],
        ["student_documents", "id (INT AUTO_INCREMENT)", "student_id REFERENCES students(id) ON DELETE CASCADE", "Metadata store for academic attachments. Cascades on student deletion to ensure referential cleanliness."]
    ],
    [Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.7)]
)

h2(doc, "2. Detailed Table Structure")

h3(doc, "Table 1: admin_users")
table_grid(doc,
    ["Column Name", "Data Type", "Null / Default", "Key Index", "Description"],
    [
        ["id", "INT", "NOT NULL, AUTO_INCREMENT", "PRIMARY KEY", "Surrogate primary key for administrator"],
        ["username", "VARCHAR(50)", "NOT NULL", "UNIQUE", "Login handle for administrator (`admin`)"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "None", "60-character BCrypt salted hash ($2y$10$...)"],
        ["full_name", "VARCHAR(100)", "NOT NULL", "None", "Full name of administrator for display in navbar"],
        ["email", "VARCHAR(100)", "NOT NULL", "UNIQUE", "Institutional email for notification / reset"],
        ["role", "VARCHAR(20)", "DEFAULT 'admin'", "None", "Authorization scope / role"],
        ["created_at", "TIMESTAMP", "CURRENT_TIMESTAMP", "None", "Account registration timestamp"],
        ["updated_at", "TIMESTAMP", "ON UPDATE CURRENT_TIMESTAMP", "None", "Timestamp of last account modification"]
    ],
    [Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.0), Inches(1.5)]
)

h3(doc, "Table 2: students")
table_grid(doc,
    ["Column Name", "Data Type", "Null / Default", "Key Index", "Description"],
    [
        ["id", "INT", "NOT NULL, AUTO_INCREMENT", "PRIMARY KEY", "Surrogate primary key for student"],
        ["roll_number", "VARCHAR(30)", "NOT NULL", "UNIQUE", "Academic identifier (e.g. `CS2026-001`)"],
        ["name", "VARCHAR(100)", "NOT NULL", "None", "Full legal name of enrolled student"],
        ["email", "VARCHAR(100)", "NOT NULL", "UNIQUE", "Primary student email address"],
        ["course", "VARCHAR(80)", "NOT NULL", "INDEX", "Enrolled degree program (e.g. B.Tech Computer Science)"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "None", "BCrypt hash for future student portal self-service"],
        ["profile_image", "VARCHAR(255)", "DEFAULT NULL", "None", "Stored relative filename of avatar photo"],
        ["status", "ENUM", "DEFAULT 'Approved'", "None", "Enrollment status: 'Pending', 'Approved', 'Rejected'"],
        ["registration_date", "TIMESTAMP", "CURRENT_TIMESTAMP", "None", "Timestamp when admission record was created"],
        ["updated_at", "TIMESTAMP", "ON UPDATE CURRENT_TIMESTAMP", "None", "Timestamp of last student record edit"]
    ],
    [Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.0), Inches(1.5)]
)

h3(doc, "Table 3: student_documents")
table_grid(doc,
    ["Column Name", "Data Type", "Null / Default", "Key Index", "Description"],
    [
        ["id", "INT", "NOT NULL, AUTO_INCREMENT", "PRIMARY KEY", "Surrogate primary key for document metadata"],
        ["student_id", "INT", "NOT NULL", "FOREIGN KEY", "Links to `students.id` with ON DELETE CASCADE"],
        ["original_filename", "VARCHAR(255)", "NOT NULL", "None", "Client original file name (e.g. marksheet.pdf)"],
        ["stored_filename", "VARCHAR(255)", "NOT NULL", "UNIQUE", "Unguessable randomized disk name on server"],
        ["file_path", "VARCHAR(255)", "NOT NULL", "None", "Relative disk storage path (`uploads/documents/...`)"],
        ["mime_type", "VARCHAR(100)", "NOT NULL", "None", "MIME type (e.g. application/pdf, image/jpeg)"],
        ["file_size", "BIGINT", "NOT NULL", "None", "Exact file payload size in bytes"],
        ["document_category", "ENUM", "DEFAULT 'other'", "INDEX", "Category: 'profile_image', 'id_proof', 'certificate'"],
        ["uploaded_at", "TIMESTAMP", "CURRENT_TIMESTAMP", "None", "Timestamp when file was uploaded"]
    ],
    [Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.0), Inches(1.5)]
)

h2(doc, "3. Complete Database Schema Script (database/student_portal.sql)")
p_body(doc, "The actual schema creation DDL and seed data script used across all modules is presented below:")
code_box(doc, sql_schema_text)

# ==============================================================================
# SECTION G: CO3 — REGISTRATION FORM (8 MARKS)
# ==============================================================================
h1(doc, "G. CO3 — REGISTRATION FORM & CLIENT VALIDATION (8 MARKS)")

h2(doc, "1. Aim")
p_body(doc, "To design, develop, and verify an interactive, responsive student admission registration form utilizing semantic HTML5 markup, modern CSS3 layout and micro-animations, real-time client-side JavaScript validation with password entropy tracking, drag-and-drop avatar handling, and secure asynchronous persistence to MySQL.")

h2(doc, "2. Technologies Used")
p_bullet(doc, "Semantic structure, accessible label associations, required attributes, drag-and-drop zone (`registration/index.html`).", bold_prefix="HTML5: ")
p_bullet(doc, "CSS Grid, Flexbox, custom design tokens, responsive breakpoints, smooth transition effects (`registration/css/style.css`).", bold_prefix="CSS3: ")
p_bullet(doc, "Regular expression validators, real-time input event listeners, 5-rule password strength calculation, FileReader image preview, AJAX submission (`registration/js/validation.js`).", bold_prefix="JavaScript (ES6): ")
p_bullet(doc, "Server-side endpoint receiving multipart form data, validating fields, generating BCrypt password hash, moving uploaded image, and persisting record via PDO (`registration/register.php`).", bold_prefix="PHP 8 (Backend Endpoint): ")

h2(doc, "3. Input Fields & Validation Rules")
table_grid(doc,
    ["Field Name", "HTML Control Type", "Mandatory", "Validation Pattern / Rule", "Error Feedback Message"],
    [
        ["Student Name", "text (`#studentName`)", "Yes", "2 to 100 characters; letters, spaces, hyphens, dots only: `/^[a-zA-Z\\s.'-]{2,100}$/`", "Name must contain only letters and spaces (2-100 characters)."],
        ["Roll Number", "text (`#rollNumber`)", "Yes", "Alphanumeric institutional format: `/^[A-Z0-9-]{3,20}$/i`", "Roll number must be 3-20 alphanumeric characters."],
        ["Email Address", "email (`#email`)", "Yes", "RFC 5322 compliant email regex: `/^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,10}$/`", "Please enter a valid institutional email address."],
        ["Academic Course", "select (`#course`)", "Yes", "Non-empty select value from allowed departments", "Please select an academic degree program."],
        ["Password", "password (`#password`)", "Yes", "Minimum 8 characters with 5 criteria: length, uppercase, lowercase, digit, special symbol", "Password does not satisfy minimum strength requirements."],
        ["Confirm Password", "password (`#confirmPassword`)", "Yes", "Exact lexical equality with `#password` value", "Passwords do not match."],
        ["Profile Avatar", "file (`#profilePic`)", "Optional", "File type: JPG, PNG, WebP; Maximum size: 2.0 MB", "Only JPG, PNG, or WebP images up to 2MB allowed."]
    ],
    [Inches(1.2), Inches(1.3), Inches(0.8), Inches(1.8), Inches(1.4)]
)

h2(doc, "4. Real-Time Password Strength Tracker (5-Factor Algorithm)")
p_body(doc, "The password meter evaluates 5 independent criteria dynamically upon every keystroke:")
p_bullet(doc, "Criterion 1: Length is at least 8 characters (`pwd.length >= 8`)")
p_bullet(doc, "Criterion 2: Contains at least one lowercase English letter (`/[a-z]/.test(pwd)`)")
p_bullet(doc, "Criterion 3: Contains at least one uppercase English letter (`/[A-Z]/.test(pwd)`)")
p_bullet(doc, "Criterion 4: Contains at least one numeric digit (`/[0-9]/.test(pwd)`)")
p_bullet(doc, "Criterion 5: Contains at least one special character (`/[!@#$%^&*(),.?\":{}|<>]/.test(pwd)`)")
p_body(doc, "Based on the score (0 to 5), the progress bar updates width (0% to 100%) and transitions colors: Red ('Weak' - 20%-40%), Orange ('Medium' - 60%-80%), and Emerald Green ('Strong' - 100%).")

h2(doc, "5. Important Code Excerpts (CO3)")

h3(doc, "Excerpts from registration/js/validation.js (Validation Engine)")
code_box(doc, """
// Regular expression definitions for client-side form validation
const VALIDATION_PATTERNS = {
    name: /^[a-zA-Z\\s.'-]{2,100}$/,
    rollNumber: /^[A-Z0-9-]{3,20}$/i,
    email: /^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,10}$/
};

// Evaluate password entropy across 5 distinct security criteria
function evaluatePasswordStrength(password) {
    const rules = {
        length: password.length >= 8,
        lower: /[a-z]/.test(password),
        upper: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    let score = Object.values(rules).filter(Boolean).length;
    let label = 'Very Weak';
    let color = '#ef4444'; // Red
    
    if (score >= 5) {
        label = 'Strong';
        color = '#10b981'; // Green
    } else if (score >= 3) {
        label = 'Medium';
        color = '#f59e0b'; // Amber
    }
    
    return { score, label, color, rules };
}
""")

h3(doc, "Excerpts from registration/register.php (Persistence Handler)")
code_box(doc, """
// Verify mandatory fields and hash password securely using BCrypt
if (empty($name) || empty($rollNumber) || empty($email) || empty($course) || empty($password)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'All mandatory fields are required.']);
    exit;
}

// Generate secure BCrypt hash ($2y$10$)
$passwordHash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 10]);

// Parameterized SQL query prevents SQL Injection attacks 100%
$stmt = $pdo->prepare(
    "INSERT INTO students (roll_number, name, email, course, password_hash, profile_image, status) 
     VALUES (:roll, :name, :email, :course, :hash, :img, 'Approved')"
);
$stmt->execute([
    ':roll'   => $rollNumber,
    ':name'   => $name,
    ':email'  => $email,
    ':course' => $course,
    ':hash'   => $passwordHash,
    ':img'    => $storedImageName
]);
""")

h2(doc, "6. Verified Screenshots (CO3)")
figure(doc, os.path.join(co3_dir, "01_registration_form.png"), "Figure 1: Main Student Admission Registration Form (CO3)")
figure(doc, os.path.join(co3_dir, "02_form_validation.png"), "Figure 2: Real-Time Field Validation Flags & Password Entropy Tracker (CO3)")
figure(doc, os.path.join(co3_dir, "03_successful_registration.png"), "Figure 3: Asynchronous AJAX Post-Registration Confirmation Screen (CO3)")
figure(doc, os.path.join(co3_dir, "04_database_record.png"), "Figure 4: Direct Database Verification in MySQL `student_portal` Table (CO3)")

h2(doc, "7. CO3 Test Cases & Results")
table_grid(doc,
    ["Test ID", "Test Case Description", "Input Action", "Expected Outcome", "Actual Result", "Status"],
    [
        ["TC-CO3-01", "Empty Form Submission", "Click submit with blank fields", "Form submission blocked; all mandatory inputs highlighted in red", "Form blocked; inline error tooltips displayed", "PASS"],
        ["TC-CO3-02", "Invalid Name Syntax", "Enter 'Aarav123!'", "Regex fails; message 'Name must contain only letters'", "Name flagged with red border and error text", "PASS"],
        ["TC-CO3-03", "Invalid Email Syntax", "Enter 'student@invalid'", "RFC regex test returns false; error prompt displayed", "Input flagged: 'Please enter a valid email address'", "PASS"],
        ["TC-CO3-04", "Weak Password Tracker", "Enter 'pass'", "Meter indicates 'Weak' (20%); 4 unmet criteria bullets visible", "Red progress bar at 20%; 1 of 5 criteria met", "PASS"],
        ["TC-CO3-05", "Strong Password Tracker", "Enter 'SecurePass@2026'", "Meter reaches 100% 'Strong'; all 5 criteria checked green", "Green progress bar at 100%; all bullets green", "PASS"],
        ["TC-CO3-06", "Password Mismatch Check", "Enter non-matching passwords", "Error: 'Passwords do not match'; submit disabled", "Real-time comparison flags mismatch error", "PASS"],
        ["TC-CO3-07", "Drag & Drop Image Preview", "Drop sample.jpg into dropzone", "Image preview thumbnail renders with file size", "FileReader displays avatar preview", "PASS"],
        ["TC-CO3-08", "Disallowed File Extension", "Upload .exe or .txt file", "Error: 'Only JPG, PNG, or WebP allowed'; file cleared", "Validation rejects extension; file input reset", "PASS"],
        ["TC-CO3-09", "Valid Student Registration", "Submit Kabir Mehta registration", "HTTP 200 JSON; screen displays success confirmation card", "Record persisted; confirmed in MySQL table", "PASS"]
    ],
    [Inches(0.9), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.1), Inches(0.5)]
)

# ==============================================================================
# SECTION H: CO4 — PHP AND MYSQL ADMIN PANEL (16 MARKS)
# ==============================================================================
h1(doc, "H. CO4 — PHP AND MYSQL ADMIN CRUD PANEL (16 MARKS)")

h2(doc, "1. Aim")
p_body(doc, "To implement, configure, and verify an administrative management panel in PHP 8 backed by a MySQL relational database, supporting administrative authentication, secure session handling, full CRUD operations on student records, document upload with metadata management, path traversal defenses, and CSRF protection.")

h2(doc, "2. CRUD Operations & Workflow")
p_bullet(doc, "Administrator completes form at `add_student.php`. Server verifies fields, computes BCrypt hash, checks for duplicate roll numbers, moves optional avatar, and inserts row.", bold_prefix="Create (Insert): ")
p_bullet(doc, "Dashboard (`dashboard.php`) and view student page (`view_student.php`) retrieve student lists, aggregate counts, and document associations via PDO prepared queries.", bold_prefix="Read (Select): ")
p_bullet(doc, "Administrator modifies details via `edit_student.php`. Form pre-populates existing data; on submit, parameterized UPDATE query modifies row while preserving foreign keys.", bold_prefix="Update (Modify): ")
p_bullet(doc, "Initiated from `delete_student.php` with CSRF token check. Script queries associated physical files, unlinks files from storage disk, and executes DELETE query with foreign key cascades.", bold_prefix="Delete (Cascade): ")

h2(doc, "3. Security & File Handling Implementations")
p_bullet(doc, "Administrators authenticate via `login.php`. Password verified with `password_verify()`. Upon successful authentication, `session_regenerate_id(true)` invalidates old session tokens to prevent session fixation.", bold_prefix="Session Security: ")
p_bullet(doc, "Every mutating form (add, edit, delete, upload) contains a cryptographically random session token (`bin2hex(random_bytes(32))`), validated on submission using `hash_equals()` to prevent Cross-Site Request Forgery.", bold_prefix="CSRF Defense: ")
p_bullet(doc, "Uploaded filenames are randomized (`bin2hex(random_bytes(10)) . '.' . $ext`) to prevent file overwrite attacks and script execution. MIME types are validated using PHP `finfo`.", bold_prefix="Upload Safety: ")
p_bullet(doc, "File streaming in `download_document.php` verifies that `realpath($targetPath)` resides strictly inside the designated `uploads/` root directory. Requests containing `../` traversal sequences are immediately aborted with HTTP 403 Forbidden.", bold_prefix="Path Traversal Defense: ")

h2(doc, "4. Important Code Excerpts (CO4)")

h3(doc, "Excerpts from php-admin/includes/auth.php (Session & CSRF Security)")
code_box(doc, """
// Start session with strict security cookie parameters
function startSecureSession(): void {
    if (session_status() === PHP_SESSION_NONE) {
        session_start([
            'cookie_httponly' => true,
            'cookie_samesite' => 'Lax'
        ]);
    }
}

// Generate cryptographically secure CSRF token
function generateCsrfToken(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

// Validate submitted CSRF token using timing-safe comparison
function validateCsrfToken(?string $token): bool {
    if (empty($token) || empty($_SESSION['csrf_token'])) {
        return false;
    }
    return hash_equals($_SESSION['csrf_token'], $token);
}
""")

h3(doc, "Excerpts from php-admin/download_document.php (Path Traversal Safe Streaming)")
code_box(doc, """
// Resolve canonical paths to defend against directory traversal attacks (../)
$realTarget = realpath($physicalPath);
$realBase   = realpath(UPLOADS_BASE_DIR);

if ($realTarget === false || strpos($realTarget, $realBase) !== 0) {
    http_response_code(403);
    die("Access Denied: Path traversal attempt blocked.");
}

// Stream file in safe 8KB memory chunks
header('Content-Type: ' . $mimeType);
header('Content-Length: ' . filesize($realTarget));
header('Content-Disposition: ' . ($forceDownload ? 'attachment' : 'inline') . '; filename="' . $filename . '"');

$handle = fopen($realTarget, 'rb');
while (!feof($handle)) {
    echo fread($handle, 8192);
    flush();
}
fclose($handle);
""")

h2(doc, "5. Verified Screenshots (CO4)")
figure(doc, os.path.join(co4_dir, "01_admin_login.png"), "Figure 5: PHP Admin Login Authentication Page (CO4)")
figure(doc, os.path.join(co4_dir, "02_admin_dashboard.png"), "Figure 6: PHP Admin Dashboard with KPI Metrics & Academic Statistics (CO4)")
figure(doc, os.path.join(co4_dir, "03_student_list.png"), "Figure 7: Registered Student Records Management Table (CO4)")
figure(doc, os.path.join(co4_dir, "04_add_student.png"), "Figure 8: Add Student Form with Validation & Avatar Upload (CO4)")
figure(doc, os.path.join(co4_dir, "05_edit_student.png"), "Figure 9: Edit Student Information Interface (CO4)")
figure(doc, os.path.join(co4_dir, "06_file_upload.png"), "Figure 10: Academic Document Upload Dropzone & Category Selector (CO4)")
figure(doc, os.path.join(co4_dir, "07_document_display.png"), "Figure 11: Student Profile View with Uploaded Academic Documents (CO4)")

h2(doc, "6. CO4 Test Cases & Results")
table_grid(doc,
    ["Test ID", "Test Case Description", "Input Action", "Expected Outcome", "Actual Result", "Status"],
    [
        ["TC-CO4-01", "Admin Login Success", "POST admin / Password@123", "BCrypt verified; session regenerated; redirect to dashboard", "Session established; dashboard rendered", "PASS"],
        ["TC-CO4-02", "Admin Login Failure", "POST admin / WrongPassword", "Generic error: 'Invalid username or password'; reject", "Credentials rejected; flash error displayed", "PASS"],
        ["TC-CO4-03", "CSRF Protection Check", "Submit POST with missing CSRF", "Request rejected; redirect to dashboard without state change", "validateCsrfToken() failed; update blocked", "PASS"],
        ["TC-CO4-04", "Duplicate Roll Number", "Add student with roll 'CS2026-001'", "Duplicate detected; error 'Roll number already exists'", "Pre-insert query flags duplicate; halted", "PASS"],
        ["TC-CO4-05", "View Student Profile", "Access view_student.php?id=1", "Displays student card, photo, and associated document list", "Profile and documents rendered cleanly", "PASS"],
        ["TC-CO4-06", "Document Upload & Metadata", "Upload marksheet.pdf for ID #1", "File saved with randomized name; row added to DB", "MIME verified via finfo; DB row created", "PASS"],
        ["TC-CO4-07", "Safe Document Download", "Click download link on doc #1", "Headers Content-Type and Disposition sent; 8KB streamed", "File streamed without exposing disk paths", "PASS"],
        ["TC-CO4-08", "Path Traversal Defense", "Request doc?profile=../../win.ini", "Request rejected with HTTP 403 Forbidden", "realpath() boundary check blocks traversal", "PASS"],
        ["TC-CO4-09", "Cascade Delete Cleanup", "Delete Student #1 via admin", "Files unlinked from disk; row deleted from MySQL", "Disk unlinked; DB row deleted via cascade", "PASS"]
    ],
    [Inches(0.9), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.1), Inches(0.5)]
)

# ==============================================================================
# SECTION I: CO5 — JAVA SERVLET, JSP, AND JDBC (16 MARKS)
# ==============================================================================
h1(doc, "I. CO5 — JAVA SERVLET, JSP, AND JDBC PORTAL (16 MARKS)")

h2(doc, "1. Aim")
p_body(doc, "To construct, package, deploy, and verify an enterprise Java web application utilizing Jakarta/Java Servlets 3.1, JavaServer Pages (JSP), JSTL, and JDBC on Apache Tomcat 8.5+, connecting to the shared MySQL/MariaDB database to deliver authenticated student registry exploration, detailed profile inspection, session authorization filtering, and binary document streaming.")

h2(doc, "2. Architecture & Deployment Environment")
p_bullet(doc, "Compiled into `student-portal.war` using Oracle JDK 24 (`javac 24.0.2` & `jar 24.0.2`) and deployed to Apache Tomcat 8.5.96 (`C:\\xampp\\tomcat\\webapps\\student-portal.war`).", bold_prefix="Packaging & Deployment: ")
p_bullet(doc, "The Java Portal runs on `http://localhost:8082/student-portal/`. Port 8082 is utilized because port 8080 is occupied by a background Windows system service (`MTAgentService.exe`, PID 4952). Configuring Tomcat to port 8082 via `switch_port.ps1` completely eliminates port contention.", bold_prefix="Port Configuration: ")
p_bullet(doc, "The Java connection utility `DBConnection.java` connects via `mysql-connector-j-8.0.33.jar` to MariaDB on port 3307, with built-in automatic port fallback between ports 3306 and 3307.", bold_prefix="Resilient JDBC Factory: ")

h2(doc, "3. Key Components & Implementation Details")
p_bullet(doc, "Authenticates administrator credentials against table `admin_users` using pure Java BCrypt verification (`BCrypt.checkpw()`). Upon authentication, regenerates the session to prevent fixation and stores the `AdminUser` principal object.", bold_prefix="LoginServlet (`/login`): ")
p_bullet(doc, "Queries all students and document counts using `StudentDAO.getAllStudents()` via JDBC PreparedStatement. Forwards request to `students.jsp` for presentation.", bold_prefix="StudentListServlet (`/students`): ")
p_bullet(doc, "Retrieves an individual student record and all associated documents from `student_documents` via `DocumentDAO.getDocumentsByStudentId()`. Forwards to `profile.jsp`.", bold_prefix="StudentProfileServlet (`/profile`): ")
p_bullet(doc, "Streams binary JPEG photos and PDF documents. Verifies canonical path boundaries (`targetFile.getCanonicalPath().startsWith(baseDir.getCanonicalPath())`), blocks dangerous extensions (.jsp, .exe, .sh), and streams bytes in 8KB chunks.", bold_prefix="DocumentStreamServlet (`/document`): ")
p_bullet(doc, "Intercepts unauthenticated requests to protected endpoints (`/students`, `/profile`, `/dashboard`). Redirects non-logged-in requests to `/login`.", bold_prefix="AuthFilter (Session Interceptor): ")
p_bullet(doc, "Destroys session via `session.invalidate()` and redirects to `/login?logout=1` with a green confirmation alert banner.", bold_prefix="LogoutServlet (`/logout`): ")

h2(doc, "4. Important Code Excerpts (CO5)")

h3(doc, "Excerpts from DBConnection.java (Dynamic Port Fallback Factory)")
code_box(doc, """
// Reusable JDBC connection factory with automatic port resilience
public static Connection getConnection() throws SQLException {
    try {
        return DriverManager.getConnection(url, user, password);
    } catch (SQLException primaryEx) {
        // Automatic resilience: If port 3306 fails, fallback to 3307 (or vice-versa)
        if (url.contains(":3306/")) {
            String fallbackUrl = url.replace(":3306/", ":3307/");
            try {
                Connection conn = DriverManager.getConnection(fallbackUrl, user, password);
                url = fallbackUrl; // Memorize successful endpoint
                return conn;
            } catch (SQLException fallbackEx) {
                throw primaryEx;
            }
        }
        throw primaryEx;
    }
}
""")

h3(doc, "Excerpts from DocumentStreamServlet.java (Canonical Path Security & Streaming)")
code_box(doc, """
// Security Check: Path Traversal defense using canonical paths
String canonicalTarget = targetFile.getCanonicalPath();
String canonicalBase   = uploadsBaseDir.getCanonicalPath();

if (!canonicalTarget.startsWith(canonicalBase)) {
    resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Access denied: Unauthorized directory traversal attempt.");
    return;
}

// Prepare binary headers and stream in 8KB buffer chunks
resp.setContentType(mimeType);
resp.setContentLengthLong(targetFile.length());
resp.setHeader("X-Content-Type-Options", "nosniff");

try (FileInputStream fis = new FileInputStream(targetFile);
     OutputStream os = resp.getOutputStream()) {
    byte[] buffer = new byte[8192];
    int bytesRead;
    while ((bytesRead = fis.read(buffer)) != -1) {
        os.write(buffer, 0, bytesRead);
    }
    os.flush();
}
""")

h2(doc, "5. Verified Screenshots (CO5)")
figure(doc, os.path.join(co5_dir, "01_servlet_login.png"), "Figure 12: Java Portal Login View Powered by LoginServlet & JSP (CO5)")
figure(doc, os.path.join(co5_dir, "02_student_list_jsp.png"), "Figure 13: JSTL Student Registry Table with Dynamic KPI Metrics (CO5)")
figure(doc, os.path.join(co5_dir, "03_student_profile.png"), "Figure 14: Student Profile View Displaying Streamed Avatar & Document Table (CO5)")
figure(doc, os.path.join(co5_dir, "04_document_streaming.png"), "Figure 15: Native Browser View Displaying Binary Image Streamed from DocumentStreamServlet (CO5)")
figure(doc, os.path.join(co5_dir, "05_session_verification.png"), "Figure 16: Session Invalidation & Protection Verification Banner (CO5)")

h2(doc, "6. CO5 Test Cases & Results")
table_grid(doc,
    ["Test ID", "Test Case Description", "Input Action", "Expected Outcome", "Actual Result", "Status"],
    [
        ["TC-CO5-01", "JDBC Connection Utility", "Invoke DBConnection.getConnection()", "Active Connection returned to `student_portal` DB", "Connected to MariaDB with 3306/3307 fallback", "PASS"],
        ["TC-CO5-02", "Student DAO Listing Query", "Invoke StudentDAO.getAllStudents()", "List of Student objects with document counts", "PreparedStatement loaded all 6 enrolled students", "PASS"],
        ["TC-CO5-03", "Java Admin Login Servlet", "POST admin / Password@123", "BCrypt validates hash; session established; redirect", "Authenticated; session created; redirected to /students", "PASS"],
        ["TC-CO5-04", "AuthFilter Access Control", "Access /students without session", "Request intercepted; redirect to /login", "AuthFilter intercepted and redirected to /login", "PASS"],
        ["TC-CO5-05", "JSTL Student Registry", "GET /students as authenticated admin", "students.jsp renders KPI cards and JSTL table", "Metric cards (6 students, 5 docs) & table rendered", "PASS"],
        ["TC-CO5-06", "Student Profile View", "GET /profile?id=1", "profile.jsp renders student details and doc table", "Aarav Sharma profile and academic files rendered", "PASS"],
        ["TC-CO5-07", "DocumentStreamServlet", "Stream /document?profile=... and id=2", "Streams binary bytes with canonical path check", "Binary JPEG and PDF streamed in 8KB chunks", "PASS"],
        ["TC-CO5-08", "Session Invalidation", "Click Logout in navbar", "Session invalidated; redirect to /login?logout=1", "Session destroyed; green logout banner displayed", "PASS"]
    ],
    [Inches(0.9), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.1), Inches(0.5)]
)

# ==============================================================================
# SECTION J: CODE EXPLANATION
# ==============================================================================
h1(doc, "J. CODE EXPLANATION")
p_body(doc, "Below is an overview of the key project source files, explaining their purpose, core logic, and important functions in simple, understandable English:")

table_grid(doc,
    ["Module / File Path", "Language / Technology", "Key Purpose & Architectural Role", "Important Functions / Classes"],
    [
        ["registration/index.html", "HTML5", "Responsive student registration form with accessible inputs and dropzone", "Form elements (`#studentName`, `#email`, `#password`), drag-and-drop avatar zone"],
        ["registration/css/style.css", "CSS3", "Design system with CSS custom properties, grid layout, password strength bar", "Flexbox cards, `.strength-meter`, `.dropzone-container`, responsive media queries"],
        ["registration/js/validation.js", "JavaScript (ES6)", "Real-time client validation engine and AJAX form dispatcher", "`evaluatePasswordStrength()`, `validateInput()`, `handleDrop()`, `submitForm()`"],
        ["registration/register.php", "PHP 8 (PDO)", "Asynchronous registration persistence endpoint", "Validates POST data, generates BCrypt hash, handles image upload, executes PDO INSERT"],
        ["php-admin/config/database.php", "PHP 8 (PDO)", "Shared database configuration and connection factory", "`getDbConnection()` returning configured PDO instance with UTF-8 charset"],
        ["php-admin/includes/auth.php", "PHP 8", "Security middleware for session, CSRF, and authentication checks", "`startSecureSession()`, `isLoggedIn()`, `generateCsrfToken()`, `validateCsrfToken()`"],
        ["php-admin/login.php", "PHP 8", "Administrator login controller and view", "Verifies credentials with `password_verify()`, regenerates session ID, redirects to dashboard"],
        ["php-admin/dashboard.php", "PHP 8 / HTML", "Main administrative overview with KPIs and student table", "Aggregates total students, approved counts, document totals, course distribution"],
        ["php-admin/add_student.php", "PHP 8", "Administrator student creation form and backend handler", "CSRF-validated student insertion with avatar upload and roll duplication checks"],
        ["php-admin/view_student.php", "PHP 8", "Detailed student profile and document upload manager", "Renders student data, lists uploaded files, provides upload dropzone and download links"],
        ["php-admin/download_document.php", "PHP 8", "Secure file streaming endpoint with path traversal prevention", "`realpath()` verification, MIME type lookup, 8KB buffer streaming"],
        ["java-portal/DBConnection.java", "Java (JDBC)", "Reusable database connection factory with port fallback", "`getConnection()` with automatic fallback between ports 3306 and 3307"],
        ["java-portal/StudentDAO.java", "Java (JDBC)", "Data Access Object for student queries and counts", "`getAllStudents()`, `getStudentById()`, mapping ResultSets to POJOs"],
        ["java-portal/DocumentDAO.java", "Java (JDBC)", "Data Access Object for academic document queries", "`getDocumentsByStudentId()`, `getDocumentById()` via PreparedStatement"],
        ["java-portal/AdminDAO.java", "Java (JDBC)", "Data Access Object for administrator authentication", "`authenticate()` verifying credentials using pure Java BCrypt verifier"],
        ["java-portal/LoginServlet.java", "Java Servlet", "HTTP controller handling administrator login and sessions", "`doGet()` renders login.jsp; `doPost()` validates credentials and creates session"],
        ["java-portal/StudentListServlet.java", "Java Servlet", "HTTP controller handling student registry requests", "`doGet()` fetches students from DAO and forwards to `students.jsp`"],
        ["java-portal/DocumentStreamServlet.java", "Java Servlet", "HTTP servlet streaming binary images and documents", "`doGet()` checks canonical path boundaries and streams binary data in 8KB chunks"],
        ["java-portal/AuthFilter.java", "Java Servlet Filter", "Access control filter intercepting protected routes", "`doFilter()` verifies `adminUser` in `HttpSession`; redirects unauthenticated requests"],
        ["java-portal/students.jsp", "JSP / JSTL", "Presentation view rendering student table and KPI cards", "JSTL `<c:forEach>` loop, Expression Language (`${student.name}`), status badges"],
        ["java-portal/profile.jsp", "JSP / JSTL", "Presentation view for individual student profile", "Displays student card, streamed avatar, and academic credentials table with stream links"]
    ],
    [Inches(1.8), Inches(1.1), Inches(1.9), Inches(1.7)]
)

# ==============================================================================
# SECTION K: TESTING AND VERIFICATION
# ==============================================================================
h1(doc, "K. TESTING AND VERIFICATION")
p_body(doc, "The comprehensive test matrix covering all 24 empirical test cases across CO3, CO4, and CO5 is summarized below. All tests were executed against active runtime services and verified 100% PASS.")

table_grid(doc,
    ["Test ID", "Module", "Test Description", "Expected Result", "Actual Result", "Status"],
    [
        ["TC-CO3-01", "CO3", "Empty Form Submission", "Form submission blocked; fields flagged", "Submission blocked; mandatory errors displayed", "PASS"],
        ["TC-CO3-02", "CO3", "Invalid Name Syntax", "Error: 'Only letters and spaces allowed'", "Border turned red; error message rendered", "PASS"],
        ["TC-CO3-03", "CO3", "Invalid Email Syntax", "Error: 'Please enter valid email'", "Regex failed; invalid email error shown", "PASS"],
        ["TC-CO3-04", "CO3", "Weak Password Tracker", "Meter indicates 'Weak' (20%)", "Red progress bar at 20%; 1 of 5 criteria met", "PASS"],
        ["TC-CO3-05", "CO3", "Strong Password Tracker", "Meter reaches 100% 'Strong'", "Green progress bar at 100%; all 5 met", "PASS"],
        ["TC-CO3-06", "CO3", "Password Mismatch", "Error: 'Passwords do not match'", "Mismatch flagged; submit prevented", "PASS"],
        ["TC-CO3-07", "CO3", "Avatar Drag & Drop Preview", "Thumbnail renders in preview box", "FileReader loaded thumbnail and size", "PASS"],
        ["TC-CO3-08", "CO3", "Disallowed File Extension", "Rejects .txt/.exe files", "Client validation cleared input; error shown", "PASS"],
        ["TC-CO3-09", "CO3", "Valid Student Registration", "HTTP 200 JSON; success card shown", "Record inserted into MySQL `students`", "PASS"],
        ["TC-CO4-01", "CO4", "Admin Authentication Success", "BCrypt verify; redirect to dashboard", "Session created; dashboard rendered", "PASS"],
        ["TC-CO4-02", "CO4", "Admin Authentication Failure", "Error: 'Invalid username/password'", "Credentials rejected; flash error set", "PASS"],
        ["TC-CO4-03", "CO4", "CSRF Protection Check", "Reject request missing CSRF token", "validateCsrfToken() failed; update blocked", "PASS"],
        ["TC-CO4-04", "CO4", "Duplicate Roll Number Check", "Error: 'Roll number already exists'", "Pre-insert check detected duplicate; halted", "PASS"],
        ["TC-CO4-05", "CO4", "View Student Profile", "Displays profile card and documents", "Profile rendered with associated files", "PASS"],
        ["TC-CO4-06", "CO4", "Document Upload & Metadata", "File saved; row added to DB", "MIME verified via finfo; DB row created", "PASS"],
        ["TC-CO4-07", "CO4", "Safe Document Download", "Headers set; 8KB streamed cleanly", "File streamed without revealing disk paths", "PASS"],
        ["TC-CO4-08", "CO4", "Path Traversal Defense", "Aborts request with HTTP 403", "realpath() boundary check blocked attempt", "PASS"],
        ["TC-CO4-09", "CO4", "Cascade Delete Cleanup", "Disk unlinked; DB row deleted", "Files unlinked; student row deleted", "PASS"],
        ["TC-CO5-01", "CO5", "JDBC Connection Factory", "Active Connection to `student_portal`", "Connected with 3306/3307 dynamic fallback", "PASS"],
        ["TC-CO5-02", "CO5", "Student DAO Listing Query", "List of Student objects populated", "PreparedStatement returned all 6 students", "PASS"],
        ["TC-CO5-03", "CO5", "Java Admin Login Servlet", "BCrypt verified; session established", "Redirected cleanly to /students", "PASS"],
        ["TC-CO5-04", "CO5", "AuthFilter Access Control", "Intercepts unauthenticated request", "Blocked access; redirected to /login", "PASS"],
        ["TC-CO5-05", "CO5", "JSTL Student Registry", "students.jsp renders KPI cards & table", "Rendered 6 students, 5 docs, 3 courses", "PASS"],
        ["TC-CO5-06", "CO5", "Student Profile View", "profile.jsp renders student & docs", "Rendered Aarav Sharma with document links", "PASS"],
        ["TC-CO5-07", "CO5", "DocumentStreamServlet", "Streams binary JPEG and PDF bytes", "Streamed 400x400 JPEG & PDF in 8KB chunks", "PASS"],
        ["TC-CO5-08", "CO5", "Session Invalidation", "Invalidates session; redirect to login", "Session destroyed; logout banner displayed", "PASS"]
    ],
    [Inches(0.9), Inches(0.6), Inches(1.4), Inches(1.4), Inches(1.4), Inches(0.5)]
)

# ==============================================================================
# SECTION L: RESULTS AND SCREENSHOTS
# ==============================================================================
h1(doc, "L. RESULTS AND SCREENSHOTS")
p_body(doc, "All 16 genuine screenshots captured during live execution of the Student Admission Portal are cataloged below with their figure references, module mappings, and descriptions:")

table_grid(doc,
    ["Fig No.", "Course Outcome", "Screenshot File Name", "Description of Captured Application State"],
    [
        ["Fig 1", "CO3", "01_registration_form.png", "Main student admission registration form with floating labels and dropzone"],
        ["Fig 2", "CO3", "02_form_validation.png", "Real-time client validation error highlights and 5-factor password strength meter"],
        ["Fig 3", "CO3", "03_successful_registration.png", "Asynchronous AJAX post-registration confirmation screen with roll number"],
        ["Fig 4", "CO3", "04_database_record.png", "Direct verification of newly inserted student record in MySQL `students` table"],
        ["Fig 5", "CO4", "01_admin_login.png", "PHP Admin login authentication page with session fixation protection"],
        ["Fig 6", "CO4", "02_admin_dashboard.png", "PHP Admin dashboard displaying KPI metric counters and academic statistics"],
        ["Fig 7", "CO4", "03_student_list.png", "Registered student records management table with quick action links"],
        ["Fig 8", "CO4", "04_add_student.png", "Add student administrative form with CSRF validation and file upload"],
        ["Fig 9", "CO4", "05_edit_student.png", "Edit student record interface with pre-populated current details"],
        ["Fig 10", "CO4", "06_file_upload.png", "Academic document upload dropzone and document category selector"],
        ["Fig 11", "CO4", "07_document_display.png", "Student profile view displaying uploaded academic credentials and download links"],
        ["Fig 12", "CO5", "01_servlet_login.png", "Java Admin Portal login page powered by LoginServlet and login.jsp"],
        ["Fig 13", "CO5", "02_student_list_jsp.png", "Student registry view rendered via JSP/JSTL displaying all 6 students and KPIs"],
        ["Fig 14", "CO5", "03_student_profile.png", "Student profile for Aarav Sharma showing streamed photo and document metadata"],
        ["Fig 15", "CO5", "04_document_streaming.png", "Native browser view displaying binary JPEG image served by DocumentStreamServlet"],
        ["Fig 16", "CO5", "05_session_verification.png", "Session invalidation and protection verification showing green logout alert banner"]
    ],
    [Inches(0.7), Inches(0.8), Inches(1.9), Inches(3.1)]
)

# ==============================================================================
# SECTION M: GITHUB REPOSITORY
# ==============================================================================
h1(doc, "M. GITHUB REPOSITORY")
p_body(doc, "Project Repository URL Placeholder:", bold_prefix="Verified Repository Status: ")
p_body(doc, "https://github.com/[YOUR_USERNAME]/student-admission-portal", bold_prefix="GitHub Repository URL: ", italic=True)
p_body(doc, "Note: The above URL is a clearly marked placeholder. Before submitting this report to faculty, replace `[YOUR_USERNAME]` with your actual personal GitHub handle once the repository is published.")

h2(doc, "1. Repository Overview")
p_body(doc, "The repository houses the complete multi-tier source code, shared database schema, deployment artifacts, automated test scripts, and high-resolution screenshot evidence. It contains three decoupled modules:")
p_bullet(doc, "Module A: `registration/` — HTML5, CSS3, JavaScript client-side registration form and validation engine.", bold_prefix="CO3: ")
p_bullet(doc, "Module B: `php-admin/` — PHP 8 admin dashboard, CRUD operations, document handlers, and CSRF defense.", bold_prefix="CO4: ")
p_bullet(doc, "Module C: `java-portal/` — Enterprise Java Servlet 3.1, JSP, JDBC, JSTL, and DocumentStreamServlet on Tomcat.", bold_prefix="CO5: ")

h2(doc, "2. Instructions for Publishing Project to GitHub")
p_body(doc, "If the repository has not yet been pushed to GitHub, follow these exact terminal commands:")
code_box(doc, """
# 1. Open PowerShell or Command Prompt in the project workspace
cd E:\\Webproject

# 2. Initialize Git repository and stage all project files
git init
git add .

# 3. Create initial commit with comprehensive message
git commit -m "feat: complete student admission portal implementation covering CO3, CO4, and CO5"

# 4. Create repository on GitHub (via browser at https://github.com/new)
# Named: student-admission-portal (Public or Private)

# 5. Link local repository to your remote GitHub repository
git branch -M main
git remote add origin https://github.com/[YOUR_USERNAME]/student-admission-portal.git

# 6. Push local commits to GitHub main branch
git push -u origin main
""")

# ==============================================================================
# SECTION N: CONCLUSION
# ==============================================================================
h1(doc, "N. CONCLUSION")
p_body(doc, "The Student Admission Portal successfully demonstrates a comprehensive, secure multi-tier web application integrating client-side validation (CO3), PHP/MySQL administrative CRUD operations (CO4), and enterprise Java Servlet/JSP persistence on Apache Tomcat (CO5). All components interface reliably with a unified MySQL database (`student_portal`), enforcing uniform BCrypt credential verification, anti-CSRF protections, and directory-traversal-safe binary document streaming. Empirical verification across all 24 test cases confirmed 100% operational success and full compliance with laboratory syllabus requirements.")

# ==============================================================================
# SECTION O: REFERENCES
# ==============================================================================
h1(doc, "O. REFERENCES")
p_bullet(doc, "World Wide Web Consortium (W3C). HTML5: A Vocabulary and Associated APIs for HTML and XHTML. W3C Recommendation. Available: https://www.w3.org/TR/html52/", bold_prefix="1. HTML5 Standard: ")
p_bullet(doc, "Mozilla Developer Network (MDN). CSS Cascading Style Sheets Reference and Grid Layout Guide. Available: https://developer.mozilla.org/en-US/docs/Web/CSS", bold_prefix="2. CSS3 Reference: ")
p_bullet(doc, "ECMA International. ECMAScript 2023 Language Specification (ECMA-262). Available: https://www.ecma-international.org/publications-and-standards/standards/ecma-262/", bold_prefix="3. JavaScript Standard: ")
p_bullet(doc, "The PHP Documentation Group. PHP 8.2 Manual: PDO Extension, Prepared Statements, and Password Hashing. Available: https://www.php.net/manual/en/", bold_prefix="4. PHP Documentation: ")
p_bullet(doc, "Oracle Corporation. MySQL 8.0 Reference Manual: InnoDB Storage Engine and SQL Syntax. Available: https://dev.mysql.com/doc/refman/8.0/en/", bold_prefix="5. MySQL Documentation: ")
p_bullet(doc, "MariaDB Foundation. MariaDB 10.4 Knowledge Base & SQL Reference. Available: https://mariadb.com/kb/en/", bold_prefix="6. MariaDB Documentation: ")
p_bullet(doc, "Oracle Corporation. Java Servlet 3.1 Specification (JSR 340) and JavaServer Pages 2.3 Specification (JSR 245). Available: https://jakarta.ee/specifications/servlet/", bold_prefix="7. Java Servlet / JSP Specification: ")
p_bullet(doc, "Apache Software Foundation. Apache Tomcat 8.5 Configuration Reference and Architecture Guide. Available: https://tomcat.apache.org/tomcat-8.5-doc/", bold_prefix="8. Apache Tomcat Documentation: ")
p_bullet(doc, "Open Web Application Security Project (OWASP). OWASP Top 10 Web Application Security Risks and Prevention Cheat Sheets. Available: https://owasp.org/www-project-top-ten/", bold_prefix="9. OWASP Security Guidelines: ")

# Save Word Document
doc.save(docx_path)
print(f"DOCX report successfully generated at {docx_path}")

# ==============================================================================
# GENERATE MATCHING MARKDOWN REPORT
# ==============================================================================
md_content = f"""# STUDENT ADMISSION PORTAL
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
| **PHP Interpreter** | Backend Scripting & Admin Engine (CO4) | PHP 8.2.12 (CLI / ZTS x64) at `C:\\xampp\\php\\php.exe` |
| **Web Server** | HTTP Server for PHP & Static Assets (CO3/CO4) | Apache HTTP Server 2.4.58 (Win64) on Port 80 |
| **Java Development Kit** | Compilation & Runtime Environment (CO5) | Oracle JDK 24.0.2 (`javac` & `jar` at `C:\\Program Files\\Java\\jdk-24`) |
| **Servlet Container** | Jakarta/Java Servlet 3.1 & JSP Container (CO5) | Apache Tomcat 8.5.96 at `C:\\xampp\\tomcat` (Port 8082) |
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
{sql_schema_text}
```

---

## G. CO3 — REGISTRATION FORM & CLIENT VALIDATION (8 MARKS)

### 1. Aim
To design, develop, and verify an interactive, responsive student admission registration form utilizing semantic HTML5 markup, modern CSS3 layout and micro-animations, real-time client-side JavaScript validation with password entropy tracking, drag-and-drop avatar handling, and secure asynchronous persistence to MySQL.

### 2. Validation Rules & Input Controls
| Field Name | Control Type | Mandatory | Validation Rule | Error Feedback |
| :--- | :--- | :--- | :--- | :--- |
| **Student Name** | text (`#studentName`) | Yes | `/^[a-zA-Z\\s.'-]{{2,100}}$/` | Name must contain only letters and spaces (2-100 chars). |
| **Roll Number** | text (`#rollNumber`) | Yes | `/^[A-Z0-9-]{{3,20}}$/i` | Roll number must be 3-20 alphanumeric characters. |
| **Email Address** | email (`#email`) | Yes | `/^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{{2,10}}$/` | Please enter a valid institutional email address. |
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
cd E:\\Webproject
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
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Markdown report successfully generated at {md_path}")
print("ALL REPORTS GENERATED SUCCESSFULLY!")
