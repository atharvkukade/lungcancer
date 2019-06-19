from django.shortcuts import render,redirect
from .models import User,Patient,Doctor,Image,Report,Feedback
from .forms import RegistrationForm,DoctorSelectForm,DoctorDashForm,ReportForm,ImageUpload,LoginForm,DocGeneratedReport,FeedbackForm
from django.contrib import messages
from hashlib import sha1
from django.db import connection
from .imageprocessing import ImageProcessor
from .extractfeatures import FeatureExtractor
from .machinelearning import getPredictedStage
from .recommendation import getdocrecoomedation
import threading


cursor = connection.cursor()


def getsha1hash(plaintext):
    binary_hash = sha1(plaintext.encode('utf-8')).digest()
    hash = ''.join(['%02x' % byte for byte in binary_hash])
    hash = hash[0:32]
    return hash


def homepage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            hash=getsha1hash(password)

            userValid = False
            users = User.objects.all()

            userId=-1
            for usrName in users:
                if username == usrName.email:
                    #return HttpResponse("{{hash}}", "<br>", "{{usrName.password}}")
                    if hash == usrName.password.decode('utf-8'):
                        userValid = True
                        userId=usrName.userid
                        break

            if userId not in (-1,):
                user = User.objects.values().get(userid=userId)
                if userValid is True and user['role'] == 'Patient':

                    messages.info(request, f"You are now logged in as {username}")
                    request.session['userid'] = userId
                    request.session['isPatientFromLogin'] = 'yes'

                    return redirect(
                        "trialapp:patientinfo",
                    )
                elif userValid is True and user['role'] == 'Doctor':
                    messages.info(request, f"You are now logged in as {username}")
                    request.session['userid'] = userId
                    docId = Doctor.objects.values().get(userid=userId)['docid']
                    request.session['doctorid'] = docId
                    return redirect(
                        "trialapp:doctordash",
                    )
            else:
                messages.error(request,f"Invalid username or password")
                print('<strong>Fail</strong>')
                return redirect('trialapp:homepage')


    form=LoginForm
    return render(
        request=request,
        template_name="trialapp/home.html",
        context={"form":form}
    )


def patientinfo(request):

    #Passing userid session variable to render Patient's and User's info
    if 'userid' in request.session:
        users = User.objects.all().get(userid=request.session['userid'])
        patient = Patient.objects.all().get(userid=request.session['userid'])
        image = Image.objects.all().get(patientid = patient.patientid)
        doctor1 = Doctor.objects.all().get(
            docid = Patient.objects.values().get(
                patientid = patient.patientid
            )['docid_id']
        )

    if 'isPatientFromLogin' in request.session:
        if request.session['isPatientFromLogin'] == 'yes':
            doctor = User.objects.get(
                userid=Doctor.objects.values().get(
                docid=Patient.objects.values().get(
                patientid=Patient.objects.values().get(
                userid=int(request.session['userid']))['patientid'])['docid_id'])['userid_id'])

            request.session['patientid'] = patient.patientid
            print("Patient", patient.patientid)
            request.session['doctorid'] = doctor1.docid
            print("Doctor", doctor1.docid)

        elif request.session['isPatientFromLogin'] == 'no':
            doctorid = int(request.session['doctorid'])
            doctor = User.objects.get(
                userid = Doctor.objects.values().get(
                    docid = doctorid
                )['userid_id']
            )



        isReportGenerated = False
        docreport = None

        try:
            docreport = Report.objects.get(patientid=patient.patientid, imageid=image.imageid, docid=doctor1.docid)
            isReportGenerated = True
            print('hell01')
        except Report.DoesNotExist:
            print('Report not generated...')

        docreportform=None
        if isReportGenerated is True:
            docreportform = DocGeneratedReport(initial={'reporttext':docreport.report,'dateofappointment':docreport.appointmentdate})

        return render(
            request=request,
            template_name='trialapp/patientinfo.html',
            context={"User":users,"Patient":patient,"Doctor":doctor,"Docreport":docreportform}
        )

def register(request):

    if request.method == "POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('firstname') +' '+form.cleaned_data.get('lastname')
            password = getsha1hash(form.cleaned_data.get('password'))
            dateofbirth = form.cleaned_data.get('dateofbirth')
            email=form.cleaned_data.get('email')
            phoneno=form.cleaned_data.get('phoneNo')
            city=form.cleaned_data.get('city')
            state=form.cleaned_data.get('state')
            role='Patient'
            bloodgrp=form.cleaned_data.get('bloodgrp')
            gender=form.cleaned_data.get('gender')
            weight=form.cleaned_data.get('weight')
            height=form.cleaned_data.get('height')

            #Sql query to insert data into user and patient table
            rowsupdated=cursor.execute('insert into user(name,password,dateofbirth,email,phoneno,city,state,role) values(%s,%s,%s,%s,%s ,%s,%s,%s);',(name,password,dateofbirth,email,phoneno,city,state,role))
            userid=User.objects.values('userid').get(email=email)['userid']

            if rowsupdated > 0:
                rowsupdated=cursor.execute('insert into patient(userid,bloodgroup,gender,weight,height) values(%s,%s,%s,%s,%s)',(userid,bloodgrp,gender,weight,height))
                patientid=Patient.objects.values('patientid').get(userid=userid)['patientid']
                if rowsupdated > 0:
                    connection.commit()
                    request.session['userid'] = userid
                    request.session['patientid']=patientid
                    return redirect(
                        "trialapp:imageupload",
                    )
            else:
                connection.rollback()
        return render(
            request=request,
            template_name='trialapp/register.html',
            context={"form":form}
        )

    form=RegistrationForm
    return render(
        request=request,
        template_name='trialapp/register.html',
        context={"form":form}
    )

def recommenddoc(patientid,request):

    docuserid = getdocrecoomedation(connection,patientid)
    request.session['recomdocid'] = docuserid



def imageuploadform(request):

    form = ImageUpload(request.POST, request.FILES)

    if form.is_valid():
        if 'userid' in request.session:
            patientid = request.session['patientid']

        instance = form.save(commit=False)
        instance.patientid = Patient.objects.get(patientid=patientid)
        instance.save()

def imageupload(request):

    if request.method=="POST":

        t1 = threading.Thread(target=imageuploadform(request))

        if 'patientid' in request.session:
            patientid = int(request.session['patientid'])

        t2 = threading.Thread(target=recommenddoc(patientid,request))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        return redirect("trialapp:docrecomm")


    form=ImageUpload
    return render(
        request=request,
        template_name="trialapp/imageupload.html",
        context={"form":form}
    )

def processImage(patientId):

    cursor.execute('Select image from image where patientid=%s',(patientId,))
    imagepath = cursor.fetchall()[0][0].decode('utf-8')

    i = ImageProcessor()
    tumourspots = i.getTumourSpots(imagepath)

    f = FeatureExtractor()
    features = f.extractfeaturs(tumourspots)

    print(features)

    cursor.execute('update image set totalNumberOfWhiteSpots=%s , totalWhiteSpotArea=%s,totalWhiteSpotLength=%s,totalWhiteAreaLessThanThirtyFivePixel=%s,totalWhiteAreaGreaterThanThirtyFivePixel=%s,totalWhiteAreaGreaterThanHundredPixel=%s,MaxWhiteSpotArea=%s,MinWhiteSpotArea=%s where patientid=%s;',(
    features['totalNumOfWhiteSpots'],
    features['totalWhiteSpotArea'],
    features['totalWhiteSpotLength'],
    features['totalPixelsLessThanThirtyFive'],
    features['totalPixelsGreaterThanThirtyFive'],
    features['totalPixelsGreaterThanHundred'],
    features['MaxWhiteSpotArea'],
    features['MinWhiteSpotArea'],
    patientId))

    systemPredictedStage = getPredictedStage(features)

    cursor.execute('update image set systemPredictedStage=%s where patientid=%s',(systemPredictedStage,patientId))

def docrecommform(request):

    form = DoctorSelectForm(request.POST)

    if form.is_valid():

        doclist = form.cleaned_data.get('doclist')

        if 'patientid' in request.session:
            patientid = request.session['patientid']
            rowsupdated = cursor.execute('update patient set docId=%s where patientid=%s;', (doclist, patientid))
            if rowsupdated > 0:
                request.session['doctorid'] = doclist
                request.session['isPatientFromLogin'] = 'no'
                print('Successfully Updated!!!')


def docrecomm(request):

    if 'recomdocid' in request.session:
        recommededDocId = int(request.session['recomdocid'])
        user = User.objects.all().get(userid=recommededDocId)


    if request.method == 'POST':

        t1 = threading.Thread(target=docrecommform(request))

        if 'patientid' in request.session:
            patientid = (request.session['patientid'])

        t2 = threading.Thread(target=processImage(patientid))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        return redirect("trialapp:patientinfo")

    form = DoctorSelectForm
    return render(
        request=request,
        template_name="trialapp/docrecomm.html",
        context={"form":form,"Doctor":user}
    )

def doctordash(request):

    if 'doctorid' in request.session:
        docid = request.session['doctorid']
        rows = cursor.execute('select i.patientid , i.systemPredictedStage from image as i where i.patientId in (select patientid from patient where docId=%s);',(docid,))
        rows = cursor.fetchall()

        finalRows = list()
        startPos = 0
        endPos = 0
        i = 0

        for i in range(1,((int(len(rows)/4)))+1):
            startPos = endPos
            endPos = 4 * i
            finalRows.append(rows[startPos:endPos])

        if (len(rows) % 4) != 0:
            finalRows.append(rows[endPos:(endPos+(len(rows) % 4))])



    if request.method == 'POST':
        form = DoctorDashForm(request.POST)

        request.session['patientid'] = request.POST['patientId1']

        return redirect("trialapp:report")


    form = DoctorDashForm
    return render(
        request=request,
        template_name="trialapp/docdash.html",
        context={"Patients":finalRows}
    )

def report(request):

    if 'patientid' in request.session:
        patientid = int(request.session['patientid'])

        patient = Patient.objects.get(patientid=patientid)

        image = Image.objects.all().get(patientid=patientid)

        user = User.objects.get(
            userid = Patient.objects.values().get(
                patientid = patientid
            )['userid_id']
        )

        doctor = Doctor.objects.get(
             docid = Patient.objects.values().get(
                 patientid = patientid
             )['docid_id']
        )

        isReportGenerated = False
        docreport = None

        try:
            docreport = Report.objects.get(patientid=patientid,imageid=image.imageid,docid=doctor.docid)
            isReportGenerated = True
            print('hell01')
        except Report.DoesNotExist:
            print('Report not generated...')

    submitclickcount = 0
    if request.method == "POST":

        form = ReportForm(request.POST)

        if isReportGenerated is True:
            print('hell02')
            form = ReportForm(request.POST,initial={'reporttext':docreport.report})

        if form.is_valid():

            reportText = form.cleaned_data.get('reporttext')
            appointmentdate = form.cleaned_data.get('dateofappointment')

            if isReportGenerated is False:
                rowsupdated = cursor.execute('insert into report(imageId,patientId,docId,dateOfReportGeneration,appointmentDate,report) values(%s,%s,%s,curdate(),%s,%s);',(image.imageid,patient.patientid,doctor.docid,appointmentdate,reportText))
                if rowsupdated > 0:
                    print('Report inserted successfully!!!')
            else:
                rowsupdated=cursor.execute('update report set report=%s where imageId=%s and patientId=%s and docId=%s',(reportText,image.imageid,patientid,doctor.docid))
                if rowsupdated > 0:
                    print('Report Updated Successfully!!!')

        return render(
            request=request,
            template_name="trialapp/report.html",
            context={"Image":image , "Patient":patient , "User":user,"form":form}
        )

    if isReportGenerated is True:
        form = ReportForm(request.POST, initial={'reporttext': docreport.report})
    else:
        form = ReportForm

    return render(
        request=request,
        template_name="trialapp/report.html",
        context={"Image":image , "Patient":patient , "User":user , "form":form}
    )

def feedback(request):

    # Each user allowed to give feedback only once
    # So checking if feedback was already given by the user or not
    isFeedbackGiven = False

    if 'patientid' in request.session and 'doctorid' in request.session:
        patientid = request.session['patientid']
        doctorid = request.session['doctorid']

        print('In Feedback PatId ',patientid)
        print('In Feedback DocId',doctorid)

        try:
            feedback = Feedback.objects.all().get(pateintid=patientid, docid=doctorid)
            isFeedbackGiven = True
        except Feedback.DoesNotExist:
            print('Feedback is not given...')

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():

            rating1 = int(form.cleaned_data.get('docknowfeedback'))
            rating2 = int(form.cleaned_data.get('dockindfeedback'))
            rating3 = int(form.cleaned_data.get('waittimefeedback'))
            averageRating = (rating1+rating2+rating3) / 3

            feedback = form.cleaned_data.get('feedbacktext')

            if isFeedbackGiven != True:
                rowsupdated = cursor.execute('insert into feedback(pateintId,docId,averageRating,feedback) values(%s,%s,%s,%s)',(patientid, doctorid, averageRating, feedback))
                if rowsupdated > 0:
                    print('Feedback Inserted Successfully!')

                isFeedbackGiven = True

            return render(
                request = request,
                template_name='trialapp/feedback.html',
                context={'form':form, "isFeedbackGiven":isFeedbackGiven }
            )

    form = FeedbackForm
    return render(
        request=request,
        template_name='trialapp/feedback.html',
        context={'form':form,"isFeedbackGiven":isFeedbackGiven}
    )
