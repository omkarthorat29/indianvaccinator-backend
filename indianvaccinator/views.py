import json
import os
from datetime import datetime
import smtplib
from rest_framework.response import Response
from rest_framework.decorators import api_view
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sender_address = 'indianvaccinator@gmail.com'
sender_pass = 'omkar@1998@omkar'
path = "docs/authkey.json"
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)


@api_view(["GET"])
def send_alert(request):
    db = firestore.client()
    users_ref = db.collection(u'users')
    docs = users_ref.where(u'wantAlert', u'==', True).stream()
    listdict = []
    for val in docs:
        listdict.append(val.to_dict())
    set_list = []
    try:
        for value in listdict:
            zip = value['pincode']
            set_list.append(zip)
            # print(postal_codes)
    except Exception as e:
        pass
        print(e)
    postal_codes = list(set(set_list))
    today_date = str(datetime.today().strftime("%d-%m-%Y"))
    mainStringList = []
    data = {}
    for code in postal_codes:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={code}&date={today_date} "
        payload = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        apiData = json.loads(data)
        if apiData['centers']:
            for value in apiData['centers']:
                centerName = value['name']
                for session in value['sessions']:
                    if session['available_capacity'] > 0:
                        data = {'date': session['date'], 'pincode': code, 'address': value['address'],
                                'capacity': session['available_capacity'], 'vaccine': session['vaccine'],
                                'ageLimit': session['min_age_limit'], 'slots': session['slots'],
                                'centerName': centerName}
                        mainStringList.append(data)
    for newData in mainStringList:
        users = []
        for user in listdict:
            if user['pincode'] == newData['pincode']:
                users.append({
                    'email': user['email'],
                    'phone': user['phoneNumber'],
                    'name': user['displayName']
                })
        newData['userDetails'] = users

    for newData in mainStringList:
        for user in newData['userDetails']:
            send_email(user, newData)
            send_sms(user, newData)

    return Response({"message": 'inside alert sender'})

def send_email(user, selectedCenterDetail):
    msgString = get_sms_string(user, selectedCenterDetail, True)
    try:
        if user['email']:
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = user['email']
            message['Subject'] = 'Alert vaccination slots are available book fast'  # The subject line
            # The body and the attachments for the mail
            message.attach(MIMEText(msgString, 'plain'))
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, user['email'], text)
            session.quit()
            print('Mail Sent')
    except Exception as err:
        print(err)



def send_sms(user, selectedCenterDetail):
    msgString = get_sms_string(user, selectedCenterDetail,False)
    try:
        if user['phone']:
            sms_url = "https://www.fast2sms.com/dev/bulkV2"
            payload = json.dumps({
                "route": "v3",
                "sender_id": "TXTIND",
                "message": msgString,
                "language": "english",
                "flash": 0,
                "numbers": str(user['phone'])
            })
            headers = {
                'Authorization': 'HM4CWPc7rhZSYOQ5vL36Jtiy1uzBlgbK9kVwGmxpqIDo0ej2Fn13HvOIJjUK92QaDiz5CeERgA7Vlfp6',
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", sms_url, headers=headers, data=payload)
            print(response.text)
    except Exception as e:
        print(e)


def get_sms_string(user, selectedCenterDetail,sms):
    try:
        msgString = ''
        if user['name']:
            msgString = f"ALERT Hello, {user['name']} vaccination slots are available book fast!\n"
        msgString += f"Center: {selectedCenterDetail['centerName']} Date: {selectedCenterDetail['date']}\n"
        msgString += f"Capacity: {selectedCenterDetail['capacity']}\n"
        msgString += f"Age: {selectedCenterDetail['ageLimit']}\n"
        if sms == True:
            msgString += f"Vaccine: {selectedCenterDetail['vaccine']}\n"
            msgString += f"Slots: {selectedCenterDetail['slots']}\n"
        msgString += 'The future depends on what you do today. - Mahatma Gandhi'
        if sms == True:
            msgString += '\n\n\nDeveloped by Omkar Thorat & Ashwini More'
        return msgString
    except Exception as err:
        print(err)
