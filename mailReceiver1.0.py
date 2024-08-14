import imaplib
import pyzmail
import os
import time
import zipfile
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Datos de conexión
EMAIL = 'sender@example.com'
PASSWORD = 'pw'
IMAP_SERVER = 'mail-es.securemail.pro'  # Ej: 'imap.gmail.com' para Gmail
SMTP_SERVER = 'smtp-es.securemail.pro'  # Ej: 'smtp.gmail.com' para Gmail
SMTP_PORT = 465
RECIPIENT_EMAIL = 'recipient@example.com'

def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        return mail
    except Exception as e:
        print(f"Error al conectar al servidor IMAP: {e}")
        raise

def create_date_folder():
    today = datetime.now().strftime("%d-%m-%Y")
    folder_path = os.path.join(os.getcwd(), today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # Si se ha creado una nueva carpeta, enviar los archivos del día anterior
        send_yesterdays_attachments()
        yesterday = datetime.now() - timedelta(1)
        yesterday_str = yesterday.strftime("%d-%m-%Y")
        yesterday_folder_path = os.path.join(os.getcwd(), yesterday_str)
        try:
            os.rmdir(yesterday_folder_path)
        except Exception as e:
            print(f"Error eliminando la carpeta de ayer: {e}")
    return folder_path

def download_attachments(msg, folder_path):
    for part in msg.mailparts:
        if part.filename:
            file_path = os.path.join(folder_path, part.filename)
            with open(file_path, 'wb') as f:
                f.write(part.get_payload())
            print("Fichero descargado con éxito.")

def mark_as_read(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Seen')

def check_for_new_emails(mail, folder_path):
    result, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    for email_id in email_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = pyzmail.PyzMessage.factory(raw_email)

        if msg:
            download_attachments(msg, folder_path)
            mark_as_read(mail, email_id)

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def send_email_with_attachments(zip_path, date_str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f'Tickets {date_str}'

    body = f'Adjunto se encuentran los tickets del día {date_str}.'
    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    with open(zip_path, 'rb') as f:
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_path)}')
    msg.attach(attachment)

    try:
        smtp_server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp_server.login(EMAIL, PASSWORD)
        smtp_server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
        smtp_server.close()
        print(f"Correo enviado con los tickets del día {date_str}.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def send_yesterdays_attachments():
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = yesterday.strftime("%d-%m-%Y")
    yesterday_folder_path = os.path.join(os.getcwd(), yesterday_str)
    if os.path.exists(yesterday_folder_path):
        zip_path = f"{yesterday_folder_path}.zip"
        zip_folder(yesterday_folder_path, zip_path)
        send_email_with_attachments(zip_path, yesterday_str)
        os.remove(zip_path)  # Elimina el archivo ZIP después de enviarlo

def main():
    print("""
███    ███  █████  ██ ██      ██████  ███████  ██████ ███████ ██ ██    ██ ███████ ██████      ██    ██  ██     ██████  
████  ████ ██   ██ ██ ██      ██   ██ ██      ██      ██      ██ ██    ██ ██      ██   ██     ██    ██ ███    ██  ████ 
██ ████ ██ ███████ ██ ██      ██████  █████   ██      █████   ██ ██    ██ █████   ██████      ██    ██  ██    ██ ██ ██ 
██  ██  ██ ██   ██ ██ ██      ██   ██ ██      ██      ██      ██  ██  ██  ██      ██   ██      ██  ██   ██    ████  ██ 
██      ██ ██   ██ ██ ███████ ██   ██ ███████  ██████ ███████ ██   ████   ███████ ██   ██       ████    ██ ██  ██████  
    """)
    while True:
        try:
            mail = connect_to_email()
            folder_path = create_date_folder()
            check_for_new_emails(mail, folder_path)
            mail.logout()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)  # Espera 1 minuto antes de verificar de nuevo

if __name__ == '__main__':
    main()
