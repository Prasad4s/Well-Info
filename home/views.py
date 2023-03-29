from cmath import log
from django.core.exceptions import TooManyFieldsSent
from django.shortcuts import render , redirect, get_object_or_404,HttpResponseRedirect
from .forms import CreateUserForm,dataForm
from .models import data_form
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
				messages.info(request, "You are logged in.")
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

#for registration form
# Create your views here.
def loginForm(req):
      if req.method == 'POST': 
            username = req.POST['unL']
            password = req.POST['pwL']
            logStudent = auth.authenticate(username=username, password=password)
            if logStudent is None:
                  print(username +" Username not found.")
                  messages.warning(req, "Username not found.")
                  return redirect('loginForm')
            else:
                  print(username+"Login successful.")
                  messages.success(req,"Login successful.")
                  return render(req, 'home/form.html')
      return render(req, 'home/loginF.html')
      
def registerForm(req):
    context ={}
    context['form']= dataForm()
    # return render(req, "home/registerF.html", context)
    if req.method == 'POST':
        for key, value in req.POST.items():
            print('Key: %s' % (key) ) 
    # print(f'Key: {key}') in Python >= 3.7
            print('Value %s' % (value) )
    # print(f'Value: {value}') in Python >= 3.7
        email = req.POST['emailF']
        username = req.POST['websiteUsername']
        studentName =req.POST['studentName']
        age =req.POST['age']
        collegeName =req.POST['collegeName']
        websiteUsername =req.POST['websiteUsername']
        sponsered =req.POST['sponsered']
        sponsBy =req.POST['sponsBy']
        
        
        if  data_form.objects.filter(emailF=email).exists():
                    messages.warning(req, _(u'This Email has been registered. '))        
        elif  data_form.objects.filter(websiteUsername=username).exists():
                messages.warning(req,"Username already exists.")
        
        else:
                
                form = dataForm(req.POST)
                if form.is_valid():
                                          
                    form.save()
                    print("User Registered Successfully.")
                else:
                    form.errors.as_json()
                    print(form.errors)
                    messages.error(req, _(u"Please check the form."))
                # messages.info(req,"User Registered Successfully.")
        return HttpResponseRedirect(req.path_info)
    else:
        context ={}
        context['form']= dataForm()
        return render(req, "home/registerF.html", context)    
    return render(req,'home/registerF.html')      


def form(req):
    for key, value in req.POST.items():
                print('Key: %s' % (key) ) 
                print('Value %s' % (value) )
    user = req.user
    # mail = req.email
    username = user.username
    emailid = user.email
    print(username,emailid)
    # request_dict = vars(req)
    # print(request_dict)
    # print(req)
    if req.method == 'POST':
            emailF = username
            studentName = req.POST['sname']
            age = req.POST['age']
            websiteUsername = emailid
            collegeName = req.POST['cname']
            sponsered = req.POST['sponsered']
            sponsBy = req.POST['sponsBy']
            ownDevice = req.POST['ownDevice']
            date = req.POST['datE']  
            
            # form = dataForm(req.POST)
            totalData = data_form(emailF=emailF,studentName=studentName,age=age,collegeName=collegeName,websiteUsername=websiteUsername,sponsered=sponsered,sponsBy=sponsBy,ownDevice=ownDevice,date=date)
            # print(studentName)
            if  data_form.objects.filter(emailF=emailF).exists():
                    messages.warning(req, _(u'This Email has been registered. '))        
                    return HttpResponseRedirect(req.path_info)
            elif  data_form.objects.filter(websiteUsername=websiteUsername).exists():
                messages.warning(req,"Username already exists.")
                return HttpResponseRedirect(req.path_info)
            else:
                totalData.save()
                messages.info(req,"Student succesfully registered.")
                return render(req, 'home/viewWells.html')
                
    return render(req, 'home/form.html')

def add_tasks (req) :
      # if req.method == 'POST':
      #       addTasks = req.POST['addTasks'] 
      #       percent = req.POST['percent']

      #       taskData = data_of_tasks(addTasks=addTasks,percent=percent)
      #       taskData.save()
      return render(req,'home/add_tasks.html')

def home(req):
    return render(req,'home/homeF.html')
