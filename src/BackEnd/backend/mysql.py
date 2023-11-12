import pymysql


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

    def PatientLogIn(self, name: str, password: str):
        self.connect()
        sql = "SELECT * FROM patient WHERE name = %s AND password = %s"
        self.cursor.execute(sql, (name, password))
        result = self.cursor.fetchall()
        self.close()
        return len(result) != 0

    def DoctorLogIn(self, name: str, password: str):
        self.connect()
        sql = "SELECT * FROM doctor WHERE name = %s AND password = %s"
        self.cursor.execute(sql, (name, password))
        result = self.cursor.fetchall()
        self.close()
        return len(result) != 0

    def AdminLogIn(self, id: str, password: str):
        self.connect()
        sql = "SELECT * FROM admin WHERE id = %s AND password = %s"
        self.cursor.execute(sql, (id, password))
        result = self.cursor.fetchall()
        self.close()
        return len(result) != 0

    def PatientRegister(self, name: str, iscommem: bool, password: str, idcard: str):
        self.connect()
        sql = "SELECT * FROM patient WHERE name = %s"
        self.cursor.execute(sql, name)
        result = self.cursor.fetchall()
        if len(result) != 0:
            return False, 3
        if len(idcard) != 18:
            return False, 2
        sql0 = "SELECT MAX(id) FROM patient"
        self.cursor.execute(sql0)
        result = self.cursor.fetchall()
        id = str(int(result[0]['MAX(id)']) + 1)
        iscommem = 1 if iscommem else 0
        sql = "INSERT INTO patient (id, name, iscommem, password, idcard, active) VALUES (%s, %s, %s, %s, %s, 1)"
        self.cursor.execute(sql, (id, name, iscommem, password, idcard))
        self.connection.commit()
        self.close()
        return True, 1

    def SoftDeletePatient(self, name: str): # 软删除
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
        else :
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

    def QueryCounterById(self, id : str):
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