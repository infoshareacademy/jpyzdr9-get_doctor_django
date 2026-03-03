from .models import Appointment, Service
from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from registrations_visit.models import TimeSlot
from django.contrib.auth.decorators import login_required
from notifications.emails import appointment_confirmation
from .forms import AppointmentDoctorForm



class PatientAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'booking/appointment.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(
            patient=self.request.user
        ).select_related(
            'slot', 'slot__doctor'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        context['upcoming_appointments'] = (
            self.get_queryset()
            .filter(slot__start_datetime__gte=now)
            .order_by('slot__start_datetime')
        )

        context['past_appointments'] = (
            self.get_queryset()
            .filter(slot__start_datetime__lt=now)
            .order_by('-slot__start_datetime')
        )

        return context


class CancelAppointmentView(LoginRequiredMixin, View):
    def post(self, request, id):
        if request.user.is_staff:
            appointment = get_object_or_404(Appointment, pk=id)
        else:
            appointment = get_object_or_404(Appointment, pk=id, patient=request.user)
        slot = appointment.slot
        slot.is_booked = False
        slot.save()
        appointment.delete()
        messages.success(request, "Wizyta została anulowana")
        return redirect('booking:appointment')



class AppointmentDetailListView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/appointment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slot_id = self.kwargs.get('slot_id')
        slot = TimeSlot.objects.get(id=slot_id)
        context['slot'] = slot
        context['services'] = Service.objects.filter(doctor=slot.doctor)
        context['specialization'] = slot.doctor.specialization

        return context

@login_required
def confirm_visit(request, slot_id):
    slot = get_object_or_404(TimeSlot, id=slot_id)
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        appointment = Appointment.objects.create(
            patient=request.user,
            slot=slot,
        )

        appointment_confirmation(request.user, appointment)

        return redirect('booking:appointment_success')
    return redirect('booking:appointment_detail', slot_id=slot.id)


class AppointmentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/appointment_success.html'


class AppointmentPriceListView(TemplateView):
    template_name = 'booking/appointment_prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.select_related('doctor').order_by('doctor__specialization')
        return context



class AppointmentNotesView(ListView):
    template_name = 'booking/appointment_notes.html'
    context_object_name = 'notes'
    queryset = Appointment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentDoctorForm()
        return context

    def post(self, request, *args, **kwargs):
        appointment_id = request.POST.get('appointment_id')
        new_note = request.POST.get('doctor_notes', '').strip()
        if not new_note:
            return redirect('booking:appointment_notes')

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return redirect('booking:appointment_notes')

        if appointment.doctor_notes:
            appointment.doctor_notes += f"\n{new_note}"
        else:
            appointment.doctor_notes = new_note

        appointment.save()
        return redirect('booking:appointment_notes')