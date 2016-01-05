from email.mime.multipart import MIMEMultipart
import smtplib
import constants as c
class QAMailSender: 
    def __init__(self,Subject,To,attachments): #String/list(strings)/list(MIMEs)
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(c.sender_mail, c.sender_mail_pwd)
        self.ms = MIMEMultipart()
        self.ToList=To
        self.ms['Subject'] = Subject
        self.ms['From'] = c.from_mail_header #If we want to change how it appears to the reciever
        self.ms['To'] = ', '.join(To) if list == type(To) else To
        self.ms.add_header('reply-to', c.from_mail)
        for attachment in attachments:
            self.ms.attach(attachment)
    def SendMail(self):
        self.server.sendmail(self.ms['From'],self.ToList,self.ms.as_string())
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.server.quit()
    def __del__(self):
        pass