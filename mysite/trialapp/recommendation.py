#Here we assumed that at least one doctor have same state as that of
#Becoz we will not able to calculate actual geographical distance unless we use google's distance matrix

from .models import Patient,User,Doctor,Feedback

def getdocrecoomedation(cursor,patientid):
    userid=Patient.objects.values('userid').get(patientid=patientid)['userid']
    patientinfo = User.objects.values().get(userid=userid)

    docwithsamestate = User.objects.filter(state=patientinfo['state'],role="Doctor").values()

    if docwithsamestate.count() > 0:
        docwithsamecity = User.objects.filter(state=patientinfo['state'],city=patientinfo['city'],role="Doctor").values()

        if docwithsamecity.count()>0 :
            if len(docwithsamecity) > 1:

                maxAverageRating = 0
                maxFeedbackDocsUserId = 0

                for doc in docwithsamecity:
                    docid = Doctor.objects.all().get(
                            userid=doc['userid']).docid

                    docratings = Feedback.objects.filter(docid=docid).values()
                    totalrating = 0

                    for rating in docratings:
                        totalrating += int(rating['averagerating'])

                    avgrating = totalrating/len(docratings)

                    if maxAverageRating < avgrating:
                        maxAverageRating = avgrating
                        maxFeedbackDocsUserId = doc['userid']

                return maxFeedbackDocsUserId

            else:
                return docwithsamecity[0]['userid']


        if len(docwithsamestate) > 1:
            maxAverageRating = 0
            maxFeedbackDocsUserId = 0

            for doc in docwithsamestate:
                docid = Doctor.objects.all().get(
                    userid=doc['userid']).docid

                docratings = Feedback.objects.filter(docid=docid).values()
                totalrating = 0

                for rating in docratings:
                    totalrating += int(rating['averagerating'])

                avgrating = totalrating / len(docratings)

                if maxAverageRating < avgrating:
                    maxAverageRating = avgrating
                    maxFeedbackDocsUserId = doc['userid']

            return maxFeedbackDocsUserId

        else:
            return docwithsamestate[0]['userid']

