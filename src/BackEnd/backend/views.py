from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import mysql as MySQLdb
import json

def LogIn(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        print(username)
        print(password)
        db = MySQLdb.MyDatabase()
        success, status, t = db.login(username, password)
        return JsonResponse({'success': success, 'code' : status, 'type' : t})
    else:
        return HttpResponse("Not a POST request")

def Register(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        idcard = data['idcard']
        db = MySQLdb.MyDatabase()
        success, status = db.patient_register(name=username, password=password, idcard=idcard)
        return JsonResponse({'success': success, 'status' : status})
    else:
        return HttpResponse("Not a POST request")

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

def registByPatient(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        patientid = data['patientid']
        doctorid = data['doctorid']
        db = MySQLdb.MyDatabase()
        success, status = db.registByPatient(patientid, doctorid)
        return JsonResponse({'success': success, 'status' : status})
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
        return JsonResponse({'Info' : list})
    else:
        return HttpResponse("Not a POST request")

def showAllinCounter(request):
    if (request.method == 'POST'):
        return

def visitCounterById():
    return

def visitLabById():
    return

def visitDiagnosis():
    return

