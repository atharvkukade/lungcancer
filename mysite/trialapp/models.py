# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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
    docid = models.AutoField(db_column='docId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    specialization = models.CharField(max_length=30, blank=True, null=True)
    experience = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doctor'


class Feedback(models.Model):
    feedbackid = models.AutoField(db_column='feedbackId', primary_key=True)  # Field name made lowercase.
    pateintid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='pateintId', blank=True, null=True)  # Field name made lowercase.
    docid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='docId', blank=True, null=True)  # Field name made lowercase.
    averagerating = models.FloatField(db_column='averageRating', blank=True, null=True)  # Field name made lowercase.
    feedback = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'


class Image(models.Model):
    imageid = models.AutoField(db_column='imageId', primary_key=True)  # Field name made lowercase.
    patientid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patientId', blank=True, null=True)  # Field name made lowercase.
    image = models.ImageField(upload_to='ctimages/',default="\\OriginalImg.JPG")
    totalnoofwhitespots = models.FloatField(db_column='totalNumberOfWhiteSpots', blank=True, null=True)  # Field name made lowercase.
    totalwhitespotarea = models.FloatField(db_column='totalWhiteSpotArea', blank=True, null=True)  # Field name made lowercase.
    totalwhitespotlength = models.FloatField(db_column='totalWhiteSpotLength', blank=True, null=True)  # Field name made lowercase.
    totalwhitearealessthanthirtyfivepixel = models.FloatField(db_column='totalWhiteAreaLessThanThirtyFivePixel', blank=True, null=True)  # Field name made lowercase.
    totalwhiteareagreaterthanthirtyfivepixel = models.FloatField(db_column='totalWhiteAreaGreaterThanThirtyFivePixel', blank=True, null=True)  # Field name made lowercase.
    totalwhiteareagreaterthanhundredpixel = models.FloatField(db_column='totalWhiteAreaGreaterThanHundredPixel', blank=True, null=True)  # Field name made lowercase.
    maxwhitespotarea = models.FloatField(db_column='MaxWhiteSpotArea', blank=True, null=True)  # Field name made lowercase.
    minwhitespotarea = models.FloatField(db_column='MinWhiteSpotArea', blank=True, null=True)  # Field name made lowercase.
    systempredictedstage = models.CharField(db_column='systemPredictedStage', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'image'

class Patient(models.Model):
    patientid = models.AutoField(db_column='patientId', primary_key=True)  # Field name made lowercase.
    docid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='docId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    bloodgroup = models.CharField(db_column='bloodGroup', max_length=2, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=6, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient'


class Report(models.Model):
    reportid = models.AutoField(db_column='reportId', primary_key=True)  # Field name made lowercase.
    imageid = models.ForeignKey(Image, models.DO_NOTHING, db_column='imageId', blank=True, null=True)  # Field name made lowercase.
    patientid = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patientId', unique=True, blank=True, null=True)  # Field name made lowercase.
    docid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='docId', blank=True, null=True)  # Field name made lowercase.
    dateofreportgeneration = models.DateField(db_column='dateOfReportGeneration', blank=True, null=True)  # Field name made lowercase.
    report = models.CharField(max_length=1000, blank=True, null=True)
    appointmentdate = models.DateField(db_column='appointmentDate', blank=True, null=True)  # Field name made lowercase.
    doctorpredictedstage = models.IntegerField(db_column='doctorPredictedStage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'report'


class User(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=32,default="Not Set")
    dateofbirth = models.DateField(db_column='dateOfBirth', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=50, blank=True, null=True)
    phoneno = models.BigIntegerField(db_column='phoneNo', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'
        unique_together = (('email', 'phoneno'),)
