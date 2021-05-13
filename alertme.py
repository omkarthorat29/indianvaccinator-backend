import json
import urllib.request
from datetime import datetime
import time
import playsound
code = [413801, 413802]
today_date = str(datetime.today().strftime("%d-%m-%Y"))

def play():
    playsound.playsound('alert.mp3', True)
    return

def fectch():
    try:
        for curr_code in code:
            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={curr_code}&date={today_date} "
            payload = {}
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            data = response.read()
            apiData = json.loads(data)
            print('status:\t', response.getcode(),'\tTime:\t',str(datetime.now()))
            if apiData['centers']:
                for value in apiData['centers']:
                    centerName = value['name']
                    for session in value['sessions']:
                        if session['available_capacity'] > 0 and session['min_age_limit'] == 18:
                            print("Center name:\t", centerName)
                            print("Address:\t", value['address'])
                            print("capacity:\t", session['available_capacity'])
                            play()
                            return
    except Exception as err:
        print(err)
starttime = time.time()
while True:
    print("--------------------------------------------------------------------------")
    fectch()
    time.sleep(60)