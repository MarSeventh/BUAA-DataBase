from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.utils import timezone

from . import mysql as MySQLdb
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


        token, created = Token.objects.get_or_create(user=user)
        token_data = {
            'token': token.key,
            'expires_at': timezone.now() + token.settings.get("TOKEN_TIMEOUT")
        }

        if user != None:
            reponse = JsonResponse({
                'success': success,
                'code': code,
                'type': user.type,
                'token_data': token_data
            })
            request.session['username'] = username
            request.session['id'] = user.id
            request.session['type'] = user.type
            return reponse
        else:
            return JsonResponse({
                'success': success,
                'code': code,
            })
    else:
        return HttpResponse("Not a POST request")
