"""
URL configuration for migrations project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from . import testviews
from . import gptAnswer
urlpatterns = [
    # Add your code here

    path('api/login/', views.LogIn),
    path('api/signUp/', views.SignUpByPatient),
    path('api/departmentList/', views.GetDepartmentList),
    path('api/departmentInfo/', views.GetInfoListByDepartment),
    path('api/registration/', views.PatientRegistration),
    path('api/counterToPay/', views.showAllNeedtoPay),
    path('api/fetchPayList/', views.showAllinCounter),
    path('api/prescribeMedication/', views.PrescribeMedication),
    path('api/payAllCounter/', views.PayAll),
    path('api/showAllDrug/', views.showAllDrug),
    path('api/showAllDrugName/', views.showAllDrugName),
    path('api/medicalDiagnosisStatement/', views.MedicalDiagnosisStatement),
    path('api/getDiagnosisByPid/', views.getDiagnosisByPid),
    path('api/getLaboratorySheetids/', views.getLaboratorySheetids),
    path('api/getLaboratorySheet/', views.getLaboratorySheet),
    path('api/conductLaboratorySheet/', views.conductLaboratorySheet),
    path('api/deletePatient/', views.deletePatient),
    path('api/checkThePosInQueueu/', views.checkThePosInQueueu),
    path('api/showCounterById/', views.showCounterById),
    path('api/getDoctorDispatch/', views.getDoctorDispatch),
    path('api/hardDeleteDrug/', views.hardDeleteDrug),
    path('api/doctorList/', views.GetInfoListByDepartment),
    path("api/confirmdoctor/", views.PatientRegistration),
    path('api/getSuggestion', views.answer),
    path('api/getDiagnosisList/', views.getDiagnosisList),
    path('api/deleteAccount/', views.deletePatient),
    path('api/account', views.account),
    path('api/signin', views.SignUpByPatient),
    path('api/getCheckCombineList', views.getCheckCombineList),
    path('api/getcheckItemList', views.getCheckItemsList),
    path('api/queryDrugInfo', views.queryDrugInfo),
    path('test/showAlluser', views.showAllUser),
    path('test/showRequestJson', testviews.showRequestJson),
    path('test/login', testviews.LogIn),
    path('test/Registration', views.testPatientRegistration),
    path('test/deleteCounter', views.deleteCounter)

]
