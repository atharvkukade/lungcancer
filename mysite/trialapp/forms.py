from django import forms
from django.forms import ModelForm
from .models import Image,Doctor,User
from django.db import connection
import os

cursor = connection.cursor()

class ImageUpload(forms.ModelForm):

    class Meta:
        model=Image
        fields=['image',]

    def __init__(self, *args, **kwargs):
        super(ImageUpload, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "btn"

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email address','autofocus':'autofocus'}))
    password = forms.CharField(max_length=200,help_text="Maximum length 200 Chars",widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"



class RegistrationForm(forms.Form):
    firstname = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder': 'Enter First Name','autofocus':'autofocus'}))
    lastname =  forms.CharField(label="Last Name",widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name','autofocus':'autofocus'}))
    dateofbirth = forms.DateField(label="Date Of Birth",widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd','autofocus':'autofocus'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'eg:abc@gmail.com','autofocus':'autofocus'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','autofocus':'autofocus'}))
    phoneNo=forms.IntegerField(label="Mobile Number",help_text="10 Digits only",widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Num','autofocus':'autofocus'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City','autofocus':'autofocus'}))
    state=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State','autofocus':'autofocus'}))

    CHOICES=[('Male','Male'),
             ('Female','Female')]
    gender=forms.ChoiceField(choices=CHOICES)

    CHOICES=[('A+','A+'),
             ('A-', 'A-'),
             ('B+', 'B+'),
             ('B-', 'B-'),
             ('O+', 'O+'),
             ('O-','O-'),
             ('AB+', 'AB+'),
             ('AB-','AB-')]
    bloodgrp=forms.ChoiceField(choices=CHOICES)
    height=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Height','autofocus':'autofocus'}))
    weight=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Weight','autofocus':'autofocus'}))



    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"

class DoctorSelectForm(forms.Form):

    rowCount = cursor.execute('Select u.name,u.city,u.state from user as u , doctor as d where u.userid=d.userid')
    rows = cursor.fetchall()

    CHOICES = list()
    rowCount = 1
    for r in rows:
        currRow = list()
        currRow.append(str(rowCount))
        currRow.append(''.join(str(i)+", " for i in r))
        currRow = tuple(currRow)
        CHOICES.append(currRow)
        rowCount+=1


    doclist=forms.ChoiceField(label="Doctor List",choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(DoctorSelectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"

class DoctorDashForm(forms.Form):

    patientIdHidden = forms.CharField(label="First Name", widget=forms.HiddenInput(attrs={'placeholder': 'Enter First Name','autofocus':'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(DoctorDashForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"

class ReportForm(forms.Form):

    reporttext = forms.CharField(label='Report', widget=forms.Textarea(attrs={'placeholder': 'Write Your Report Here...'}))
    CHOICES = [('Stage-1', 'Stage-1'),
               ('Stage-2', 'Stage-2'),
               ('Stage-3', 'Stage-3'),
               ('Stage-4', 'Stage-4'),]

    stage = forms.ChoiceField(label="Stage of Cancer",choices=CHOICES)
    dateofappointment = forms.DateField(label="Date Of Appointment",widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd','autofocus':'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
            self.fields['dateofappointment'].required = True


class DocGeneratedReport(forms.Form):
    reporttext = forms.CharField(label='Report',widget=forms.Textarea(attrs={'placeholder': 'Write Your Report Here...','readonly':True}))
    dateofappointment = forms.DateField(label="Date Of Appointment", widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd', 'autofocus': 'autofocus','readonly':True}))

    def __init__(self, *args, **kwargs):
        super(DocGeneratedReport, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class FeedbackForm(forms.Form):

    CHOICES = [('5', 'Very Satiesfied'),
               ('4', 'Satiesfied'),
               ('3', 'Neutral'),
               ('2', 'Unsatiesfied'),
               ('1', 'Very Unsatiesfied'),]

    docknowfeedback = forms.ChoiceField(label="Doctor's Knowledge", choices=CHOICES)

    dockindfeedback = forms.ChoiceField(label="Doctor's Kindness", choices=CHOICES)

    waittimefeedback = forms.ChoiceField(label="Waiting Time", choices=CHOICES)

    feedbacktext = forms.CharField(label='Report',widget=forms.Textarea(attrs={'placeholder': 'Write Your Feedback Here...'}))

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
