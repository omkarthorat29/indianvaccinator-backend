import json

from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..configs import config
import requests
import urllib.request
@api_view(["GET"])
def main(request):
    try:
        response = requests.request("GET", config.localUrl + 'firebase/')
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", config.localUrl + 'cowin/', headers=headers, data=json.dumps(response.text))
    except Exception as exc:
        return JsonResponse({"users": str(exc)})
    return JsonResponse({"users": 200})