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
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/Login/', views.LogIn),
    path('api/SignUp/', views.SignUpByPatient),
    path('api/DepartmentList/', views.GetDepartmentList),
    path('api/DepartmentInfo/', views.GetInfoListByDepartment),
    path('api/Registration/', views.PatientRegistration),
    path('api/CounterToPay/', views.showAllNeedtoPay),
    path('api/Counters/', views.showAllinCounter),
    path('api/PrescribeMedication/', views.PrescribeMedication),
    path('api/PayAllCounter/', views.PayAll),
    path('api/showAllDrug/', views.showAllDrug),
    path('api/showAllDrugName/', views.showAllDrugName),
    path('api/MedicalDiagnosisStatement/', views.MedicalDiagnosisStatement),
    path('api/getDiagnosisByPid/', views.getDiagnosisByPid),
    path('api/getLaboratorySheetids/', views.getLaboratorySheetids),
    path('api/getLaboratorySheet/', views.getLaboratorySheet),
    path('api/conductLaboratorySheet/', views.conductLaboratorySheet),
    path('api/deletePatient/', views.deletePatient),
    path('api/checkThePosInQueueu/', views.checkThePosInQueueu),
    path('api/showCounterById/', views.showCounterById),
    path('api/getDoctorDispatch/', views.getDoctorDispatch),
    path('api/hardDeleteDrug/', views.hardDeleteDrug),
]
