from django.http import HttpResponse
from . import mysql as MySQLdb
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import django.db.transaction as transaction
import openai
import jwt, datetime

GPT_API_KEY = 'sess-G4RoUh550yS8FokrxF7hTY38u1pJNIX0WFBVM0G6'

DEFAULT_AVATAR = 'https://cdn.jsdelivr.net/gh/MarSeventh/imgbed/posts/202312091100889.png'

from rest_framework.authtoken.models import Token
from django.utils import timezone


@csrf_exempt
def LogIn(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        db = MySQLdb.MyDatabase()
        success, code, user = db.Login(username=username, password=password)

        if user != None:
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            timestamp_seconds = int(exp.timestamp())
            timestamp_milliseconds = timestamp_seconds * 1000
            payload = {
                'username': username,
                'role': user.type,
                'exp': timestamp_milliseconds,
            }
            token = jwt.encode(payload, 'secret key', algorithm='HS256')
            request.session['username'] = username
            request.session['id'] = user.id
            request.session['type'] = user.type
            request.session.save()
            print(request.session['username'], request.session['id'], request.session['type'])
            return JsonResponse({'code': 0, 'message': 'success', 'type': user.type,
                                 'data': {'token': token, 'expires': timestamp_milliseconds}})
        else:
            return JsonResponse({
                'success': success,
                'code': code,
            })
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
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
            return JsonResponse({'code': status})
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
            jsonObj = {"id": i["id"], "name": i["name"], "price": i["price"], "description": i["description"],
                       "Storage": i['Storage']}
            l.append(jsonObj)
        return JsonResponse({'info': l})
    else:
        return HttpResponse("Not a POST request")


def GetDepartmentList(request):
    # assert request.type == 'patient'
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        info = db.GetDepartmentList()
        return JsonResponse({'name': info})
    else:
        return HttpResponse("Not a GET request")


@csrf_exempt
def GetInfoListByDepartment(request):
    # assert request.type == 'patient'
    if (request.method == 'POST'):
        department = request.POST.get('departmentName', None)
        db = MySQLdb.MyDatabase()
        info = db.GetInfoListByDepartment(department)
        l = []
        for i in info:
            l.append({'name': i['doctor'], 'jobtitle': i['jobtitle'], 'room': i['room'], 'queuelen': i['queueLen']})
        L = list(l)
        print(L)
        return JsonResponse({'doctorList': L})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def GetDoctorListByDepartment(request):
    # assert request.type == 'patient'
    if (request.method == 'POST'):
        data = json.loads(request.body)
        department = data['department']
        print(department)
        db = MySQLdb.MyDatabase()
        info = db.GetInfoListByDepartment(department)
        l = []
        print(info)
        if len(info) == 0:
            return HttpResponse('no doctor')
        for i in info:
            l.append({'name': i['doctor'], 'roomid': i['room'], 'jobtitle': i['jobtitle'], 'queuelen': i['queueLen']})
        print(l)
        return JsonResponse({'doctorList': l})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def PatientRegistration(request):
    # assert request.type == 'patient'
    if (request.method == 'POST'):
        data = json.loads(request.body)
        print(request.body)
        name = data['userName']
        db = MySQLdb.MyDatabase()
        id = db.getIdByUsername(name=name)
        doctorId = db.getIdByUsername(data['name'])
        Payid, success, status = db.PatientRegistration(patientid=id, doctorid=doctorId)
        return JsonResponse({'id': Payid})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def testPatientRegistration(request):
    assert request.method == 'POST'
    data = json.loads(request.body)
    Pid = data['Pid']
    Did = data['Did']
    db = MySQLdb.MyDatabase()
    PayId, success, status = db.PatientRegistration(patientid=Pid, doctorid=Did)
    return JsonResponse({'id': PayId})


@csrf_exempt
def finishPay(request):
    # assert request.type == 'patient'
    if request.method == 'POST':
        data = json.loads(request.body)
        Payid = data['id']
        db = MySQLdb.MyDatabase()
        if Payid != '-1':
            r = db.finishPay(id=Payid)
            if r:
                return HttpResponse('Success')
            else:
                return HttpResponse('Failed')
        else:
            print('PayAll')
            return PayAll(request=request)


def showAllNeedtoPay(request):
    # assert request.type == 'patient'
    if (request.method == 'GET'):
        data = json.loads(request.body)
        db = MySQLdb.MyDatabase()
        Pid = data['Pid']
        # Pid = '6'
        ans = db.showAllNeedToPay(Pid=Pid)
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], "price": i["price"]}
            l.append(jsonObj)
        return JsonResponse({'Info': l})
    else:
        return HttpResponse("Not a POST request")


def showAllinCounter(request):
    # assert request.type == 'patient'
    if (request.method == 'GET'):
        db = MySQLdb.MyDatabase()
        username = request.GET.get('username', None)
        Pid = db.getIdByUsername(name=username)
        # Pid = '6'
        ans = db.showAllinCounter(Pid=Pid)
        l = []
        for i in ans:
            jsonObj = {"id": i["id"], 'status': i['ispaid'], 'type': i['type'], 'price': i['price']}
            l.append(jsonObj)
        return JsonResponse({'Info': l})


@transaction.atomic
@csrf_exempt
def PrescribeMedication(request):
    # assert request.type == 'doctor'
    if request.method == 'POST':
        # Did = request.session['id']
        data = json.loads(request.body)
        db = MySQLdb.MyDatabase()
        username = data['username']
        print(data)
        Did = db.getIdByUsername(name=username)
        # Did = '5'
        Pid = data['Pid']
        print(Pid)
        MedcineList = data['MedicineList']
        AmountList = data['AmountList']
        if MedcineList == None or AmountList == None:
            print('NOT LIST')
            return HttpResponse("NOT LIST")
        else:
            print('LIST')
            success, status = db.PrescribeMedication(did=Did, pid=Pid, nameList=MedcineList, amount=AmountList)
            return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


def GetAllMedicine(request):
    # assert request.type == 'patient'
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        ans = db.GetAllMedicine()
        return JsonResponse({'info': ans})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def searchMedicine(request):
    # assert request.type == 'patient'
    name = request.GET.get('name', None)
    db = MySQLdb.MyDatabase()
    ans = db.searchMedicine(name=name)
    return JsonResponse({'medicineList': ans})


def PayAll(request):
    # assert request.type == 'patient'
    if request.method == 'POST':
        print("-------------------------------")
        data = json.loads(request.body)
        # Pid = '6'
        db = MySQLdb.MyDatabase()
        Pid = db.getIdByUsername(name=data['userName'])
        print(Pid)
        success, status = db.PayAll(Pid=Pid)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


def showAllDrugName(request):
    if request.method == 'GET':
        db = MySQLdb.MyDatabase()
        ans = db.showAllDrugName()
        return JsonResponse({'nameList': ans})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def MedicalDiagnosisStatement(request):
    # assert request.type == 'doctor'
    if request.method == 'POST':
        # Did = request.session['id']
        data = json.loads(request.body)
        # Did = '5'
        name = data['username']
        db = MySQLdb.MyDatabase()
        Did = db.getIdByUsername(name=name)
        Pid = data['Pid']
        Statement = data['Diagnosis']
        success, status = db.MedicalDiagnosisStatement(Did=Did, Pid=Pid, Statement=Statement)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


def getDiagnosisByPid(request):
    # assert request.type == 'patient'
    if request.method == 'GET':
        # Pid = request.session['id']
        # Pid = '6'
        data = json.loads(request.body)
        Pid = data['Pid']
        db = MySQLdb.MyDatabase()
        ans = db.getDiagnosisByPid(Pid=Pid)
        l = []
        for i in ans:
            jsonObj = {"time": i["time"], "statement": i["statement"]}
            l.append(jsonObj)
        return JsonResponse({'Info': l})
    else:
        return HttpResponse("Not a GET request")


def getLaboratorySheetids(request):
    # assert request.type == 'patient'
    if request.method == 'GET':
        # Pid = request.session['id']
        # Pid = '6'
        username = request.GET.get('username', None)
        db = MySQLdb.MyDatabase()
        Pid = db.getIdByUsername(username)
        print(Pid)
        ans = db.showAllLaboratorySheetIds(Pid=Pid)
        print(ans)
        return JsonResponse({'assayList': ans})
    else:
        return HttpResponse("Not a GET request")


@csrf_exempt
def getLaboratorySheet(request):
    # assert request.type == 'patient'
    if request.method == 'POST':
        # Pid = request.session['id']
        data = json.loads(request.body)
        Sheetid = data['id']
        db = MySQLdb.MyDatabase()
        ans = db.getLaboratorySheet(id=Sheetid)
        print(ans)
        return JsonResponse({'assayItemList': ans})
    else:
        return HttpResponse("Not a GET request")


@csrf_exempt
@transaction.atomic
def conductLaboratorySheet(request):
    # assert request.type == 'doctor'
    if request.method == 'POST':
        # Did = request.session['id']
        # Did = '5'
        data = json.loads(request.body)
        username = data['username']
        db = MySQLdb.MyDatabase()
        Did = db.getIdByUsername(name=username)
        Pid = data['Pid']
        checkName = data['checkName']
        checkItemIds = data['checkItemIds'] if 'checkItemIds' in data else None
        success, status = db.conductAlaboratoryAnalysis(checkName=checkName, checkItemIds=checkItemIds, Did=Did,
                                                        Pid=Pid)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
@transaction.atomic
def sendAnalysisList(request):
    # assert request.type == 'doctor'
    if request.method == 'POST':
        # Did = request.session['id']
        # Did = '5'
        data = json.loads(request.body)
        username = data['username']
        db = MySQLdb.MyDatabase()
        Did = db.getIdByUsername(name=username)
        Pid = data['Pid']
        AnalysisList = data['AnalysisList']
        for i in AnalysisList:
            print(i.__class__)
            checkName = i
            checkItemIds = None
            success, status = db.conductAlaboratoryAnalysis(checkName=checkName, checkItemIds=checkItemIds, Did=Did,
                                                            Pid=Pid)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


@csrf_exempt
def deletePatient(request):
    # assert request.type == 'patient'
    if request.method == 'POST':
        # Pid = request.session['id']
        data = json.loads(request.body)
        username = data['username']
        db = MySQLdb.MyDatabase()
        Pid = db.getIdByUsername(name=username)
        db.SoftDeletePatient(id=Pid)
        return JsonResponse({"success": True})
    else:
        return HttpResponse("Not a POST request")


def checkThePosInQueueu(request):
    # assert request.type == 'patient'
    if request.method == 'GET':
        # Pid = request.session['id']
        data = json.loads(request.body)
        Pid = data['Pid']
        # Pid = '6'
        db = MySQLdb.MyDatabase()
        success, ans, id = db.getRegisterRelationInfo(Pid=Pid)
        if success:
            try:
                return JsonResponse({'success': success, 'queueNum': ans, 'code': 0, 'id': id,
                                     'msg': "您前面还有%d，您的号码为%d" % (ans, int(id))})
            except:
                print(id, ans)
                return HttpResponse("ERROR")
        else:
            return JsonResponse({'success': False, 'queueNum': -1, 'code': 404, 'id': -1, "msg": '尚未挂号'})
    else:
        return HttpResponse("Not a GET request")


@csrf_exempt
def showCounterById(request):
    # assert request.type == 'patient'
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        db = MySQLdb.MyDatabase()
        res, data = db.showCounterById(id=id)
        if not res:
            return JsonResponse({'code': 404, 'msg': '没有该id的订单'})
        else:
            return JsonResponse(data)
    else:
        return HttpResponse("Not a POST request")


def getDoctorDispatch(request):
    # assert request.type == 'doctor'
    if request.method == 'GET':
        # Did = request.session['id']
        data = json.loads(request.body)
        Did = data['Did']
        # Did = '5'
        db = MySQLdb.MyDatabase()
        res = db.getDoctorDispatcher(Did=Did)
        if len(res) != 0:
            return JsonResponse({'info': res})
        else:
            return JsonResponse({'code': 404, 'msg': '没有该医生的挂号信息'})
    else:
        return HttpResponse("Not a GET request")


def hardDeleteDrug(request):
    assert request.type == 'admin'
    if request.method == 'POST':
        name = request.get('name')
        db = MySQLdb.MyDatabase()
        db.HardDeleteDrug(name=name)
        return JsonResponse({'success': True, 'code': 0})
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
        # Pid = request.session['id']
        username = request.GET.get('username', None)
        db = MySQLdb.MyDatabase()
        Pid = db.getIdByUsername(name=username)
        r = db.getDiagnosisList(Pid=Pid)
        return JsonResponse({'diagnosisList': r})
    else:
        return HttpResponse('NOT A GET REQUEST')


@csrf_exempt
def answer(request):
    d = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    content = data['question']
    departmentlist = d.GetDepartmentList()
    sendText = "你好，我是一名病人，我的症状是" + content + "，请我应该选择从" + str(
        departmentlist) + "中的哪个科室就诊？在三十到八十个字以内解决，假设你是医院的智能导医台（但回答中不要提及这一点）"
    openai.api_key = GPT_API_KEY
    openai.api_base = "https://api.openai.com/v1"

    print(sendText)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': sendText}
        ],
        temperature=0.5,
        max_tokens=300,
        stream=True
    )

    result = ""

    for chunk in response:
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            result += chunk_msg  # 将输出内容附加到结果字符串上
            # print(chunk_msg, end='', flush=True)
            # time.sleep(0.05)

    print(result)

    return JsonResponse({"answer": result})


def account(request):
    # 获取 session 中的信息

    # 打印 session 的键值对信息
    username = request.GET.get('username', None)
    db = MySQLdb.MyDatabase()
    account = {}
    account['username'] = username
    account['gender'] = 0
    account['age'] = 18
    permissions = []
    u = db.getUserById(db.getIdByUsername(name=username))
    permissions.append(u.type)
    if u.avatar is not None:
        account['avatar'] = u.avatar
    else:
        account['avatar'] = DEFAULT_AVATAR
        db.updateAvatar(id=u.id, avatar=account['avatar'])
    print(account['avatar'])
    if u.type == 'doctor':
        account['jobtitle'] = db.getDoctorById(id=u.id)['jobtitle']
    else:
        account['jobtitle'] = ''
    role = u.type
    j = {'account': account, 'permission': permissions, 'role': role}
    return JsonResponse(j)


def conductMedcine(request):
    assert request.type == 'doctor'
    if request.method == 'POST':
        # Did = request.session['id']
        data = json.loads(request.body)
        Did = data['Did']
        Pid = data['Pid']
        MedcineList = request.POST.get('MedcineList')
        AmountList = request.POST.get('AmountList')
        db = MySQLdb.MyDatabase()
        success, status = db.PrescribeMedication(did=Did, pid=Pid, nameList=MedcineList, amount=AmountList)
        return JsonResponse({'success': success, 'code': status})
    else:
        return HttpResponse("Not a POST request")


def queryDrugInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        db = MySQLdb.MyDatabase()
        return JsonResponse(db.queryDrugInfo)


def showAllUser(request):
    assert request.method == 'GET'
    db = MySQLdb.MyDatabase()
    print(db.showAllUser())
    return HttpResponse('Success')


def deleteCounter(request):
    db = MySQLdb.MyDatabase()
    db.deleteAllCounter()
    return HttpResponse('Success')


@csrf_exempt
def getDiagnosis(request):
    db = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    id = data['id']
    r = db.getDiagnosisById(id=id)
    return JsonResponse({'info': r})


@csrf_exempt
def getPatient(request):
    db = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    room = data['room']
    print(room)
    print('-------------------')
    p = db.getCurrentPatient(RoomId=room)
    if p == False:
        return JsonResponse({'name': '无', 'id': -1})
    return JsonResponse({'name': p['name'], 'id': p['id']})


@csrf_exempt
def addDoctor(request):
    db = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    name = data['username']
    tittle = data['tittle']
    password = data['password']
    l, _ = db.addDoctor(name=name, tittle=tittle, password=password)
    return JsonResponse({'success': l})


@csrf_exempt
def getDispatch(request):
    db = MySQLdb.MyDatabase()
    username = request.GET.get('username', None)
    print(username)
    id = db.getIdByUsername(name=username)
    print(id)
    r = db.getDispathcOfDoc(Did=id)
    print(r)
    return JsonResponse({'info': r})


@csrf_exempt
def getAnalysisList(request):
    db = MySQLdb.MyDatabase()
    r = db.getAnalysisList()
    print(r)
    return JsonResponse({'info': r})


@csrf_exempt
def addPatient(request):
    db = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    name = data['username']
    password = data['password']
    s = db.addCommemPatient(username=name, password=password)
    return JsonResponse({'success': s})


@csrf_exempt
def getStorage(request):
    db = MySQLdb.MyDatabase()
    r = db.getAllStorage()
    return JsonResponse({'info': r})


@csrf_exempt
def deleteMedicine(request):
    db = MySQLdb.MyDatabase()
    id = request.GET.get('id', None)
    db.HardDeleteDrug(id=id)
    return JsonResponse({'success': True})


@csrf_exempt
def nextPatient(request):
    db = MySQLdb.MyDatabase()
    data = json.loads(request.body)
    id = data['id']
    l = db.NextPatient(Did=id)
    return JsonResponse({'success': l})


@csrf_exempt
def getMedicineList(request):
    db = MySQLdb.MyDatabase()
    name = request.GET.get('name', None)
    r = db.getMedicineList(name=name)
    print(r)
    return JsonResponse({'medicineList': r})


@csrf_exempt
def addMedicine(request):
    data = json.loads(request.body)
    Medicine = data['Medicine']
    Amount = data['Amount']
    Price = data['Price']
    Description = data['Description']
    db = MySQLdb.MyDatabase()
    db.addMedicine(name=Medicine, amount=Amount, price=Price, description=Description)
    return JsonResponse({'success': True})


@csrf_exempt
def updateAvatar(request):
    data = json.loads(request.body)
    username = data['username']
    avatar = data['avatar']
    db = MySQLdb.MyDatabase()
    db.updateAvatar(id=db.getIdByUsername(name=username), avatar=avatar)
    return JsonResponse({'success': True})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def uploadAvatar(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        username = request.POST.get('username', None)

        # Ensure 'avatar.jpg' is a unique name for each user
        file_path = f'avatar_{username}.jpg'

        # Read the content of the uploaded file
        file_data = f.read()

        # Save the file locally
        with open(file_path, 'wb') as file:
            file.write(file_data)

        # Use your uploader class to upload the image
        from .upload import uploader
        u = uploader()
        u.__int__()
        url = u.upload_image(file_path)

        # Update the avatar URL in the database
        db = MySQLdb.MyDatabase()
        id = db.getIdByUsername(name=username)
        db.updateAvatar(id=id, avatar=url)

        return JsonResponse({'avatar': url})

    return JsonResponse({'status': False, 'message': 'Invalid request method'})


@csrf_exempt
def getAllDoctors(request):
    db = MySQLdb.MyDatabase()
    r = db.getAllDoctors()
    return JsonResponse({'doctorList': r})


@csrf_exempt
def getAllPatients(request):
    db = MySQLdb.MyDatabase()
    r = db.getAllPatients()
    return JsonResponse({'patientList': r})
