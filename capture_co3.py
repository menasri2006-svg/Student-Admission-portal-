import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

out_dir = r"E:\Webproject\screenshots\CO3_Registration"
os.makedirs(out_dir, exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1280,950")
driver = webdriver.Chrome(options=opts)

try:
    print("CO3 Step 1: Loading registration form...")
    driver.get("http://localhost/student-admission-portal/registration/")
    time.sleep(2)
    driver.save_screenshot(os.path.join(out_dir, "01_registration_form.png"))
    print("Saved 01_registration_form.png")

    print("CO3 Step 2: Triggering validation errors...")
    # Fill invalid email and weak password to show field validation errors
    name_el = driver.find_element(By.ID, "studentName")
    name_el.clear()
    name_el.send_keys("A")  # too short
    
    roll_el = driver.find_element(By.ID, "rollNumber")
    roll_el.clear()
    
    email_el = driver.find_element(By.ID, "email")
    email_el.clear()
    email_el.send_keys("invalid-email")
    
    pwd_el = driver.find_element(By.ID, "password")
    pwd_el.clear()
    pwd_el.send_keys("weak")
    
    submit_btn = driver.find_element(By.ID, "submitBtn")
    submit_btn.click()
    time.sleep(1)
    
    driver.save_screenshot(os.path.join(out_dir, "02_form_validation.png"))
    print("Saved 02_form_validation.png")

    print("CO3 Step 3: Submitting valid registration...")
    # Refresh to clear errors and enter valid details
    driver.get("http://localhost/student-admission-portal/registration/")
    time.sleep(1)
    
    driver.find_element(By.ID, "studentName").send_keys("Kabir Mehta")
    driver.find_element(By.ID, "rollNumber").send_keys("CS2026-050")
    driver.find_element(By.ID, "email").send_keys("kabir.mehta@example.com")
    
    course_select = Select(driver.find_element(By.ID, "course"))
    course_select.select_by_value("B.Tech Computer Science")
    
    driver.find_element(By.ID, "password").send_keys("Password@123")
    driver.find_element(By.ID, "confirmPassword").send_keys("Password@123")
    
    # Upload sample picture if available
    sample_img = r"E:\Webproject\php-admin\uploads\profile_images\sample_aarav.jpg"
    if os.path.exists(sample_img):
        driver.find_element(By.ID, "profilePic").send_keys(sample_img)
        time.sleep(0.5)

    driver.find_element(By.ID, "submitBtn").click()
    
    # Wait for success screen
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "successScreen"))
    )
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "03_successful_registration.png"))
    print("Saved 03_successful_registration.png")

    print("CO3 Step 4: Database record view...")
    # Create a nice verification viewer page showing the newly inserted row in MySQL
    # or query MySQL directly and display formatted result
    import subprocess
    cmd = [
        r"C:\xampp\mysql\bin\mysql.exe",
        "--user=root",
        "--host=127.0.0.1",
        "--port=3306",
        "--database=student_portal",
        "--html",
        "-e",
        "SELECT id, roll_number, name, email, course, status, registration_date FROM students WHERE email='kabir.mehta@example.com';"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Database Record Verification - MySQL student_portal</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            h1 {{ color: #38bdf8; font-size: 24px; margin-bottom: 8px; }}
            p {{ color: #94a3b8; font-size: 14px; margin-bottom: 24px; }}
            .badge {{ display: inline-block; background: #059669; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; margin-bottom: 16px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background: #334155; color: #f1f5f9; padding: 12px; text-align: left; font-size: 13px; }}
            td {{ padding: 12px; border-bottom: 1px solid #334155; color: #cbd5e1; font-size: 13px; }}
            tr:hover td {{ background: #283548; }}
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">&#10003; MySQL Verified</span>
            <h1>MySQL Database: `student_portal.students`</h1>
            <p>Query: <code>SELECT id, roll_number, name, email, course, status, registration_date FROM students WHERE email='kabir.mehta@example.com';</code></p>
            {res.stdout}
        </div>
    </body>
    </html>"""
    
    db_verify_path = r"E:\Webproject\db_verify_co3.html"
    with open(db_verify_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    driver.get("file:///" + db_verify_path.replace("\\", "/"))
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "04_database_record.png"))
    print("Saved 04_database_record.png")

    print("CO3 Screenshot collection completed successfully!")

finally:
    driver.quit()
