import smtplib

EMAIL = "harishravikuamr74@gmail.com"
PASSWORD = "aajdhbqabdpirlto"

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASSWORD)
    print("✅ LOGIN SUCCESS")
except Exception as e:
    print("❌ ERROR:", e)