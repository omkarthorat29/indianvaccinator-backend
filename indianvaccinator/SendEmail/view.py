import json
import yagmail
from datetime import datetime
from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..configs import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
@api_view(["POST"])
def sendEmail(request):
    data = request.data
    yag = yagmail.SMTP(config.sender_address, config.sender_pass)
    for sendData in data:
        emailStr = sendData['msg']
        email = sendData['email']
        try:
            contents = emailStr + '\nvisit https://indianvaccinator.com/ to unsubscribe'
            subject = 'Alert vaccination slots are available book fast'
            yag.send(email, subject , contents)
            print('Mail Sent')
        except Exception as err:
            print(err)
    return JsonResponse({})
