# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Checkcombine(models.Model):
    id = models.CharField(primary_key=True,
                          max_length=25)  # The composite primary key (id, itemId) found, that is not supported. The first column is selected.
    itemid = models.ForeignKey('Checkitems', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    checkname = models.CharField(db_column='checkName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'checkcombine'
        unique_together = (('id', 'itemid'),)


class Checkitems(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    price = models.FloatField()
    description = models.CharField(max_length=255)
    minresult = models.FloatField(db_column='MinResult')  # Field name made lowercase.
    maxresult = models.FloatField(db_column='MaxResult')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'checkitems'


class Counter(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    pid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='Pid')  # Field name made lowercase.
    did = models.ForeignKey('Doctor', models.DO_NOTHING, db_column='Did')  # Field name made lowercase.
    ispaid = models.IntegerField(db_column='isPaid')  # Field name made lowercase.
    price = models.FloatField(blank=True, null=True)
    date = models.DateField(db_column='DATE')  # Field name made lowercase.
    type = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'counter'


class Diagnosis(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    patientid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patientId')  # Field name made lowercase.
    doctorid = models.ForeignKey('Doctor', models.DO_NOTHING, db_column='doctorId')  # Field name made lowercase.
    diagnosis = models.TextField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'diagnosis'


class Dispatcher(models.Model):
    timeperiod = models.CharField(db_column='TimePeriod', primary_key=True,
                                  max_length=25)  # Field name made lowercase. The composite primary key (TimePeriod, ROOMID) found, that is not supported. The first column is selected.
    roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='ROOMID')  # Field name made lowercase.
    doctorid = models.ForeignKey('Doctor', models.DO_NOTHING, db_column='doctorId', blank=True,
                                 null=True)  # Field name made lowercase.
    titleid = models.CharField(db_column='TitleId', max_length=25, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dispatcher'
        unique_together = (('timeperiod', 'roomid'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctor(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    tid = models.ForeignKey('Titles', models.DO_NOTHING, db_column='Tid')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'doctor'


class Drug(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    name = models.CharField(max_length=25)
    price = models.FloatField()
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    isbanned = models.IntegerField(db_column='isBanned')  # Field name made lowercase.
    storage = models.FloatField(db_column='Storage')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'drug'


class Laboratorysheet(models.Model):
    id = models.OneToOneField(Counter, models.DO_NOTHING, db_column='id',
                              primary_key=True)  # The composite primary key (id, itemID) found, that is not supported. The first column is selected.
    checkname = models.CharField(db_column='checkName', max_length=255)  # Field name made lowercase.
    begintime = models.DateTimeField(db_column='beginTime')  # Field name made lowercase.
    outputtime = models.DateTimeField(db_column='OutputTime', blank=True, null=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Checkitems, models.DO_NOTHING, db_column='itemID')  # Field name made lowercase.
    result = models.FloatField()

    class Meta:
        managed = False
        db_table = 'laboratorysheet'
        unique_together = (('id', 'itemid'),)


class Medicinepurchase(models.Model):
    id = models.OneToOneField(Counter, models.DO_NOTHING, db_column='id',
                              primary_key=True)  # The composite primary key (id, drugId) found, that is not supported. The first column is selected.
    drugid = models.ForeignKey(Drug, models.DO_NOTHING, db_column='drugId')  # Field name made lowercase.
    amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'medicinepurchase'
        unique_together = (('id', 'drugid'),)


class Patient(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    iscommem = models.IntegerField(db_column='isComMem')  # Field name made lowercase.
    idcard = models.CharField(db_column='idCard', max_length=25, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient'


class Registrelation(models.Model):
    id = models.OneToOneField(Counter, models.DO_NOTHING, db_column='id', primary_key=True)
    roomid = models.CharField(db_column='ROOMID', max_length=25)  # Field name made lowercase.
    isfinished = models.IntegerField(db_column='isFinished')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registrelation'


class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    isoccupied = models.IntegerField(db_column='isOccupied')  # Field name made lowercase.
    queuelen = models.IntegerField(db_column='QueueLen')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'room'


class Titles(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'titles'

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    username = models.CharField(db_column='USERNAME', max_length=25, unique=True)  # Field name made lowercase.
    password = models.CharField(max_length=25)
    type = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'user'
