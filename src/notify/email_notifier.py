import smtplib
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, EMAIL_TO

def send_email_notification(subject: str, body: str):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("メール通知送信成功")
    except Exception as e:
        print(f"メール送信失敗: {e}")
