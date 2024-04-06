import time
import openai
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import mysql as MySQLdb
import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import django.db.transaction as transaction
GPT_API_KEY = 'your-api-key'

def answer(request):
    import mysql as DB
    d = DB.MyDatabase()
    data = json.loads(request.body)
    content = data['content']
    departmentlist = d.GetDepartmentList()
    sendText = "你好，我是一名病人，我的症状是" + content + "，请问我得了什么病？我应该选择从" + departmentlist + "中的哪个科室就诊？"
    openai.api_key = GPT_API_KEY
    openai.api_base = "https://api.openai.com/v1"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': sendText}
        ],
        temperature=0.5,
        max_tokens=20,
        stream=True
    )

    result = ""

    for chunk in response:
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            result += chunk_msg  # 将输出内容附加到结果字符串上
            #print(chunk_msg, end='', flush=True)
            #time.sleep(0.05)

    return JsonResponse(result)
