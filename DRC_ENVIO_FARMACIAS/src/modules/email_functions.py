from modules.config import SMTP_PORT, ZIMBRA_PASSWORD, ZIMBRA_EMAIL, SMTP_SERVER
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from modules.logger import get_logger
import smtplib
import os

# Logger configuration
logger = get_logger()

# SMTP server configuration
smtp_server = SMTP_SERVER
smtp_port = SMTP_PORT
username = ZIMBRA_EMAIL
password = ZIMBRA_PASSWORD

def send_email(
        to_email: str, 
        subject: str, 
        body: str, 
        bcc_emails: list = None,
        attachment_path: str = None
        ) -> None:
    """
    Function to send an email with an attachment

    :param to_email: Email adress to send the data to
    :param subject: Email subject
    :param body: Email body in HTML
    :param attachment_path: Path to the file to attach
    :param bcc_emails: List of email addresses for blind carbon copies (BCC).
    """
    # email configuration variables 
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Email body in HTML
    html_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: sans-serif;
                    font-size: 12px;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                }}
                .indent {{
                    margin-left: 20px;
                }}
            </style>
        </head>
        <body>
            <p>{body.splitlines()[0]}</p>
            <p class="indent">{body.splitlines()[1]}</p>
            <p>{body.splitlines()[2]}</p>
            <p>{body.splitlines()[3]}</p>
            <p>{body.splitlines()[4]}</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    # If the path exists, add attachment 
    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            base_name = os.path.basename(attachment_path)
        
            part = MIMEApplication(attachment.read(), Name=base_name)
            part['Content-Disposition'] = f'attachment; filename="{base_name}"'
            msg.attach(part)

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(username, [to_email] + bcc_emails, msg.as_string())
            logger.info(
                f'Email enviado para {to_email} com '
                f'cópias ocultas para {', '.join(bcc_emails)}'
                )
    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")

def no_new_subscribers() -> None:
    """
    Function to send an email warning that there are no new subscribers
    """
    try:
        # Adjust variables for sending the email
        to_email = "yorton.filho@centraldeconsultas.med.br"
        subject = "Convênio Dr Central - 19013906000179"
        body = """Olá pessoal, bom dia!
        Hoje não tivemos novos assinantes!
        Dúvidas, à disposição.
        Abs.
        Email enviado pelo @Robô_PY do time de dados do Dr. Central!"""
        bcc_emails = bcc_emails = [ 
            "yorton.filho@centraldeconsultas.med.br",
            "yorton.filho@centraldeconsultas.med.br",
            "yorton.filho@centraldeconsultas.med.br"
        ]
        
        # Sending email
        send_email(to_email, subject, body, bcc_emails)

        logger.info(f"Email de que não tivemos novos assinantes enviado para {to_email} com sucesso!")
        return
    
    except Exception as e:
        logger.error(f"Erro ao enviar email de que não tivemos novos assinantes para: {to_email}")
        raise e

def new_subscribers(output_file: str) -> None:
    """
    Function to an send email with new subscribers

    :param output_file: Path of the file
    """
    try:
        # Adjust variables for sending the email
        to_email = "yorton.filho@centraldeconsultas.med.br"
        subject = "Convênio Dr Central - 19013906000179"
        body = """Olá pessoal, bom dia!
        Segue em anexo a base de novos assinantes para o cadastro na plataforma de vocês.
        Dúvidas, à disposição.
        Abs.
        Email enviado pelo @Robô_PY do time de dados do Dr. Central!"""
        attachment_path = output_file
        bcc_emails = [ 
           "yorton.filho@centraldeconsultas.med.br",
            "yorton.filho@centraldeconsultas.med.br",
            "yorton.filho@centraldeconsultas.med.br"
            ]
        # send email
        send_email(to_email, subject, body, bcc_emails, attachment_path)
        logger.info(f"Email com a base de novos assinantes enviado para {to_email} com sucesso!")
        return
    
    except Exception as e:
        logger.error(f"Erro ao enviar base de novos assinantes para o email: {to_email}")
        raise e