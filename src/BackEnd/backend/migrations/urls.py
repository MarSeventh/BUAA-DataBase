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

    path('api/login/', views.LogIn), # finished
    path('api/signUp/', views.SignUpByPatient), # finished
    path('api/departmentList/', views.GetDepartmentList), # finished
    path('api/departmentInfo/', views.GetInfoListByDepartment), # finished
    path('api/doctorList/', views.GetDoctorListByDepartment),
    path('api/registration/', views.PatientRegistration), # finished
    path('api/counterToPay/', views.showAllNeedtoPay), # finished
    path('api/fetchPayList/', views.showAllinCounter), # finished
    path('api/sendMedicineList/', views.PrescribeMedication), # finished
    path('api/payAllCounter/', views.PayAll), # finished
    path('api/finishPay/', views.finishPay),
    path('api/showAllDrug/', views.showAllDrug), # finished
    path('api/showAllDrugName/', views.showAllDrugName), # finished
    path('api/medicalDiagnosisStatement/', views.MedicalDiagnosisStatement), # finished
    path('api/getDiagnosisByPid/', views.getDiagnosisByPid), # finished
    path('api/getLaboratorySheetids/', views.getLaboratorySheetids), # finished
    path('api/getLaboratorySheet/', views.getLaboratorySheet), # finished
    path('api/conductLaboratorySheet/', views.conductLaboratorySheet), # finished
    path('api/deletePatient/', views.deletePatient), # finished
    path('api/checkThePosInQueueu/', views.checkThePosInQueueu), # finished
    path('api/showCounterById/', views.showCounterById), # finished
    path('api/getDoctorDispatch/', views.getDoctorDispatch), # finished
    path('api/hardDeleteDrug/', views.hardDeleteDrug), # finished
    path('api/doctorList/', views.GetInfoListByDepartment), # finished
    path("api/confirmDoctor/", views.PatientRegistration), # finished
    path('api/getSuggestion/', views.answer),
    path('api/getDiagnosis', views.getDiagnosis),
    path('api/getDiagnosisList/', views.getDiagnosisList),
    path('api/deleteAccount/', views.deletePatient),
    path('api/account/', views.account),
    path('api/signin/', views.SignUpByPatient),
    path('api/getCheckCombineList', views.getCheckCombineList),
    path('api/getcheckItemList', views.getCheckItemsList),
    path('api/queryDrugInfo', views.queryDrugInfo),
    path('test/showAlluser', views.showAllUser), # finished
    path('test/showRequestJson', testviews.showRequestJson), # finished
    path('test/login', testviews.LogIn), # finished
    path('test/Registration', views.testPatientRegistration), # finished
    path('test/deleteCounter', views.deleteCounter), # finished
    path('api/getPatient', views.getPatient), # finished
    path('api/getAnalysisName', views.getAnalysisList), # finished
    path('api/sendAnalysisList/', views.conductLaboratorySheet), # finished
    path('api/sendCheckResults/', views.MedicalDiagnosisStatement), # finished
    path('api/getDoctorSchedule/', views.getDispatch), # finished
    path('api/sendDoctorList/', views.addDoctor), # finished
    path('api/getMedicine/', views.GetAllMedicine), # finished
    path('api/deleteMedicine/', views.deleteMedicine), # finished
    path('api/nextPatient/', views.nextPatient),
    path('api/searchMedicineList/', views.searchMedicine), # finished
    path('api/addPatient/', views.addPatient) # finished

]
