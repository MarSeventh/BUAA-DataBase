import pymysql
from datetime import datetime

from django.db import transaction

from . import models
from django.db.models import Max

ERROR_CODE = 404


class MyDatabase:
    def connect(self):
        host = '120.46.80.149'
        user = '21373405'
        password = 'Aa490635'
        db = 'db21373405'
        charset = 'utf8mb4'
        cursorclass = pymysql.cursors.DictCursor
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset,
                                          cursorclass=cursorclass)
        self.cursor = self.connection.cursor()

    def getUserById(self, id : str):
        from .models import User
        return User.objects.get(id=id)

    def close(self):
        self.connection.close()

    def queryidbyusername(self, username: str):
        from .models import User
        result = User.objects.filter(username=username)
        return result[0].id

    def Login(self, username: str, password: str):
        from .models import User
        User.objects.filter(username=username, password=password)
        if len(User.objects.filter(username=username, password=password)) == 0:
            return False, 404, None
        else:
            from .models import Patient
            u = User.objects.get(username=username)
            print(u.id)
            p = Patient.objects.get(id=u.id)
            if p.active:
                return True, 0, User.objects.filter(username=username, password=password)[0]
            else:
                return False, 404, None


    def SignUpByPatient(self, name: str, iscommem: bool, password: str, idcard: str):
        from .models import User, Patient
        r = User.objects.filter(username=name)
        if len(r) != 0:
            print('用户名重叠')
            return False, 404
        if len(idcard) != 18:
            print('身份证号不合法')
            return False, 404
        last_user = User.objects.all().order_by('-id').first()
        ids = []
        it = User.objects.all().iterator()
        for i in it:
            ids.append(int(i.id))
        ids.sort()
        if len(ids) == 0:
            new_id = '1'
        else:
            new_id = str(ids[len(ids) - 1] + 1)
        from .models import User, Patient
        User.objects.create(id=new_id, username=name, type='patient', password=password)
        Patient.objects.create(id=new_id, iscommem=iscommem, idcard=idcard, active=1)
        return True, 0

    def SoftDeletePatient(self, id: str):  # 软删除
        from .models import Patient
        result = Patient.objects.filter(id=id)
        if (result[0].iscommem == 0):
            Patient.objects.filter(id=id).update(active=0)
            return True
        else:
            return False

    def HardDeleteDrug(self, id: str):
        from .models import Drug
        self.connect()
        sql = "DELETE FROM DRUG WHERE id = %s"
        self.cursor.execute(sql, id)
        self.connection.commit()
        return True

    def SoftDeleteDrug(self, name: str):
        from .models import Drug
        Drug.objects.filter(name=name).update(active=0)
        return True

    def QueryPatientCounterToPay(self, id: str):
        from .models import Counter
        result = Counter.objects.filter(pid=id, ispaid=False)
        return result

    def getDate(self):
        today = datetime.now()
        day_of_week = today.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[day_of_week]
        return day_name

    def QueryPatientAllCounter(self, id: str):
        from .models import Counter
        result = Counter.objects.filter(pid=id)
        return result

    def QueryCounterById(self, id: str):
        from .models import Counter
        result = Counter.objects.filter(id=id)
        return result

    def GetDepartmentList(self):
        from .models import Titles
        result = []
        l = Titles.objects.all()
        for i in l:
            result.append(i.name)
        return result

    def get_time_period(self):
        # 获取当前时间
        current_time = datetime.now().time()

        # 设置时间范围
        morning_start = datetime.strptime('08:00', '%H:%M').time()
        morning_end = datetime.strptime('13:00', '%H:%M').time()

        afternoon_start = datetime.strptime('14:00', '%H:%M').time()
        afternoon_end = datetime.strptime('22:00', '%H:%M').time()

        # 判断当前时间所属时间段
        if morning_start <= current_time <= morning_end:
            return "morning"
        elif afternoon_start <= current_time <= afternoon_end:
            return "afternoon"
        else:
            return "not in time range"

    def GetInfoListByDepartment(self, name: str):
        self.connect()
        timePeriod = self.get_time_period()
        sql = "SELECT doctorId, ROOMid FROM Dispatcher WHERE TitleId = (SELECT id FROM Titles WHERE name = %s) AND TimePeriod = %s AND DATE = %s"
        self.cursor.execute(sql, (name, self.get_time_period(), self.getDate()))
        r = self.cursor.fetchall()
        l = []
        for i in r:
            doctor = models.Doctor.objects.get(id=i['doctorId'])
            name = models.User.objects.get(id=doctor.id).username
            room = models.Room.objects.get(id=i['ROOMid'])
            l.append({'doctor': name, 'room': room.id, 'queueLen': room.queuelen})
        print(l)
        self.close()
        return l

    def NextPatient(self, Did: str):
        from .models import Room, Registrelation, Dispatcher
        RoomId = self.getRoomIdByDid(Did=Did)
        r = self.getCurrentRegistRelation(RoomId)
        Registrelation.objects.filter(id=r.id).update(isfinished=True)
        Room.objects.filter(id=RoomId).update(queuelen=Room.objects.get(id=RoomId).queuelen - 1)
        
    def finishPatiet(self, Did: str, Pid : str):
        RoomId = self.getRoomIdByDid(Did=Did)
        if RoomId == None:
            return False
        from .models import Room, Registrelation, Counter
        c = Counter.objects.filter(pid=Pid, type='Registration').iterator()
        r = None
        for i in c:
            if Registrelation.objects.get(id=i).isfinished == False:
                r = i
                break
        if r == None:
            return False
        Registrelation.objects.filter(id=r).update(isfinished=True)
        Room.objects.filter(id=RoomId).update(queuelen=Room.objects.get(id=RoomId).queuelen - 1)
        return True
    
    def getRoomIdByDid(self, Did: str):
        from .models import Dispatcher
        r = Dispatcher.objects.filter(doctorid=Did, timeperiod=self.get_time_period(), date=self.getDate())
        if len(r) == 0:
            return None
        else:
            return r[0].roomid

    def getCurrentPatient(self, RoomId: str):
        from .models import  User, Counter
        self.connect()
        sql = "SELECT *FROM RegistrelationWHERE RoomId = '输入值' AND isFinished = 0 ORDER BY CAST(id AS UNSIGNED)LIMIT 1;"
        self.cursor.execute(sql, RoomId)
        r = self.cursor.fetchone()
        c = Counter.objects.filter(id=r['id'])
        self.close()
        p = User.objects.get(id=c[0].pid)
        info = {'name' : p.username, 'id' : p.id}
        return info
    
    def getCurrentRegistRelation(self, RoomId: str):
        from .models import Registrelation
        r = Registrelation.objects.filter(roomid=RoomId, isfinished=False)
        if len(r) == 0:
            return None
        else:
            return r[0]

    @transaction.atomic
    def PatientRegistration(self, patientid: str, doctorid: str):
        timePeriod = self.get_time_period()
        from .models import Dispatcher, Counter, Registrelation, Patient, Room
        r0 = Dispatcher.objects.filter(doctorid=doctorid, timeperiod=timePeriod, date=self.getDate()).values_list(
            'roomid', flat=True).first()
        if r0 == None:
            print('NO DOCTOR' + doctorid + 'IN ' + timePeriod)
            return '-2', False, 404
        r = Counter.objects.filter(pid=patientid, did=doctorid, type='Registration', ispaid=False)
        if r == None:
            iscommem = Patient.objects.get(id=patientid).iscommem
            price = 1 if iscommem else 10
            id = self.createNewCounter(pid=patientid, did=doctorid, type='Registration', price=price)
            room = r0
            Registrelation.objects.create(id=Counter.objects.get(id=id), isfinished=0, roomid=room)
            print(room)
            Room.objects.filter(id=room).update(queuelen=Room.objects.get(id=room).queuelen + 1)
            return id, True, 0
        else:
            print('ALREADY REGISTERED')
            return '-2', False, 404

    def genCounterId(self):
        self.connect()
        sql = "SELECT MAX(CAST(id AS UNSIGNED)) AS max_id FROM COUNTER"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.close()
        max_id = result['max_id']
        if max_id is None:
            return '1'
        else:
            return str(int(max_id) + 1)

    def showAllNeedToPay(self, Pid : str):
        from .models import Counter
        l = Counter.objects.filter(pid=Pid, ispaid=False).iterator()
        res = []
        for i in l:
            res.append({'id': i.id, 'type': i.type, 'price': i.price})
        return res

    def showCounterById(self, id: str):
        from .models import Counter, Laboratorysheet, Registrelation, Medicinepurchase, Doctor
        assert len(Counter.objects.filter(id=id)) != 0
        c = Counter.objects.get(id=id)
        l1 = len(Laboratorysheet.objects.filter(id=c))
        l2 = len(Registrelation.objects.filter(id=c))
        l3 = len(Medicinepurchase.objects.filter(id=c))
        if l1 != 0:
            l = Laboratorysheet.objects.filter(id=c)
            return True , {'type': "化验订单", 'name': l[0].checkname, 'price': c.price}
        elif l2 != 0:
            l = Registrelation.objects.get(id=c)
            Did = Counter.objects.get(id=id).did
            try:
                Dname = models.User.objects.get(id=Did.id).username
            except:
                print(Did.id)
                print('no such doctor')
                return False, 404
            return True, {'type': "挂号订单", 'name': format("您对%s医生的挂号" % Dname),
                    'price': Counter.objects.get(id=id).price}
        elif l3 != 0:
            return True, {'type': "购药订单", 'name': '购药订单', 'price': Counter.objects.get(id=id).price}
        else:
            print('no such counter')
            return False, 404

    def showMedicinePurchase(self, id: str):
        from .models import Medicinepurchase, Drug
        l = Medicinepurchase.objects.filter(id=id)
        res = []
        for i in l:
            res.append({'name': Drug.objects.get(id=i.drugid).name, 'amount': i.amount,
                        'signalPrice': Drug.objects.get(id=i.drugid).price,
                        'price': i.amount * Drug.objects.get(id=i.drugid).price})
        return res

    def PayCounter(self, id: str):
        self.connect()
        sql = "UPDATE COUNTER SET isPaid = 1 WHERE id = %s"
        self.cursor.execute(sql, id)
        self.connection.commit()
        self.close()

    def showAllinCounter(self, Pid : str):
        from .models import Counter
        l = Counter.objects.filter(pid=Pid).iterator()
        res = []
        for i in l:
            res.append({'id': i.id, 'type': i.type, 'ispaid': i.ispaid, 'price': i.price})
            if i.price == None:
                print('price is None')
            else:
                print(i.price)
        return res

    def showAllinCounterByPid(self, pid: str):
        from .models import Counter
        l = Counter.objects.filter(pid=pid).iterator()
        res = []
        for i in l:
            res.append({'id': i.id, 'type': i.type, 'price': i.price})
        return res

    def getIdByUsername(self, name: str):
        d = models.User.objects.filter(username=name)
        if len(d) != 0:
            return d[0].id
        else:
            return None

    def getNameById(self, id: str):
        d = models.User.objects.filter(id=id)
        print(id)
        if len(d) != 0:
            return d[0].username
        else:
            return None

    def createNewCounter(self, pid: str, did: str, price: float, type: str):
        id = self.genCounterId()
        from .models import Counter, Doctor, Patient
        p = Patient.objects.filter(id=pid)
        d = Doctor.objects.filter(id=did)
        if len(p) == 0 or len(d) == 0:
            return False
        elif price == None:
            Counter.objects.create(id=id, pid=p[0], did=d[0], price=0, ispaid=0, type=type, date=datetime.now())
        else:
            Counter.objects.create(id=id, pid=p[0], did=d[0], price=price, ispaid=0, type=type, date=datetime.now())
        return id

    def PrescribeMedication(self, nameList : list, amount : list, pid: str, did: str):
        idList = []
        for i in nameList:
            from .models import Drug
            result = Drug.objects.filter(name=i)
            if len(result) == 0:
                return False, 404
            idList.append(result[0].id)

        id = self.createNewCounter(pid=pid, did=did, type='Medicine', price=0)
        if id == False:
            print(pid)
            print(did)
            return False, 404
        from .models import Medicinepurchase, Counter, Drug
        for i in range(len(idList)):
            Medicinepurchase.objects.create(id=Counter.objects.get(id=id), drugid=Drug.objects.get(id=idList[i]), amount=amount[i])
            Counter.objects.filter(id=id).update(
                price=Counter.objects.get(id=id).price + amount[i] * Drug.objects.get(id=idList[i]).price)
            Drug.objects.filter(id=idList[i]).update(storage=Drug.objects.get(id=idList[i]).storage - amount[i])
        return True, 0


    def showAllDrugName(self):
        from .models import Drug
        l = Drug.objects.all().iterator()
        res = []
        for i in l:
            res.append(i.name)
        return res
    
    def showAllDrug(self):
        from .models import Drug
        l = Drug.objects.all().iterator()
        res = []
        for i in l:
            res.append({'id': i.id, 'name': i.name, 'price': i.price, 'Storage': i.storage, 'description': i.description})
        return res

    def PayAll(self, Pid : str):
        from .models import Counter
        l = Counter.objects.filter(pid=Pid).iterator()
        for i in l:
            Counter.objects.filter(id=i.id).update(ispaid=True)
            c = Counter.objects.get(id=i.id)
            print(c.ispaid)
        return True, 0

    def MedicalDiagnosisStatement(self, Did: str, Pid: str, Statement: str):
        from .models import Diagnosis, Patient, Doctor
        if len(Diagnosis.objects.all()) == 0:
            id = '1'
        else:
            self.connect()
            sql = "SELECT MAX(CAST(id AS UNSIGNED)) AS max_id FROM DIAGNOSIS"
            self.cursor.execute(sql)
            id = self.cursor.fetchone()
            self.close()
        Diagnosis.objects.create(id=id, doctorid=Doctor.objects.get(id=Did), patientid=Patient.objects.get(id=Pid), time=datetime.now(), diagnosis=Statement)
        return True, 0

    def getDiagnosisByPid(self, Pid: str):
        from .models import Diagnosis
        l = Diagnosis.objects.filter(patientid=Pid).iterator()
        res = []
        for i in l:
            res.append({'doctor': self.getNameById(i.doctorid.id), 'time': i.time, 'statement': i.diagnosis})
        return res

    def conductAlaboratoryAnalysis(self, Pid: str, Did: str, checkItemIds : list, checkName: str):
        from .models import Checkcombine
        m = Checkcombine.objects.filter(checkname=checkName)
        if m == None:
            assert len(checkItemIds) != 0
            from .models import Laboratorysheet, Counter
            id = str(int(Counter.objects.all().order_by('-id')[0].id) + 1)
            Counter.objects.create(id=id, pid=Pid, did=Did, price=0, ispaid=0, type='Laboratory', date=datetime.now())
            for i in checkItemIds:
                from .models import Checkitems
                Laboratorysheet.objects.create(id=id, itemid=i, time=datetime.now(), checkName=checkName)
                Counter.objects.filter(id=id).update(
                    price=Counter.objects.get(id=id).price + Checkitems.objects.get(itemid=i).price)
            return True, 0
        else:
            r = Checkcombine.objects.filter(checkname=checkName).iterator()
            from .models import Laboratorysheet, Counter, Patient, Doctor, Checkitems
            id = self.genCounterId()
            Counter.objects.create(id=id, pid=Patient.objects.get(id=Pid), did=Doctor.objects.get(id=Did), price=0, ispaid=0, type='Laboratory', date=datetime.now())
            for i in r:
                from .models import Checkitems
                try:
                    Laboratorysheet.objects.create(id=Counter.objects.get(id=id), itemid=i.itemid, begintime=datetime.now(), checkname=checkName, result=-1)
                    Counter.objects.filter(id=id).update(price=Counter.objects.get(id=id).price + i.itemid.price)
                except:
                    print(i.itemid)
                    return False, 404
            return True, 0

    def getLaboratorySheet(self, id: str):
        print(id)
        from .models import Laboratorysheet, Counter
        l = Laboratorysheet.objects.filter(id=Counter.objects.get(id=id)).iterator()
        print(l)
        if l == None:
            return False
        else:
            res = []
            for i in l:
                print(i)
                from .models import Checkitems
                res.append({'itemid': int(i.itemid.id), 'checkName': i.itemid.description, 'result': i.result if i.result != None else -1,
                            'minresult': i.itemid.minresult,
                            'maxresult': i.itemid.maxresult, 'outputtime': str(datetime.now()) if i.outputtime == None else self.formatedDate(str(i.outputtime))
                            })
            print(res)
            return res

    def showAllLaboratorySheetIds(self, Pid: str):
        from .models import Laboratorysheet, Counter, Checkitems
        id = Counter.objects.filter(pid=Pid, type='Laboratory').iterator()
        res = []
        for i in id:
            if i.price == 0:
                continue
            print(i)
            l = Laboratorysheet.objects.filter(id=i)
            if len(l) != 0:
                x = l[0]
                res.append({'id': x.id.id, 'checkName' : x.checkname, 'time' : self.formatedDate(str(x.begintime))})
        return res

    def getRegisterRelationInfo(self, Pid: str):
        from .models import Registrelation, Counter
        id = Counter.objects.filter(pid=Pid, type='Registration').iterator()
        res = []
        for i in id:
            if Registrelation.objects.get(id=i.id).isfinished == False:
                res.append({'id': i.id})
        if len(res) == 0:
            return False, 404
        Rid = res[0]['id']
        l = Registrelation.objects.get(id=Rid, isfinished=0)
        if l == None:
            return False, 404, -1
        else:
            roomid = l.roomid
            o = Registrelation.objects.filter(isfinished=False, roomid=roomid).order_by(('id_id')).iterator()
            ans = 0
            for i in o:
                if int(i.id.id) < int(l.id.id):
                    ans += 1
            return True, ans, l.id.id

    def getDoctorDispatcher(self, Did: str):
        from .models import Dispatcher, Doctor
        r = Dispatcher.objects.filter(doctorid=Doctor.objects.get(id=Did))
        res = []
        for i in r:
            res.append({'timeperiod': i.timeperiod, 'RoomId': i.roomid.id, 'date': i.date})
        return res

    def getCheckItemsList(self):
        from .models import Checkitems
        r = Checkitems.objects.all().iterator()
        res = []
        for i in r:
            res.append({'id': i.id, 'name': i.description, 'price': i.price})
        return res

    def getCheckCombineList(self):
        from .models import Checkcombine
        r = Checkcombine.objects.all().iterator()
        res = []
        for i in r:
            res.append({'name': i.checkname})
        return res

    def finishPay(self, id: str):
        from .models import Counter
        print(id)
        c = Counter.objects.filter(id=id)
        if c == None:
            return False
        Counter.objects.filter(id=id).update(ispaid=True)
        return True

    def getDiagnosisList(self, Pid: str):
        from .models import Diagnosis, Patient
        r = Diagnosis.objects.filter(patientid=Patient.objects.get(id=Pid)).iterator()
        res = []
        for i in r:
            j = {'id': i.id, 'time': self.formatedDate(str(i.time)), 'doctor': self.getNameById(id=i.doctorid.id)}
            res.append(j)
        print(res)
        return res

    def formatedDate(self, Date):
        datetime_obj = datetime.strptime(Date, "%Y-%m-%d %H:%M:%S%z")

        # 将 datetime 对象格式化为指定格式的字符串
        formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        print(formatted_date)
        return formatted_date

    def getDiagnosisById(self, id : str):
        from .models import Diagnosis
        r = Diagnosis.objects.get(id=id)
        res = {'doctor' : self.getNameById(r.doctorid.id), 'statement' : r.diagnosis, 'time' : r.time}
        return res

    def genUserId(self):
        from .models import User
        max_id = User.objects.all().aggregate(Max('id'))['id__max']
        return str(int(max_id) + 1)

    def getTidByName(self, name: str):
        from .models import Titles
        return Titles.objects.get(name=name)[0]

    def createNewDoctor(self, name: str, tittle: str, password: str):
        from .models import Doctor, User
        id = self.genUserId()
        User.objects.create(id=id, username=name, password=password, type='Doctor')
        Doctor.objects.create(id=id, Tid=self.getTidByName(name=tittle), active=1)

    def queryDrugInfo(self, id: str):
        from .models import Drug
        r = Drug.objects.get(id=id)
        return r

    def getUserTypeById(self, id: str):
        from .models import User
        r = User.objects.get(id=id)
        return r['type']

    def showAllUser(self):
        from .models import User
        r = User.objects.all().iterator()
        a = []
        for i in r:
            a.append({'id': i.id, 'username': i.username, 'type': i.type, 'password': i.password})
        return a

    def deleteAllCounter(self):
        from .models import Counter
        Counter.objects.all().delete()
        
    def addDoctor(self, name: str, tittle: str, password: str):
        from .models import Doctor, User
        id = self.genUserId()
        User.objects.create(id=id, username=name, password=password, type='Doctor')
        Doctor.objects.create(id=id, Tid=self.getTidByName(name=tittle), active=1)
        return True, 0
    
    def GetAllMedicine(self):
        from .models import Drug
        r = Drug.objects.all().iterator()
        res = []
        for i in r:
            res.append({'id': i.id, 'name': i.name, 'price': i.price, 'storage': i.storage, 'description': i.description})
        return res
    
    def searchMedicine(self, name: str):
        from .models import Drug
        r = Drug.objects.all.iterator()
        res = []
        for i in r:
            if i.name.find(name) != -1:
                res.append({'id': i.id, 'name': i.name, 'price': i.price})
        return res
    
    def getDispathcOfDoc(self, Did : str):
        from .models import Dispatcher, Doctor
        Did = Doctor.objects.get(id=Did)
        r = Dispatcher.objects.filter(doctorid=Did).iterator()
        res = []
        day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        period = ['morning', 'afternoon']
        for i in day:
            for j in period:
                d = Dispatcher.objects.filter(doctorid=Did, date=i, timeperiod=j)
                if len(d) != 0:
                    res.append(d[0].roomid.id)
        return res
    
    def getAnalysisList(self):
        from .models import Checkcombine
        r = Checkcombine.objects.all().iterator()
        res = []
        for i in r:
            if res.find(i.checkname) == -1:
                res.append(i.checkname)
        return res
    
    def addCommemPatient(self, username : str, password : str):
        from .models import User, Patient
        id = self.genUserId()
        User.objects.create(id=id, username=username, password=password, type='patient')
        Patient.objects.create(id=id, iscommem=True, active=True)
        return True, 0
    
    def getAllStorage(self):
        from .models import Drug
        r = Drug.objects.all().iterator()
        res = []
        for i in r:
            res.append({'id': i.id, 'name': i.name, 'storage': i.storage})
        return res
    
    def getAllMedicine(self):
        from .models import Drug
        r = Drug.objects.all().iterator()
        res = []
        for i in r:
            res.append({'id': i.id, 'name': i.name, 'price': i.price, 'amount': i.storage})
        return res