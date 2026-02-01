from django.urls import path
from .views import PatientAppointmentsView, CancelAppointmentView, AppointmentDetailListView, AppointmentSuccessView, confirm_visit, AppointmentPriceListView

app_name = 'booking'

urlpatterns = [
    path('wizyty/', PatientAppointmentsView.as_view(), name='appointment'),
    path('wizyty/<int:id>/anuluj/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('wybierz-wizyte/<int:slot_id>/', AppointmentDetailListView.as_view(), name='wybierz_wizyte'),
    path('potwierdzenie/', AppointmentSuccessView.as_view(), name='appointment_success'),
    path('potwierdz-wizyte/<int:slot_id>/', confirm_visit, name='confirm_visit'),
    path('cennik-i-uslugi/', AppointmentPriceListView.as_view(), name='prices_and_services'),

]

