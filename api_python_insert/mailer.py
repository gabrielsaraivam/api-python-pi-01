import os
import smtplib
from email.message import EmailMessage

def mailer(assunto, texto):
    EMAIL_ADRESS = 'overall3011@gmail.com'
    EMAIL_PASSWORD = '#Grupo01'

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = 'overall3011@gmail.com'
    msg['To'] = 'tickets@slack-be2t6i.p.tawk.email' # esse email é o que nós temos que enviar para abrir o chamado, ent n apague
    msg.set_content(texto)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)
