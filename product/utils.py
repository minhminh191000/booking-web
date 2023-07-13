from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['email-subject'],
            body=data['body'],
            from_email='cautit2205@gmail.com',#os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()
