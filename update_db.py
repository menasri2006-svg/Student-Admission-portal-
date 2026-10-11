import subprocess

admin_hash = '$2y$10$pqlfs4UhUDhaSV2HirlmiOfB2d3UowuIeayCU77dfJzV48AG4U8qG'
student_hash = '$2y$10$YAkbEInvYwX4WDTGTH3yweMXGsW5ccVBbuQH6G3GZcfc/Z39JAb5W'

sql = f"UPDATE admin_users SET password_hash = '{admin_hash}' WHERE username = 'admin'; UPDATE students SET password_hash = '{student_hash}';"

cmd = [
    r"C:\xampp\mysql\bin\mysql.exe",
    "--user=root",
    "--host=127.0.0.1",
    "--port=3306",
    "--database=student_portal",
    "-e",
    sql
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
