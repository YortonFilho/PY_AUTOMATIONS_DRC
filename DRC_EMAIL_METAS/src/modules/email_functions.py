import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from jinja2 import Environment, FileSystemLoader
from modules.logger import get_logger
from modules.config import SMTP_PORT, ZIMBRA_EMAIL_PASSWORD, ZIMBRA_EMAIL, SMTP_SERVER
import pandas as pd
import os

# Logger configuration
logger = get_logger()

# SMTP server settings
smtp_server = SMTP_SERVER
port = SMTP_PORT
username = ZIMBRA_EMAIL
password = ZIMBRA_EMAIL_PASSWORD

def calculate_ref_month() -> str:
    """
    Calculate date to the reference month
    """
    # Get today date
    today = datetime.date.today()

    # First day of the current month
    first_day_current_month = today.replace(day=1).strftime('%m/%Y')

    return first_day_current_month

def send_email(to_email: str, subject: str, html_body: str, bcc_emails: list) -> None:
    """
    Function to send emails with personalized html.

    :to_email: Adress email to send to
    :subject: the subject of the email
    :html_body: Variables containing the HTML
    :bcc_emails: List of emails, which is initialized as empty if not provided
    """

    # Email configuration
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adding the HTML body of the email
    msg.attach(MIMEText(html_body, 'html'))

    # Connecting to the SMTP server and sending emails
    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(username, password)
            server.sendmail(username, [to_email] + bcc_emails, msg.as_string())
            logger.info(f"Email enviado para {to_email}")

    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        raise e
    
def generate_email_body(affiliate_data: dict) -> str:
    """"
    Function to load the template and pass recipient data variables.

    :affiliate_data: A dictionary containing the recipient's data.
    """
    # Adjusting the path to the HTML model in 'templates'
    try:
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))

        # loading template
        template = env.get_template('email_template_collaborators.html')
    except Exception as e:
        logger.error(f"Erro ao carregar o template: {e}")
        raise e

    date = calculate_ref_month()

    # Create the sales list in HTML format
    sales_html = ""
    count = 0
    commission = 0
    for sales in affiliate_data['VENDAS']:
        count += 1
        commission += float(sales['VALOR_META_FINAL'])
        if sales['CPF_CLIENTE']:
            sales_html += f"""
            <tr>
                <td>{count}</td>
                <td>{sales['DATA']}</td>
                <td>{sales['CPF_CLIENTE']}</td>
                <td>{sales['VALOR']}</td>
                <td>{sales['PLANO']}</td>
            </tr>
            """

    if affiliate_data['VENDEDOR']['LIDER'] == 'S':
        if len(affiliate_data['VENDAS']) > 1:
            sales = int(affiliate_data['VENDEDOR']['VENDAS']) + int(affiliate_data['VENDAS'][1]['VENDAS'])
        else:
            sales = int(affiliate_data['VENDEDOR']['VENDAS'])
    else:
        sales = int(affiliate_data['VENDEDOR']['VENDAS'])

    # Rendering template with variables extracted from database
    html_body = template.render(
        collaborator_name=affiliate_data['VENDEDOR']['NOME_VENDEDOR'],
        ref_month=date,
        sales=sales,
        commission=str(commission).replace('.',','),
        sales_table=sales_html
    )
    
    return html_body

def send_emails_to_users(affiliate_data: pd.DataFrame, bcc_emails: list = []) -> None:
    """
    Function to send emails to multiple recipients.

    :affiliate_data: DataFrame with recipients' data.
    :bcc_emails: List of emails for blind carbon copies.
    """      
    try:
        # Loop to send emails
        for cpf in affiliate_data:
            # Generating the HTML body for the email
            html_body = generate_email_body(affiliate_data[cpf])

            email = affiliate_data[cpf]['VENDEDOR']['EMAIL_VENDEDOR'] #.strip(';')
            
            # Sending the email with the recipient's data
            send_email(to_email=email, bcc_emails=bcc_emails, html_body=html_body, subject='(META) Dr. Central')

    except Exception as e:
        logger.error(f"Erro ao enviar email! {e}")
        raise e