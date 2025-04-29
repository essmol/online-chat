from celery import shared_task
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
import redis
import random
from django.utils import timezone


redis_client = redis.Redis(
    host='redis',  
    port=6379,
    db=1,  
    decode_responses=True  
)

@shared_task
def send_verification_email(email):
    try:
        verification_code = _generate_verification_code()
        
        redis_client.setex(
            f'verification_code_{email}',
            settings.VERIFICATION_CODE_EXPIRATION_TIME,
            verification_code
        )

        subject = "Email Verification"
        message = f"Your verification code is: {verification_code}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        return {"message": "Verification email sent successfully."}
    
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return {"message": "Error sending verification email", "error": str(e)}


@shared_task
def send_verification_sms(phone_number):
    try:
        verification_code = _generate_verification_code()
        redis_client.setex(
            f'verification_code_{phone_number}',
            settings.VERIFICATION_CODE_EXPIRATION_TIME,
            verification_code
        )

        # Implement your SMS sending logic here
        return {"message": "Verification SMS sent successfully."}
    
    except Exception as e:
        print(f"Error sending verification SMS: {str(e)}")
        return {"message": "Error sending verification SMS", "error": str(e)}


def _generate_verification_code():
    return str(random.randint(100000, 999999))
