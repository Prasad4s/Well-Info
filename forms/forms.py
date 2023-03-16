from django import forms 
from .models import BasicInformationModel #NutrigardenInformationModel, factsheetInformationModel, factsheetDynamicIndicatorsModel, financialExpensesModel, outputIndicatorsModel
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class BasicInformationForm(forms.ModelForm):
    class Meta:
        model = BasicInformationModel
        fields = '__all__'
        
