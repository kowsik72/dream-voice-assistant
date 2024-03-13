
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_whom, subject, content):
    sender_mail = "kowsik_s@srmap.edu.in"
    sender_pass = "9959499109@k"
    receiver_mail = to_whom

    try:
        msg = MIMEMultipart()
        msg['From'] = "kowsik_s@srmap.edu.in"
        msg["To"] = "johnwick231122@gmail.com"
        msg["Subject"] = "hi"
        msg.attach(MIMEText(content, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_mail, sender_pass)
            server.sendmail(sender_mail, receiver_mail, msg.as_string())
            print("email sent successfully")
    except Exception as e:
        print(f'Error: {e}')
