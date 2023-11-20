from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import mysql as MySQLdb
import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import django.db.transaction as transaction

@csrf_exempt
def LogIn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        request.session['id'] = data.get('id', '')

        user = authenticate(request, username=username, password=password)

        request.session['type'] = user.type
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
    assert request.type == 'patient'
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        info = db.GetDepartmentList()
        list = []
        for i in info:
            list.append(i['name'])
        return JsonResponse({'name': list})
    else:
        return HttpResponse("Not a GET request")

@login_required
def GetInfoListByDepartment(request):
    assert request.type == 'patient'
    if (request.method == 'POST'):
        data = json.loads(request.body)
        department = data['Title']
        db = MySQLdb.MyDatabase()
        info = db.GetInfoListByDepartment(department)
        l = []
        for i in info:
            l.append({i['name'], i['RoomID'], i['QueueLen']})
        return JsonResponse({'info': list})
    else:
        return HttpResponse("Not a POST request")


@login_required
def PatientRegistration(request):
    assert request.type == 'patient'
    if (request.method == 'POST'):
        data = json.loads(request.body)
        name = request.session['username']
        id = request.session['id']
        db = MySQLdb.MyDatabase()
        doctorId = db.getIdByUsername(data['doctor'])
        success, status = db.PatientRegistration(patientid=id, doctorid=doctorId)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")

@login_required
def showAllNeedtoPay(request):
    assert request.type == 'patient'
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

@login_required
def showAllinCounter(request):
    assert request.type == 'patient'
    if (request.method == 'POST'):
        db = MySQLdb.MyDatabase()
        ans = db.showAllinCounter()
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], "price": i["price"]}
            l.append(jsonObj)
        return

@login_required
@transaction.atomic
def PrescribeMedication(request):
    assert request.type == 'doctor'
    if request.method == 'POST':
        Did = request.session['id']
        Pid = request.POST.get('Pid')
        MedcineList = request.POST.get('MedcineList')
        AmountList = request.POST.get('AmountList')
        db = MySQLdb.MyDatabase()
        success, status = db.PrescribeMedication(did=Did, pid=Pid, nameList=MedcineList, amount=AmountList)
        return JsonResponse({'success' : success, 'code' : status})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def PayAll(request):
    assert request.type == 'patient'
    if request.method == 'POST':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        success, status = db.PayAll(pid=Pid)
        return JsonResponse({'success' : success, 'code' : status})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def showAllDrug(request):
    assert request.type == 'admin'
    if request.method == 'POST':
        db = MySQLdb.MyDatabase()
        ans = db.showAllDrug()
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], "name": i["name"], "price": i["price"], "description": i["description"], "Storage" : i['Storage']}
            l.append(jsonObj)
        return JsonResponse({'Info': list})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def showAllDrugName(request):
    assert request.type == 'doctor'
    if request.method == 'POST':
        db = MySQLdb.MyDatabase()
        ans = db.showAllDrugName()
        l = []
        for i in ans:
            jsonObj = {"name": i["name"]}
            l.append(jsonObj)
        return JsonResponse({'Info': list})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def MedicalDiagnosisStatement(request):
    assert request.type == 'doctor'
    if request.method == 'POST':
        Did = request.session['id']
        Pid = request.POST.get('Pid')
        Statement = request.POST.get('Statement')
        db = MySQLdb.MyDatabase()
        success, status = db.MedicalDiagnosisStatement(did=Did, pid=Pid, statement=Statement)
        return JsonResponse({'success' : success, 'code' : status})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def getDiagnosisByPid(request):
    assert request.type == 'patient'
    if request.method == 'GET':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        ans = db.getDiagnosisByPid(pid=Pid)
        l = []
        for i in ans:
            jsonObj = {"time": i["time"], "statement": i["statement"]}
            l.append(jsonObj)
        return JsonResponse({'Info': list})
    else:
        return HttpResponse("Not a GET request")
    
@login_required
def getLaboratorySheetids(request):
    assert request.type == 'patient'
    if request.method == 'GET':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        ans = db.showAllLaboratorySheetIds(Pid=Pid)
        return JsonResponse({'Info': ans})
    else:
        return HttpResponse("Not a GET request")

@login_required
def getLaboratorySheet(request):
    assert request.type == 'patient'
    if request.method == 'GET':
        Pid = request.session['id']
        Sheetid = request.POST.get('Sheetid')
        db = MySQLdb.MyDatabase()
        ans = db.getLaboratorySheet(id=Sheetid)
        return JsonResponse({'Info': ans})
    else:
        return HttpResponse("Not a GET request")
    
@login_required
def conductLaboratorySheet(request):
    assert request.type == 'doctor'
    if request.method == 'POST':
        Did = request.session['id']
        Pid = request.POST.get('Pid')
        checkName = request.POST.get('checkName')
        checkItemIds = request.POST.get('checkItemIds')
        db = MySQLdb.MyDatabase()
        success, status = db.conductAlaboratoryAnalysis(checkName=checkName, checkItemIds=checkItemIds, did=Did, pid=Pid)
        return JsonResponse({'success' : success, 'code' : status})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def deletePatient(request):
    assert request.type == 'patient'
    if request.method == 'POST':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        db.SoftDeletePatient(id=Pid)
        return JsonResponse({"success" : True})
    else:
        return HttpResponse("Not a POST request")

@login_required
def checkThePosInQueueu(request):
    assert request.type == 'patient'
    if request.method == 'GET':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        success, ans, id = db.getRegisterRelationInfo(Pid=Pid)
        if success:
            return JsonResponse({'success' : success, 'queueNum' : ans, 'code' : 0, 'id' : id, 'msg' : format("您前面还有%d,您的号码为%d" % ans % id)})
        else:
            return JsonResponse({'success' : False, 'queueNum' : -1, 'code' : 404, 'id' : -1 ,"msg" : '尚未挂号'})
    else:
        return HttpResponse("Not a GET request")
@login_required
def showCounterById(request) :
    assert request.type == 'patient'
    if request.method == 'POST':
        id = request.get('id')
        db = MySQLdb.MyDatabase()
        res = db.showCounterById(id=id)
        if res:
            return JsonResponse({'code' : 404, 'msg' : '没有该id的订单'})
        else :
            return JsonResponse(res)
    else:
        return HttpResponse("Not a POST request")

@login_required
def getDoctorDispatch(request):
    assert request.type == 'doctor'
    if request.method == 'GET':
        Did = request.session['id']
        db = MySQLdb.MyDatabase()
        res = db.getDoctorDispatcher(Did=Did)
        if len(res) != 0:
            return JsonResponse(res)
        else:
            return JsonResponse({'code' : 404, 'msg' : '没有该医生的挂号信息'})
    else:
        return HttpResponse("Not a GET request")

@login_required
def hardDeleteDrug(request):
    assert request.type == 'admin'
    if request.method == 'POST':
        name = request.get('name')
        db = MySQLdb.MyDatabase()
        db.HardDeleteDrug(name=name)
        return JsonResponse({'success' : True, 'code' : 0})
    else:
        return HttpResponse("Not a POST request")
    
@login_required
def getCheckItemsList(request):
    assert request.type == 'doctor'
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        res = db.getCheckItemsList()
        return JsonResponse(res)
    else:
        return HttpResponse("Not a GET request")
    
@login_required
def getCheckCombineList(request):
    assert request.type == 'doctor'
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        res = db.getCheckCombineList()
        return JsonResponse(res)
    else:
        return HttpResponse("Not a GET request")
