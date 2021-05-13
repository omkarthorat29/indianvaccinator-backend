import firebase_admin
from firebase_admin import credentials, firestore
from rest_framework.decorators import api_view
from django.http import JsonResponse
path = "docs/authkey.json"
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)


@api_view(["GET"])
def getUsersAndUniquePinocdes(request):
    listdict = []
    set_list = []
    try:
        db = firestore.client()
        users_ref = db.collection(u'users')
        docs = users_ref.where(u'wantAlert', u'==', True).stream()
        for val in docs:
            listdict.append(val.to_dict())
        for value in listdict:
            if "pincode" in value and value['pincode']:
                zip = value['pincode']
                set_list.append(zip)
    except Exception as err:
        print(err)
    return JsonResponse({'users': listdict, 'pincodes': list(set(set_list)) })
