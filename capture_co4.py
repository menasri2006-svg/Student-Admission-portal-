import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

out_dir = r"E:\Webproject\screenshots\CO4_PHP_CRUD"
os.makedirs(out_dir, exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1280,950")
driver = webdriver.Chrome(options=opts)

try:
    print("CO4 Step 1: Admin login page...")
    driver.get("http://localhost/student-admission-portal/php-admin/login.php")
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(out_dir, "01_admin_login.png"))
    print("Saved 01_admin_login.png")

    print("CO4 Step 2: Logging in as admin...")
    user_el = driver.find_element(By.NAME, "username")
    user_el.clear()
    user_el.send_keys("admin")
    
    pwd_el = driver.find_element(By.NAME, "password")
    pwd_el.clear()
    pwd_el.send_keys("Password@123")
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    
    driver.save_screenshot(os.path.join(out_dir, "02_admin_dashboard.png"))
    print("Saved 02_admin_dashboard.png")

    print("CO4 Step 3: Student list table...")
    # Scroll slightly to show full student table
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "03_student_list.png"))
    print("Saved 03_student_list.png")

    print("CO4 Step 4: Add student page...")
    driver.get("http://localhost/student-admission-portal/php-admin/add_student.php")
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(out_dir, "04_add_student.png"))
    print("Saved 04_add_student.png")

    print("CO4 Step 5: Edit student page...")
    # Pick student ID 1 (Aarav Sharma)
    driver.get("http://localhost/student-admission-portal/php-admin/edit_student.php?id=1")
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(out_dir, "05_edit_student.png"))
    print("Saved 05_edit_student.png")

    print("CO4 Step 6: File upload interface...")
    # Student view page contains document upload section
    driver.get("http://localhost/student-admission-portal/php-admin/view_student.php?id=1")
    time.sleep(1.5)
    # Scroll to document upload section
    driver.execute_script("window.scrollTo(0, 450);")
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "06_file_upload.png"))
    print("Saved 06_file_upload.png")

    print("CO4 Step 7: Document display view...")
    # View student top with documents & profile picture
    driver.get("http://localhost/student-admission-portal/php-admin/view_student.php?id=1")
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(out_dir, "07_document_display.png"))
    print("Saved 07_document_display.png")

    print("CO4 Screenshots captured successfully!")

finally:
    driver.quit()
