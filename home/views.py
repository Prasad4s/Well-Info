from cmath import log
from django.core.exceptions import TooManyFieldsSent
from django.shortcuts import render , redirect, get_object_or_404
from .forms import CreateUserForm
import re
# from django.core.files import 
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import base64
import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from django.http import HttpResponse
import csv



#login dependacies
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UploadWellPictureForm
from .models import  UploadWellPictureModel
# Create your views here.
from django.template.defaultfilters import filesizeformat
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.db.models.functions import TruncMonth 
from django.db.models import Sum, Avg ,Max

from django.views import View

# Create your views here.

def viewWells(request):
    wells = UploadWellPictureModel.objects.all()
    context = {'wells': wells}
    return render(request, 'home/viewWells.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def captwellpic(request):
    form = UploadWellPictureForm()
    global datauri
    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        datauri = request.POST['picture']
    
    if request.method == 'POST' and not request.META.get('HTTP_X_REQUESTED_WITH'):
    # if request.method == 'POST':
    # if user is authenticated, use their username
                       
        form = UploadWellPictureForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if not request.user.is_authenticated:
                obj.username = "Guest"
            else:
                obj.username = request.user.username
            # obj.save()
        name = request.POST.get('name')
        well_nm = request.POST.get('well_nm')
        radius = request.POST.get('radius')
        depth = request.POST.get('depth')
        level = request.POST.get('level')
        village = request.POST.get('village')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        date= request.POST.get('date')
        water_quality = request.POST.get('water_quality')
        try:
            imgstr = re.search(r'base64,(.*)', datauri).group(1)
            data = ContentFile(base64.b64decode(imgstr))
            myfile = "WellPics/profile-"+time.strftime("%Y%m%d-%H%M%S")+".png"
            fs = FileSystemStorage()
            filename = fs.save(myfile, data)
            picLocation = UploadWellPictureModel.objects.create(picture=filename, name=name, well_nm=well_nm, radius=radius, depth=depth, level=level, village=village, district=district, state=state,pincode=pincode, lat=lat, lng=lng, date=date, username=obj.username, water_quality =water_quality)
            picLocation.save()
            datauri= False
            del datauri
        except NameError:
            print("Image is not captured")
    else:
        form = UploadWellPictureForm()
    return render(request,'home/captureWellPic.html',{})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def uploadwellpic(request):
    if request.method == 'POST':
        form = UploadWellPictureForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('/captwellpic')
    else:
        form = UploadWellPictureForm()
    return render(request,'home/uploadWellPic.html',{})

def contact(request):
    return render(request,"home/contact.html",{})

def about(request):
    return render(request,"home/about.html",{})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, "You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="home/login.html", context={"login_form":form})

def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

def register_request(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
            return redirect('login')
    context = {'form':form}
    return render(request, "home/register.html", context)

def well_info(request):
    welldata = UploadWellPictureModel.objects.all().order_by('id')
    
    # check if a search query was submitted
    if request.GET.get('search'):
        # get the search query from the submitted form
        search_query = request.GET.get('search')
        
        # filter the welldata queryset to only include results containing the search query
        welldata = welldata.filter(well_nm__icontains=search_query)
        
        # create a message to display the search results
        message = f"Search results for '{search_query}':"
        
    else:
        # set message to None if no search query was submitted
        message = None
    
    context = {
        'welldata': welldata,
        'message': message,
    }
    # well_data= UploadWellPictureModel.objects.all().order_by('id')
    # date = []
    # level = []
    # for data in well_data:
    #     date.append(str(data.date))
    #     level.append(data.level)
    # context = {
    #     'dates': date,
    #     'level': level,
    # }
    
    return render(request, 'home/well_info.html', context)#context

def graph_well(request):
    well_data= UploadWellPictureModel.objects.all().order_by('date')   
    date = []
    level = []
    highest_level = []
    monthly_data = well_data.annotate(month=TruncMonth('date')).values('month').annotate(level_avg=Avg('level'),level_max=Max('level'))
    for data in monthly_data:
        if data['month'] is not None:
            date.append(data['month'].strftime('%B %Y'))
        else:
            date.append('')
        level.append(str(data['level_avg']))
        highest_level.append(str(data['level_max']))
    context = {
        'dates': date,
        'level': level,
        'highest_level': highest_level,
    }
    # water_level_data = {}
    # for data in well_data:
    #     date = data.date.strftime("%Y-%m")
    #     if date in water_level_data:
    #         water_level_data[date].append(data.level)
    #     else:
    #         water_level_data[date] = [data.level]
    # for date, levels in water_level_data.items():
    #     water_level_data[date] = sum(levels) / len(levels)
    # return render(request, 'home/graph_well.html',{'water_level_data':water_level_data})

    return render(request, 'home/graph_well.html',context)

def view_entered_details(request):
    username = request.user.username
    # Retrieve the record from the database based on the user who is currently logged in
    uploaded_pics = UploadWellPictureModel.objects.filter(username=username)
    
    context = {
        'uploaded_pics': uploaded_pics
    }
    return render(request, 'home/view_entered_details.html',context)

def edit_well_picture(request, pk):
    well_picture = get_object_or_404(UploadWellPictureModel,pk=pk, username=request.user.username)
    
    # form= None 

    if request.method == 'POST':
        form = UploadWellPictureForm(request.POST, instance=well_picture)
        if form.is_valid():
            

            well_picture = form.save(commit=False)
            well_picture.username = request.user.username
            
            well_picture.save()
            messages.success(request, 'Well picture updated successfully')
            return redirect('view_entered_details')
    else:
        # messages.error(request, 'There was an error in the form. Please correct it.')
        form = UploadWellPictureForm(instance=well_picture)

    context = {
        'form': form ,
        'well_picture': well_picture,
    }

    return render(request, 'home/edit_well_picture.html', context)