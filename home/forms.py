from django.db.models import fields
from .models import UploadWellPictureModel,data_form
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db import models

class UploadWellPictureForm(forms.ModelForm):
    class Meta:
        model = UploadWellPictureModel
        fields = ('picture','name','well_nm','radius','depth','level','village','district','state','pincode', 'lat', 'lng','date','username', 'water_quality')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class dataForm(forms.ModelForm):
    class Meta:
        model = data_form
        fields = '__all__' 