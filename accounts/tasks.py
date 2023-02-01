from celery import shared_task
from django.contrib.auth.tokens import default_token_generator
import smtplib
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.conf import settings
from email.mime.text import MIMEText
from django.core.mail import send_mail

# url = settings.BASE_URL
url="http://localhost:8000/"

@shared_task(bind=True,max_retries=10)
def send_registration_email(self,user):
    body = """
        <p> 
            Hello from MMYVENTRUES <br><br>

            Confirmation Mail: %s

            You can see more details in this link: %saccounts/activate/%s/%s<br><br>

            Thank You for shopping with us.

            Have a nice shopping experience
        </p>
    
    """%(user.name,url,urlsafe_base64_encode(force_bytes(user.pk)),default_token_generator.make_token(user))
    subject = 'Registration Mail'
    recipients = [user.email]

    try:
        send_email(subject,body,settings.EMAIL_HOST_USER,recipients,'html')
        return f"{body} email is sent"
    except Exception as e:
        print("Email not sent",e)
        raise self.retry(exc=e,countdown=25200)

def send_email(subject,body,recipients,body_type="plain"):
    session = smtplib.SMTP("smtp.gmail.com",getattr(settings,"EMAIL_PORT",None))
    session.starttls()
    session.login(
        getattr(settings,"EMAIL_HOST_USER",None),
        getattr(settings,"EMAIL_HOST_PASSWORD",None)
        
    )
    sender='Alldjangohub@gmail.com'

    msg = MIMEText(body,body_type)
    msg['subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    session.sendmail(sender,recipients,msg.as_string())



