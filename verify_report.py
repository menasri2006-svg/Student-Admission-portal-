import os
import docx

path = r"E:\Webproject\submission\Student_Admission_Portal_Final_Report.docx"
doc = docx.Document(path)

print("File size:", os.path.getsize(path), "bytes")
print("Total paragraphs:", len(doc.paragraphs))
print("Total tables:", len(doc.tables))

drawings = 0
for p in doc.paragraphs:
    for run in p.runs:
        if 'drawing' in run._r.xml:
            drawings += 1
print("Total embedded drawings/images:", drawings)

text = " ".join([p.text for p in doc.paragraphs])
sections = [
    "STUDENT ADMISSION PORTAL",
    "B. ABSTRACT",
    "C. OBJECTIVES",
    "D. SOFTWARE AND HARDWARE REQUIREMENTS",
    "E. SYSTEM ARCHITECTURE AND WORKFLOW",
    "F. DATABASE DESIGN",
    "G. CO3 — REGISTRATION FORM",
    "H. CO4 — PHP AND MYSQL ADMIN CRUD PANEL",
    "I. CO5 — JAVA SERVLET, JSP, AND JDBC PORTAL",
    "J. CODE EXPLANATION",
    "K. TESTING AND VERIFICATION",
    "L. RESULTS AND SCREENSHOTS",
    "M. GITHUB REPOSITORY",
    "N. CONCLUSION",
    "O. REFERENCES"
]

all_found = True
for s in sections:
    found = s in text
    status = "FOUND" if found else "MISSING"
    if not found:
        all_found = False
    print(f"Section '{s}': {status}")

conclusion_text = ""
found_n = False
for p in doc.paragraphs:
    if "N. CONCLUSION" in p.text:
        found_n = True
        continue
    if found_n and p.text.strip():
        conclusion_text = p.text.strip()
        break

print("\n--- CONCLUSION CHECK ---")
print(conclusion_text)
sentences = [s.strip() for s in conclusion_text.split('.') if s.strip()]
print(f"Conclusion sentence count: {len(sentences)} (Criteria: exactly 3-5 lines)")

print("\n--- OVERALL VERIFICATION ---")
if all_found and drawings == 16:
    print("ALL CHECKS PASSED PERFECTLY!")
else:
    print(f"Checks completed with all_found={all_found}, drawings={drawings}")
