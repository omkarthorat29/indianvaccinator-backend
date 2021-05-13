import json
from datetime import datetime
from ..configs import config
import requests
from rest_framework.decorators import api_view
from django.http import JsonResponse
import urllib.request
@api_view(["POST"])
def fetchCenterAndUsers(request):
    try:
        data = json.loads(request.data)
        users = data['users']
        pincodes = data['pincodes']
        mainData = []
        tasks = []
        urls = []
        for code in pincodes:
            today_date = str(datetime.today().strftime("%d-%m-%Y"))
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
                                    'centerName': centerName,
                                    'usersData': list(filter(lambda x: ('pincode' in x and x['pincode']) == code, users))}
                            mainData.append(data)
        headers = {
            'Content-Type': 'application/json'
        }
        requests.request("POST", config.localUrl + 'alerts/', headers=headers, data=json.dumps(mainData))
        return JsonResponse({"data": apiData})
    except Exception as err:
        return JsonResponse({"users": str(err)})
    return JsonResponse({"data": []})