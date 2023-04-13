from pickle import TRUE
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.core.exceptions import ValidationError
import easygui
import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
#from matplotlib.pyplot import summer
from numpy import average
import datetime

# Create your models here.
class UploadWellPictureModel(models.Model):
    picture = models.ImageField( upload_to='WellPics/', blank=True, null=True, default='WellPics/noImage.jpg')
    name = models.CharField(max_length=100, blank=True, null=True)
    well_nm = models.CharField(max_length=100, blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=8, blank=True, null=True)
    lat = models.CharField(max_length=15)
    lng = models.CharField(max_length=15)
    date = models.DateField(null=True)
    username = models.CharField(max_length=50, blank=True,null=True)
    water_quality = models.CharField(max_length=100, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.picture = self.compressImage(self.picture)
        super(UploadWellPictureModel, self).save(*args, **kwargs)
    def compressImage(self,picture):
        imageTemproary = Image.open(picture)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        picture = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return picture
    class Meta:
       managed = True
       db_table = 'home_uploadwellpicturemodel'

    def __str__(self):
        return self.well_nm
# For registration form

class data_form(models.Model):

    # id = models.IntegerField(primary_key=True) -- It throws an error because postgresql has an property that it generates id automatically, make primary key false
    emailF = models.CharField(max_length=100)
    studentName = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    collegeName = models.CharField(max_length=100)
    websiteUsername = models.CharField(max_length=100)
    sponsered = models.CharField(max_length=3)
    sponsBy = models.CharField(max_length=100)
    ownDevice = models.CharField(max_length=3)
    date = models.CharField(max_length=20)
    # grad_year= models.CharField(max_length=20)
    # grad_stream= models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'app_data_of_form'

    def __str__(self):
        return self.websiteUsername+"- of - "+self.collegeName+" -Institute"

# class data_of_tasks(models.Model):

#     addTasks = models.CharField(max_length=200)
#     percent = models.CharField(max_length=4)
