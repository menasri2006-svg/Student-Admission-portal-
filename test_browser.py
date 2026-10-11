from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1280,900")
driver = webdriver.Chrome(options=opts)
driver.get("http://localhost/student-admission-portal/registration/")
print("Page Title:", driver.title)
driver.quit()
