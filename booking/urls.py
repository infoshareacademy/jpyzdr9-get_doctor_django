from django.urls import path
# from .views import AppointmentListView
from .views import PatientAppointmentsView

urlpatterns = [
    path('appointment/', PatientAppointmentsView.as_view(), name='appointment'),
]