from django.shortcuts import render
from .forms import BasicInformationForm # NutrigardenInformationForm, factsheetInformationForm, factsheetDynamicIndicatorsForm, financialExpensesForm, outputIndicatorsForm
from django.shortcuts import redirect
# Create your views here.
def basicinfo(request):
    if request.method == 'POST':
        form = BasicInformationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            print("data is saved.")
            return redirect('/')
    else:
        form = BasicInformationForm()
    return render(request,'forms/basic_forms.html',{'form':form})
