import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Ler as credenciais do arquivo JSON
with open("config/config_email.json", "r") as config_file:
    config_data = json.load(config_file)

smtp_server = "smtp.gmail.com"
smtp_port = 587

# Configurações do e-mail
sender_email = config_data["email"]
smtp_password = config_data["senha"]
recipient_email = "destinatario@email.com"
subject = "Automação "
body = "Logs"

# Configurar a mensagem de e-mail
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = "micneaz@gmail.com"
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Conectar ao servidor SMTP e enviar e-mail
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Iniciar conexão TLS (criptografada)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, recipient_email, message.as_string())

print("E-mail enviado com sucesso!")
