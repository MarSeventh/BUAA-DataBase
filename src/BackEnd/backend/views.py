from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import mysql as MySQLdb
import json
from django.contrib.auth import authenticate, login


from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def LogIn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'code': '0', 'type': user.type})
        else:
            return JsonResponse({'success': False, 'code': '404', 'type': ''})
    else:
        return JsonResponse({'error': 'Not a POST request'})
    
def SignUpByPatient(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        idcard = data.get('idcard', '')
        db = MySQLdb.MyDatabase()
        success, status = db.SignUpByPatient(name=username, password=password, iscommem=False, idcard=idcard)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


@login_required
def GetDepartmentList(request):
    if (request.method == 'POST'):
        db = MySQLdb.MyDatabase()
        info = db.GetDepartmentList()
        list = []
        for i in info:
            list.append(i['name'])
        return JsonResponse({'info': list})
    else:
        return HttpResponse("Not a POST request")

@login_required
def GetInfoListByDepartment(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        department = data['Title']
        db = MySQLdb.MyDatabase()
        info = db.GetInfoListByDepartment(department)
        l = []
        for i in info:
            l.append(i['name'])
        return JsonResponse({'info': list})
    else:
        return HttpResponse("Not a POST request")


@login_required
def PatientRegister(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        name = request.session['username']
        id =
        db = MySQLdb.MyDatabase()
        success, status = db.PatientRegistration(name, department, doctor, date)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")

def showAllNeedtoPay(request):
    if (request.method == 'POST'):
        db = MySQLdb.MyDatabase()
        ans = db.showAllNeedToPay()
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], "price": i["price"]}
            l.append(jsonObj)
        return JsonResponse({'Info': list})
    else:
        return HttpResponse("Not a POST request")


def showAllinCounter(request):
    if (request.method == 'POST'):
        return


def visitCounterById(request):
    return


def visitLabById():
    return


def visitDiagnosis():
    return
