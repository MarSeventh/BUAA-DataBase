from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from django.utils import timezone

from . import mysql as MySQLdb
import jwt, datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import django.db.transaction as transaction
import openai

import json
from django.http import JsonResponse


@csrf_exempt
def showRequestJson(request):
    received_data = json.loads(request.body)  # 解析请求体中的 JSON 数据
    response_data = {'received_data': received_data, 'status': 'success'}  # 示例数据
    return JsonResponse(response_data)


@csrf_exempt
def LogIn(request):
    if request.method == 'POST':
        print('Login')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        db = MySQLdb.MyDatabase()
        success, code, user = db.Login(username=username, password=password)
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        payload = {
            'username': username,
            'exp': exp,
        }
        token = jwt.encode(payload, 'secret key', algorithm='HS256')

        if user != None:
            request.session['username'] = username
            request.session['id'] = user.id
            request.session['type'] = user.type
            return JsonResponse({'code': 0, 'message': 'success', 'type': user.type,
                                 'data': {'token': token, 'expires': exp.timestamp()}})
        else:
            return JsonResponse({
                'success': success,
                'code': code,
            })
    else:
        return HttpResponse("Not a POST request")
