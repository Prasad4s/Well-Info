from django.contrib import admin

# Register your models here.

from .models import UploadWellPictureModel,data_form
admin.site.register(UploadWellPictureModel)
admin.site.register(data_form)