import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import EMAIL_CONFIG

def send_email(subject, content, recipients=EMAIL_CONFIG["recipients"], attachment_path=None):
    remitente = EMAIL_CONFIG["user"]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    subject = f"Notificación {subject} {now_str}"

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(recipients)
    mensaje['Subject'] = subject

    header = "<br><br><img src='https://meta.fullpay.cl/images/logo.png' style='width:200px;'><br><br>"
    mensaje.attach(MIMEText(header + content, 'html'))

    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            mensaje.attach(part)

    try:
        session = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        session.starttls()
        session.login(EMAIL_CONFIG["user"], EMAIL_CONFIG["password"])
        session.sendmail(remitente, recipients, mensaje.as_string())
        session.quit()
        print("Correo enviado correctamente.")
    except Exception as e:
        print("Error enviando correo:", str(e))