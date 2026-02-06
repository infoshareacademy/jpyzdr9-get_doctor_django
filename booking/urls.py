from django.urls import path
from .views import PatientAppointmentsView, CancelAppointmentView, AppointmentDetailListView, AppointmentSuccessView, confirm_visit, AppointmentPriceListView

app_name = 'booking'

urlpatterns = [
    path('appointments/', PatientAppointmentsView.as_view(), name='appointment'),
    path('appointments/<int:id>/cancel/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('select-appointment/<int:slot_id>/', AppointmentDetailListView.as_view(), name='select_appointment'),
    path('appointment-success/', AppointmentSuccessView.as_view(), name='appointment_success'),
    path('confirm-visit/<int:slot_id>/', confirm_visit, name='confirm_visit'),
    path('prices-and-services/', AppointmentPriceListView.as_view(), name='prices_and_services'),

]

