from django.urls import path
from .views import register_patient

app_name = 'patients_registration'

urlpatterns = [
    path('register/', register_patient, name='register_patient'),
]
