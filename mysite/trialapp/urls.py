"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "trialapp"

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("patientinfo/",views.patientinfo,name="patientinfo"),
    path("doctordash/",views.doctordash,name="doctordash"),
    path("doctordash/report",views.report,name="report"),
    path("register/",views.register,name="register"),
    path("register/imageupload/",views.imageupload,name="imageupload"),
    path("register/imageupload/docrecomm",views.docrecomm,name="docrecomm"),
    path("patientinfo/feedback",views.feedback,name="feedback"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

