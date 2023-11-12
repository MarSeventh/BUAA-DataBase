import pymysql
from datetime import datetime
import models

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

    def login(self, username: str, password: str):
        if username == 'admin':
            success, status, t = self.admin_login(username, password)
            return success, status, t
        else:
            success, status, t = self.patient_login(username, password)
            if success:
                return success, status, t
            else:
                success, status, t = self.doctor_login(username, password)
                return success, status, t

    def patient_login(self, name: str, password: str):
        self.connect()
        sql = "SELECT * FROM patient WHERE name = %s"
        self.cursor.execute(sql, name)
        result = self.cursor.fetchall()
        self.close()
        if len(result) == 0:
            return False, ERROR_CODE, 'error'
        if result[0]['password'] == password:
            return True, 0, 'patient'
        else:
            return False, 404, 'error'

    def doctor_login(self, name: str, password: str):
        self.connect()
        sql = "SELECT * FROM doctor WHERE name = %s"
        self.cursor.execute(sql, name)
        result = self.cursor.fetchall()
        self.close()
        if len(result) == 0:
            return False, 404, 'error'
        if result[0]['password'] == password:
            return True, 0, 'doctor'
        else:
            return False, 404, 'error'

    def admin_login(self, id: str, password: str):
        self.connect()
        sql = "SELECT * FROM admin WHERE id = %s"
        self.cursor.execute(sql, id)
        result = self.cursor.fetchall()
        self.close()
        if len(result) == 0:
            return False, 404, 'error'
        if result[0]['password'] == password:
            return True, 0, 'admin'
        else:
            return False, 404, 'error'

    def patient_register(self, name: str, iscommem: bool, password: str, idcard: str):
        self.connect()
        sql = "SELECT * FROM patient WHERE name = %s"
        self.cursor.execute(sql, name)
        result = self.cursor.fetchall()
        if len(result) != 0:
            return False, 404
        if len(idcard) != 18:
            return False, 404
        sql0 = "SELECT MAX(id) FROM patient"
        self.cursor.execute(sql0)
        result = self.cursor.fetchall()
        id = str(int(result[0]['MAX(id)']) + 1)
        iscommem = 1 if iscommem else 0
        sql = "INSERT INTO patient (id, name, iscommem, password, idcard, active) VALUES (%s, %s, %s, %s, %s, 1)"
        self.cursor.execute(sql, (id, name, iscommem, password, idcard))
        self.connection.commit()
        self.close()
        return True, 0

    def SoftDeletePatient(self, name: str):  # 软删除
        self.connect()
        sql0 = "SELECT isComMem FROM patient WHERE name = %s"
        self.cursor.execute(sql0, name)
        result = self.cursor.fetchall()
        if (result[0]['isComMem'] == 0):
            sql1 = "UPDATE patient SET active = 0 WHERE name = %s"
            self.cursor.execute(sql1, name)
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

    def registByPatient(self, patientid: str, doctorid: str):
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
            sql = "INSERT INTO COUNTER (id, Pid, Did, isPaid, price) VALUES (%s, %s, %s, 1, 1)"
            self.cursor.execute(sql, (self.genCounterId(), patientid, doctorid))
            self.connection.commit()
            sql2 = "INSERT INTO RegistRelation (id, ROOMID) VALUES (%s, %s)"
            self.cursor.execute(sql2, (self.genCounterId(), r[0]['ROOMID']))
            self.connection.commit()
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
