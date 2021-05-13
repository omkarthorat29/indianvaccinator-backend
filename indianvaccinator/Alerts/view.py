import json
from datetime import datetime
from ..configs import config
import requests
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(["POST"])
def sendAlerts(request):
    centerData = request.data
    msgString = ''
    listofstr = []
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        ages = ['18']
        for data in centerData:
            for user in data['usersData']:
                if 'ageGroups' in user:
                    if user['ageGroups']:
                        ages = user['ageGroups']
                if str(data['ageLimit']) in ages:
                    msg_str = get_email_string(user, data)
                    listofstr.append({ 'msg': msg_str, 'email': user['email'] })
        requests.request("POST", config.localUrl + 'sendEmail/', headers=headers,
                         data=json.dumps(listofstr))
        return JsonResponse({'centers': listofstr})
    except Exception as err:
        print(err)


def get_email_string(user, selectedCenterDetail):
    try:
        msgString = ''
        if user['displayName']:
            msgString = f"ALERT Hello, {user['displayName']} vaccination slots are available book fast!\n"
        msgString += f"Center: {selectedCenterDetail['centerName']} Date: {selectedCenterDetail['date']}\n"
        msgString += f"Capacity: {selectedCenterDetail['capacity']}\n"
        msgString += f"Age: {selectedCenterDetail['ageLimit']}\n"
        msgString += f"Vaccine: {selectedCenterDetail['vaccine']}\n"
        msgString += f"Slots: {selectedCenterDetail['slots']}\n"
        msgString += 'The future depends on what you do today. - Mahatma Gandhi'
        msgString += '\n\n\nDeveloped by Omkar Thorat & Ashwini More'
        return msgString
    except Exception as err:
        print(err)