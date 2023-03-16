from django.contrib import admin

# Register your models here.

from .models import BasicInformationModel # NutrigardenInformationModel, factsheetInformationModel, factsheetDynamicIndicatorsModel, financialExpensesModel, outputIndicatorsModel
admin.site.register(BasicInformationModel)