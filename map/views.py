from django.shortcuts import render

# Create your views here.
# from home.models import UploadPictureModel
from django.core import serializers
# from home.forms import UploadWellPictureForm
# Create your views here.
def map(request):
  qs ={}
#   qs = UploadPictureModel.objects.all()
  #serialized = serializers.serialize("json", qs)
  #print(serialized[0])
  return render(request,'map/map.html',{'data':qs})

def heir_map(request):
    return render(request,"map/heir_map.html",{})