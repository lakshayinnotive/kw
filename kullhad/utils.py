from django.conf import settings
from django.core.mail import send_mail

def send_email_token(request):
    try:
        subject = "Welcome to kullhadwala, your account needs to be verify"
        message = f"click on link to verify http://127.0.0.1.8000/verify/{token}/"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return False
    return True