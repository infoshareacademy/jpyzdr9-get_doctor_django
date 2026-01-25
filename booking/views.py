from .models import Appointment
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class PatientAppointmentsView(ListView):
    model = Appointment
    template_name = 'booking/appointment.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # (brak sesji)
        return (
            Appointment.objects
            .order_by('slot__start_datetime')
        )

# class PatientAppointmentsView(LoginRequiredMixin, ListView):
#     model = Appointment
#     template_name = 'booking/appointment.html'
#     context_object_name = 'appointments'
#
#     def get_queryset(self):
#         return Appointment.objects.filter(patient=self.request.user).order_by('-slot__start_datetime')