"""Manage the Notifications"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flight_data import FlightData

SMTP_SERVER = "smtp.gmail.com"
FROM_EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')
TEMPLATE_HTML = "template.html"


class NotificationManager:
    """Talks with smtp to send e-mail"""

    def __init__(self):
        self.client = smtplib.SMTP(SMTP_SERVER)
        self.client.starttls()

    def structure_msg(self, flight_data: FlightData, email: str):
        with open('template.html', mode='r', encoding='utf-8') as file:
            template = file.read()
            msg = template.replace('[city]', flight_data.destination_city)
            msg = msg.replace('[escalas]', str(flight_data.stop_overs))
            msg = msg.replace('[price]', str(flight_data.price))
            html_body = msg.replace('[url]', flight_data.url)
            text_body = f"Encontramos uma passagem barata para {flight_data.destination_city}\ncom {flight_data.stop_overs} escalas, por apenas R$ {flight_data.price}"
            return self.send_emails(html_body, text_body, email)

    def send_emails(self, html_body, text_body, email):
        message = MIMEMultipart('alternative')
        message['subject'] = 'Passagens Baratas'
        message['To'] = email
        message['From'] = FROM_EMAIL

        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        message.attach(part1)
        message.attach(part2)

        self.client.login(FROM_EMAIL, PASSWORD)
        self.client.sendmail(FROM_EMAIL, email, message.as_string())
