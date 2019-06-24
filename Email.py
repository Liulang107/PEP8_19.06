import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"


class Email:
    def __init__(self, login, password, subject, recipients, message, header):
        self.login = login
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message
        if header is not True:
            header = 'ALL'
        self.header = header

    def send_message(self):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))
        ms = smtplib.SMTP(GMAIL_SMTP, 587)

        # identify ourselves to smtp gmail client
        ms.ehlo()

        # secure our email with tls encryption
        ms.starttls()

        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()

    def receive_message(self):
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = f'(HEADER Subject "{self.header}")'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        print(email_message)
        mail.logout()


if __name__ == '__main__':
    my_email = Email(
        login='login@gmail.com',
        password='qwerty',
        subject='Subject',
        recipients=['vasya@email.com',
                    'petya@email.com'],
        message='Message',
        header=None
    )
    my_email.send_message()
    my_email.receive_message()
