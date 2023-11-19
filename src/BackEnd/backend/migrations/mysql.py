import pymysql
from datetime import datetime
from . import models
from django.db.models import Max

ERROR_CODE = 404

class MyDatabase:
    def connect(self):
        host = '120.46.80.149'
        user = 'u21373405'
        password = 'Aa490635'
        db = 'db21373405'
        charset = 'utf8mb4'
        cursorclass = pymysql.cursors.DictCursor
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset,
                                          cursorclass=cursorclass)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def queryidbyusername(self, username: str):
        self.connect()
        sql = "SELECT id FROM User WHERE name = %s"
        self.cursor.execute(sql, username)
        result = self.cursor.fetchall()
        self.close()
        return result[0]['id']
    """
    """
    def SignUpByPatient(self, name: str, iscommem: bool, password: str, idcard: str):
        self.connect()
        sql0 = "SELECT id FROM User WHERE name = %s"
        self.cursor.execute(sql0, name)
        r = self.cursor.fetchall()
        id = r[0]['id']
        if len(id) != 0:
            return False, 404
        sql = "SELECT * FROM patient WHERE id = %s"
        self.cursor.execute(sql, id)
        result = self.cursor.fetchall()
        if len(result) != 0:
            return False, 404
        if len(idcard) != 18:
            return False, 404
        sql1 = "SELECT MAX(id) FROM patient"
        self.cursor.execute(sql1)
        result = self.cursor.fetchall()
        id = str(int(result[0]['MAX(id)']) + 1)
        iscommem = 1 if iscommem else 0
        sql = "INSERT INTO patient (id, iscommem, idcard, active) VALUES (%s, %s, %s, 1)"
        self.cursor.execute(sql, (id, iscommem, idcard))
        self.connection.commit()
        self.close()
        return True, 0

    def SoftDeletePatient(self, id: str):  # 软删除
        self.connect()
        sql0 = "SELECT isComMem FROM patient WHERE id = %s"
        self.cursor.execute(sql0, id)
        result = self.cursor.fetchall()
        if (result[0]['isComMem'] == 0):
            sql1 = "UPDATE patient SET active = 0 WHERE id = %s"
            self.cursor.execute(sql1, id)
            self.connection.commit()
            self.close()
            return True
        else:
            return False

    def HardDeleteDrug(self, name: str):
        self.connect()
        sql = "DELETE FROM drug WHERE name = %s"
        self.cursor.execute(sql, name)
        self.connection.commit()
        self.close()

    def SoftDeleteDrug(self, name: str):
        self.connect()
        sql = "UPDATE drug SET active = 0 WHERE name = %s"
        self.cursor.execute(sql, name)
        self.connection.commit()
        self.close()

    def QueryPatientCounterToPay(self, id: str):
        self.connect()
        sql = "SELECT * FROM COUNTER WHERE id = %s AND isPaid = 0"
        self.cursor.execute(sql, id)
        result = self.cursor.fetchall()
        self.close()
        return result

    def QueryPatientAllCounter(self, id: str):
        self.connect()
        sql = "SELECT id FROM COUNTER WHERE id = %s"
        self.cursor.execute(sql, id)
        result = self.cursor.fetchall()
        self.close()
        return result

    def QueryCounterById(self, id: str):
        self.connect()
        sql = "SELECT * FROM LABORATORYSHEET WHERE id = %s"
        self.cursor.execute(sql, id)
        result = self.cursor.fetchall()
        sql1 = "SELECT * FROM REGISTRELATION WHERE id = %s"
        self.cursor.execute(sql1, id)
        result1 = self.cursor.fetchall()
        sql2 = "SELECT * FROM MEDICINEPURCHASE WHERE id = %s"
        result2 = self.cursor.fetchall()
        self.close()

    def GetDepartmentList(self):
        self.connect()
        sql = "SELECT name FROM Titles"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.close()
        return result

    def get_time_period(self):
        # 获取当前时间
        current_time = datetime.now().time()

        # 设置时间范围
        morning_start = datetime.strptime('08:00', '%H:%M').time()
        morning_end = datetime.strptime('12:00', '%H:%M').time()

        afternoon_start = datetime.strptime('14:00', '%H:%M').time()
        afternoon_end = datetime.strptime('18:00', '%H:%M').time()

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
        sql = "SELECT doctorId, ROOMid FROM Dispatcher WHERE TitleId = (SELECT id FROM Titles WHERE name = %s) AND TimePeriod = %s"
        self.cursor.execute(sql, (name, timePeriod))
        r = self.cursor.fetchall()
        l = []
        for i in r:
            doctor = models.Doctor.objects.get(id=i['doctorId'])
            room = models.Room.objects.get(id=i['ROOMid'])
            l.append({'doctor': doctor.name, 'room': room.name, 'queueLen': room.queueLen})
        self.close()
        return l
    
    def NextPatient(self, Did : str, RoomId : str):
        from src.BackEnd.backend.migrations.models import Room, Registrelation
        assert Room.objects.get(id=RoomId) > 0
        r = self.getCurrentPatient(RoomId)
        Registrelation.objects.filter(id=r.id).update(isfinished=True)
        Room.objects.filter(id=RoomId).update(queuelen=Room.objects.get(id=RoomId).queuelen - 1)

    def getCurrentPatient(self, RoomId : str):
        from src.BackEnd.backend.migrations.models import Registrelation
        max_id = Registrelation.objects.filter(roomid=RoomId, isFinished=False).aggregate(Max('id'))['id__max']
        return Registrelation.objects.get(id=max_id)

    def PatientRegistration(self, patientid: str, doctorid: str):
        self.connect()
        timePeriod = self.get_time_period()
        sql = "SELECT * FROM Dispatcher WHERE doctorId = %s AND TimePeriod = %s"
        self.cursor.execute(sql, (doctorid, timePeriod))
        r = self.cursor.fetchall()
        if len(r) == 0:
            return False, 404
        sql = "SELECT * FROM REGISTRELATION WHERE doctorId = %s AND TimePeriod = %s"
        self.cursor.execute(sql, (doctorid, timePeriod))
        r = self.cursor.fetchall()
        if len(r) == 0:
            sql = "INSERT INTO COUNTER (id, Pid, Did, isPaid, price, type, date) VALUES (%s, %s, %s, 1, 1, 'Registration', %s)"
            self.cursor.execute(sql, (self.genCounterId(), patientid, doctorid, datetime.now()))
            self.connection.commit()
            sql2 = "INSERT INTO RegistRelation (id, ROOMID, isFinished) VALUES (%s, %s, False)"
            self.cursor.execute(sql2, (self.genCounterId(), r[0]['ROOMID']))
            self.connection.commit()
            models.Room.objects.filter(id=r[0]['ROOMID']).update(queueLen=models.Room.objects.get(id=r[0]['ROOMID']).queueLen + 1)
            self.close()
            return True, 0
        else:
            self.close()
            return False, 404

    def genCounterId(self):
        self.connect()
        sql = "SELECT MAX(id) FROM COUNTER"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.close()
        return str(int(result[0]['MAX(id)']) + 1)

    def showAllNeedToPay(self):
        self.connect()
        sql = "SELECT ID, PRICE FROM COUNTER WHERE ISPAID IS 0"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res
    
    def showCounterById(self, id : str):
        from src.BackEnd.backend.migrations.models import Counter, Laboratorysheet, Registrelation, Medicinepurchase
        assert len(Counter.objects.filter(id=id)) != 0
        l1 = len(Laboratorysheet.objects.filter(id=id))
        l2 = len(Registrelation.objects.filter(id=id))
        l3 = len(Medicinepurchase.objects.filter(id=id))
        if l1 != 0:
            l = Laboratorysheet.objects.get(id=id)
            return {'type' : "化验订单", 'name' : l.checkname, 'price' : Counter.objects.get(id=id).price}
        elif l2 != 0:
            l = Registrelation.objects.get(id=id)
            Did = Counter.objects.get(id=id).did
            Dname = models.User.objects.get(id=Did).username
            return {'type' : "挂号订单", 'name' : format("您对%s医生的挂号" % Dname), 'price' : Counter.objects.get(id=id).price}
        elif l3 != 0:
            l = Medicinepurchase.objects.filter(id=id)
            return {'type' : "购药订单", 'name' : '购药订单', 'price' : Counter.objects.get(id=id).price}
        else:
            return False
        
    def showMedicinePurchase(self, id : str):
        from src.BackEnd.backend.migrations.models import Medicinepurchase, Drug
        l = Medicinepurchase.objects.filter(id=id)
        res = []
        for i in l:
            res.append({'name': Drug.objects.get(id=i.drugid).name, 'amount': i.amount, 'signalPrice' : Drug.objects.get(id=i.drugid).price, 'price' : i.amount * Drug.objects.get(id=i.drugid).price})
        return res

    def PayCounter(self, id: str):
        self.connect()
        sql = "UPDATE COUNTER SET isPaid = 1 WHERE id = %s"
        self.cursor.execute(sql, id)
        self.connection.commit()
        self.close()

    def showAllinCounter(self):
        self.connect()
        sql = "SELECT * FROM COUNTER"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def showAllinCounterByPid(self, pid : str):
        self.connect()
        sql = "SELECT * FROM COUNTER WHERE Pid = %s"
        self.cursor.execute(sql, pid)
        res = self.cursor.fetchall()
        return res

    def showAllDiagnosisByPid(self, id : str):
        models.Diagnosis.objects.filter(patientid=id)
        l = []
        for i in models.Diagnosis.objects.filter(patientid=id):
            dname = self.getNameById(i.doctorid)
            l.append({'doctor': dname, 'time': i.time, 'diagnosis': i.diagnosis})
        return l

    def getIdByUsername(self, name : str):
        d = models.User.objects.filter(name=name)
        if len(d) != 0:
            return d[0].id
        else:
            return None
        

    def getNameById(self, id : str):
        d = models.User.objects.filter(id=id)
        if len(d) != 0:
            return d[0].name
        else:
            return None
        
    def createNewCounter(self, pid : str, did : str, price : float, type : str):
        self.connect()
        sql = "SELECT MAX(id) FROM COUNTER"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.close()
        id = str(int(result[0]['MAX(id)']) + 1)
        from src.BackEnd.backend.migrations.models import Counter
        if price == None:
            Counter.objects.create(id=id, pid=pid, did=did, price=0, ispaid=0, type=type, date=datetime.now())
        else:
            Counter.objects.create(id=id, pid=pid, did=did, price=price, ispaid=0, type=type, date=datetime.noew())
        return id

    def PrescribeMedication(self, nameList, amount, pid : str, did : str):
        self.connect()
        idList = []
        for i in nameList:
            sql = "SELECT id FROM DRUG WHERE name = %s"
            self.cursor.execute(sql, i)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return False, 404
            idList.append(result[0]['id'])

        id = self.createNewCounter(pid=pid, did=did, type='Medicine')
        from src.BackEnd.backend.migrations.models import Medicinepurchase, Counter, Drug
        for i in range(len(idList)):
            Medicinepurchase.objects.create(id=id, drugid=idList[i], amount=amount[i])
            Counter.objects.filter(id=id).update(price=Counter.objects.get(id=id).price + amount[i] * Drug.objects.get(id=idList[i]).price)
            Drug.objects.filter(id=idList[i]).update(Storage=Drug.objects.get(id=idList[i]).Storage - amount[i])
        self.connection.commit()
        self.close()
        return True, 0
        
    def showAllDrug(self):
        self.connect()
        sql = "SELECT * FROM DRUG WHERE ISBANNED = 0"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res
    
    def PayAll(self, Pid):
        from src.BackEnd.backend.migrations.models import Counter
        l = Counter.objects.filter(pid=Pid).iterator
        for i in l:
            i.ispaid = 1

    def MedicalDiagnosisStatement(self, Did : str, Pid : str, Statement : str):
        from src.BackEnd.backend.migrations.models import Diagnosis
        id = str(int(Diagnosis.objects.all().order_by('-id')[0].id) + 1)
        Diagnosis.objects.create(id=id, doctorid=Did, patientid=Pid, time=datetime.now(), diagnosis=Statement)
        return True, 0
    
    def getDiagnosisByPid(self, Pid : str):
        from src.BackEnd.backend.migrations.models import Diagnosis
        l = Diagnosis.objects.filter(patientid=Pid).iterator
        res = []
        for i in l:
            res.append({'doctor': self.getNameById(i.doctorid), 'time': i.time, 'statement': i.diagnosis})
        return res
    
    def conductAlaboratoryAnalysis(self, Pid : str ,Did : str, checkItemIds, checkName : str):
        from src.BackEnd.backend.migrations.models import Checkcombine
        m = Checkcombine.objects.filter(checkname=checkName)
        if m == None:
            assert len(checkItemIds) != 0
            from src.BackEnd.backend.migrations.models import Laboratorysheet, Counter
            id = str(int(Counter.objects.all().order_by('-id')[0].id) + 1)
            Counter.objects.create(id=id, pid=Pid, did=Did, price=0, ispaid=0, type='Laboratory', date=datetime.now())
            for i in checkItemIds:
                from src.BackEnd.backend.migrations.models import Checkitems
                Laboratorysheet.objects.create(id=id, itemid=i, time=datetime.now(), checkName=checkName)
                Counter.objects.filter(id=id).update(price=Counter.objects.get(id=id).price + Checkitems.objects.get(itemid=i).price)
            return True
        else:
            r = Checkcombine.objects.filter(checkName=checkName).get('itemid')
            from src.BackEnd.backend.migrations.models import Laboratorysheet, Counter
            id = str(int(Counter.objects.all().order_by('-id')[0].id) + 1)
            Counter.objects.create(id=id, pid=Pid, did=Did, price=0, ispaid=0, type='Laboratory', date=datetime.now())
            for i in r:
                from src.BackEnd.backend.migrations.models import Checkitems
                Laboratorysheet.objects.create(id=id, itemid=i, time=datetime.now(), checkName=checkName)
                Counter.objects.filter(id=id).update(price=Counter.objects.get(id=id).price + Checkitems.objects.get(itemid=i).price)
            return True
        
    def getLaboratorySheet(self, id : str):
        from src.BackEnd.backend.migrations.models import Laboratorysheet
        l = Laboratorysheet.objects.filter(id=id).iterator
        if l[0]['outputtime'] == None:
            return False
        else:
            res = []
            for i in l:
                from src.BackEnd.backend.migrations.models import Checkitems
                res.append({'id': i.itemid, 'name': i.checkName, 'result': i.result, 'minresult': Checkitems.objects.get(itemid=i.itemid).minresult, 'maxresult': Checkitems.objects.get(itemid=i.itemid).maxresult, 'outputtime': i.outputtime})
            return res
        
    def showAllLaboratorySheetIds(self, Pid : str):
        from src.BackEnd.backend.migrations.models import Laboratorysheet
        l = Laboratorysheet.objects.filter(id=Pid).iterator
        res = []
        for i in l:
            res.append({'id': i.id, 'time': i.time, 'name': i.checkName})
        return res
    
    def getRegisterRelationInfo(self, Pid : str):
        from src.BackEnd.backend.migrations.models import Registrelation
        l = Registrelation.objects.filter(id=Pid, isfinished=False).iterator
        if len(l) == 0:
            return False, 404, -1
        else:
            r = Registrelation.objects.filter(roomid=l[0]['roomid'], isfinished=False).iterator
            ans = 0
            for i in r:
                if i.id < l[0]['id']:
                    ans += 1
            return True, ans, l[0]['id']
        
    def getDoctorDispatcher(self, Did : str):
        from src.BackEnd.backend.migrations.models import Dispatcher
        r = Dispatcher.objects.filter(doctorid=Did)
        res = []
        for i in r:
            res.append({'timeperiod' : i.timeperiod, 'RoomId' : i.roomid})
        return res
        