from django.http import HttpResponse
from . import mysql as MySQLdb
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import django.db.transaction as transaction
import openai

GPT_API_KEY = 'fk-t_zzbtzG8ofRfyWO1UqAoT2axNNDQdP9QVtT9a3lnBU'

DEFAULT_AVATAR = 'https://imgse.com/i/pidqkX8'


from rest_framework.authtoken.models import Token
from django.utils import timezone

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
            request['session']['username'] = username
            request['session']['id'] = user.id
            request['session']['type'] = user.type
            return reponse
        else:
            return JsonResponse({
                'success': success,
                'code': code,
            })
    else:
        return HttpResponse("Not a POST request")
    

@csrf_exempt  # 仅用于演示，请谨慎使用
def SignUpByPatient(request):
    if (request.method == 'POST'):
        try:
            data = json.loads(request.body)
            username = data.get('username', '')
            password = data.get('password', '')
            print(username, password)
            idcard = data.get('idcard', '')
            db = MySQLdb.MyDatabase()
            success, status = db.SignUpByPatient(name=username, password=password, iscommem=False, idcard=idcard)
            print(success, status)
            return JsonResponse({'success': success, 'code': status})
        except ValueError as e:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    else:
        return HttpResponse("Not a POST request")
    
def showAllDrug(request):
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        ans = db.showAllDrug()
        l = []
        for i in ans:
            print(i)
            jsonObj = {"id": i["id"], "name": i["name"], "price": i["price"], "description": i["Description"], "Storage" : i['Storage']}
            l.append(jsonObj)
        return JsonResponse({'info' : l})
    else:
        return HttpResponse("Not a POST request")



def GetDepartmentList(request):
    # assert request.type == 'patient'
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        info = db.GetDepartmentList()
        list = []
        for i in info:
            list.append(i['name'])
        return JsonResponse({'name': list})
    else:
        return HttpResponse("Not a GET request")

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


def PatientRegistration(request):
    assert request.type == 'patient'
    if (request.method == 'POST'):
        data = json.loads(request.body)
        name = request.session['username']
        id = request.session['id']
        db = MySQLdb.MyDatabase()
        doctorId = db.getIdByUsername(data['name'])
        Payid, success, status = db.PatientRegistration(patientid=id, doctorid=doctorId)
        return JsonResponse({'id' : Payid})
    else:
        return HttpResponse("Not a POST request")
    

def finishPay(request):
    assert request.type == 'patient'
    if request.method == 'POST':
        data = json.loads(request.body)
        Payid = data['id']
        db = MySQLdb.MyDatabase()
        db.finishPay(id=Payid)

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

def showAllinCounter(request):
    assert request.type == 'patient'
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        ans = db.showAllinCounter()
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], "price": i["price"], 'status' : i['ispaid'], 'type' : i['type']}
            l.append(jsonObj)
        return

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
    
def PayAll(request):
    assert request.type == 'patient'
    if request.method == 'POST':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        success, status = db.PayAll(pid=Pid)
        return JsonResponse({'success' : success, 'code' : status})
    else:
        return HttpResponse("Not a POST request")
    
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
    
def getLaboratorySheetids(request):
    assert request.type == 'patient'
    if request.method == 'GET':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        ans = db.showAllLaboratorySheetIds(Pid=Pid)
        return JsonResponse(ans)
    else:
        return HttpResponse("Not a GET request")

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
    
def deletePatient(request):
    assert request.type == 'patient'
    if request.method == 'POST':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        db.SoftDeletePatient(id=Pid)
        return JsonResponse({"success" : True})
    else:
        return HttpResponse("Not a POST request")

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

def hardDeleteDrug(request):
    assert request.type == 'admin'
    if request.method == 'POST':
        name = request.get('name')
        db = MySQLdb.MyDatabase()
        db.HardDeleteDrug(name=name)
        return JsonResponse({'success' : True, 'code' : 0})
    else:
        return HttpResponse("Not a POST request")
    
def getCheckItemsList(request):
    assert request.type == 'doctor'
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        res = db.getCheckItemsList()
        return JsonResponse(res)
    else:
        return HttpResponse("Not a GET request")
    
def getCheckCombineList(request):
    assert request.type == 'doctor'
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        res = db.getCheckCombineList()
        return JsonResponse(res)
    else:
        return HttpResponse("Not a GET request")

def getDiagnosisList(request):
    if request.method == 'GET':
        Pid = request.session['id']
        db = MySQLdb.MyDatabase()
        r = db.getDiagnosisList(Pid=Pid)
        return JsonResponse(r)
    else:
        return HttpResponse('NOT A GET REQUEST')
    

def answer(request):
    import mysql as DB
    d = DB.MyDatabase()
    data = json.loads(request.body)
    content = data['content']
    departmentlist = d.GetDepartmentList()
    sendText = "你好，我是一名病人，我的症状是" + content + "，请问我得了什么病？我应该选择从" + departmentlist + "中的哪个科室就诊？"
    openai.api_key = GPT_API_KEY
    openai.api_base = "https://ai.fakeopen.com/v1"

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


def account(id : str):
    db = MySQLdb.MyDatabase()
    username = db.getNameById(id=id)
    j = {}
    j['avavtar'] = DEFAULT_AVATAR
    j['age'] = 18
    j['gender'] = 0
    j['username'] = username
    return JsonResponse(j)

def conductMedcine(request):
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
    

def queryDrugInfo(request):
    if request.method == 'POST':
        DrugId = request.get('id')
        db = MySQLdb.MyDatabase()
        return JsonResponse(db.queryDrugInfo)
    
def showAllUser(request):
    assert request.method == 'GET'
    db = MySQLdb.MyDatabase()
    print(db.showAllUser())
    return HttpResponse('Success')

