from home.models import Student
import time
from django.core.mail import send_mail
from django.conf import settings
def send_email_to_client():
    subject="This message is from server"
    message="This is a test message"
    from_email=settings.EMAIL_HOST_USER
    recipients_list=["ksairevanth5974@gmail.com"]
    send_mail(subject,message,from_email,recipients_list)