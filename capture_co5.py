import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

out_dir = r"E:\Webproject\screenshots\CO5_Servlet_JSP"
os.makedirs(out_dir, exist_ok=True)

port = "8082"
base_url = f"http://localhost:{port}/student-portal"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1280,950")
driver = webdriver.Chrome(options=opts)

try:
    print(f"CO5 Step 1: Navigating to Java portal login page at {base_url}/login ...")
    driver.get(f"{base_url}/login")
    time.sleep(2)
    login_shot = os.path.join(out_dir, "01_servlet_login.png")
    driver.save_screenshot(login_shot)
    print(f"Saved 01_servlet_login.png ({os.path.getsize(login_shot)} bytes)")

    print("CO5 Step 2: Logging in as admin to view student list...")
    username_field = driver.find_element(By.ID, "username")
    username_field.clear()
    username_field.send_keys("admin")

    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys("Password@123")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Confirm we are on /students
    print("Current URL after login:", driver.current_url)
    list_shot = os.path.join(out_dir, "02_student_list_jsp.png")
    driver.save_screenshot(list_shot)
    print(f"Saved 02_student_list_jsp.png ({os.path.getsize(list_shot)} bytes)")

    print("CO5 Step 3: Navigating to student profile (Student ID 1 - Aarav Sharma)...")
    driver.get(f"{base_url}/profile?id=1")
    time.sleep(2)
    profile_shot = os.path.join(out_dir, "03_student_profile.png")
    driver.save_screenshot(profile_shot)
    print(f"Saved 03_student_profile.png ({os.path.getsize(profile_shot)} bytes)")

    print("CO5 Step 4: Accessing DocumentStreamServlet for document streaming...")
    # Stream profile image served through DocumentStreamServlet
    driver.get(f"{base_url}/document?profile=doc_aarav_profile_sample.jpg")
    time.sleep(2)
    doc_shot = os.path.join(out_dir, "04_document_streaming.png")
    driver.save_screenshot(doc_shot)
    print(f"Saved 04_document_streaming.png ({os.path.getsize(doc_shot)} bytes)")

    print("CO5 Step 5: Testing session verification (logout & session protection)...")
    # Click logout to trigger LogoutServlet session invalidation and redirect with flash message
    driver.get(f"{base_url}/logout")
    time.sleep(2)
    session_shot = os.path.join(out_dir, "05_session_verification.png")
    driver.save_screenshot(session_shot)
    print(f"Saved 05_session_verification.png ({os.path.getsize(session_shot)} bytes)")

    print("\n--- ALL CO5 SCREENSHOTS CAPTURED SUCCESSFULLY ---")
    for f in sorted(os.listdir(out_dir)):
        p = os.path.join(out_dir, f)
        print(f" - {f}: {os.path.getsize(p)} bytes")

finally:
    driver.quit()
