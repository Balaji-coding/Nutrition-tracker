import smtplib
import random
from email.message import EmailMessage

from requests import request

# Generate a 6-digit OTP
def email_verifi(to):
    otp = random.randint(100000, 999999)


# Email configuration
    EMAIL_ADDRESS = "use your email"
    EMAIL_PASSWORD = os.getenv("password")
    TO_EMAIL = to

    # Create email message
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(f"Your OTP is: {otp}.   It is valid for 10 minutes.")
            
    # request.session['otp']="202020"

    # Send the email
    if to:
        try:
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
                otp =int(otp)
            return(otp)
        except Exception as e:
            err ="otp is not sent something error"
            return(err)
