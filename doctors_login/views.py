from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView, View, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import DoctorProfileForm
from booking.models import Appointment
import logging
from booking.forms import AppointmentDoctorForm

logger = logging.getLogger(__name__)
User = get_user_model()


class DoctorLoginView(FormView):
    template_name = 'doctors_login/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('doctor:start')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if str(request.user.role).lower() == 'doctor':
                return redirect('doctor:start')
            else:
                return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"Login attempt: username={user.username}, role={user.role}")
        if str(user.role).lower() == 'doctor':
            login(self.request, user)
            logger.info(f'Doctor login successful: {user.username} ({user.pk})')
            return super().form_valid(form)
        else:
            logger.warning(f'Non-doctor login attempt: {user.username} ({user.role})')
            messages.error(self.request, 'To konto nie jest kontem lekarza.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f'Failed login attempt: {self.request.POST.get("username")}')
        messages.error(self.request, 'Nieprawidłowy login lub hasło.')
        return super().form_invalid(form)


class DoctorLogoutView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        logger.info(f'Doctor {user.username} logged out')
        messages.info(request, 'Zostałeś wylogowany.')
        return redirect('doctor:login')


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'doctors_login/start.html'
    login_url = reverse_lazy('doctor:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and str(request.user.role).lower() != 'doctor':
            messages.error(request, 'Brak dostępu do panelu lekarza.')
            return redirect('doctor:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.request.user
        return context


class DoctorProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'doctors_login/profile.html'
    login_url = reverse_lazy('doctor:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and str(request.user.role).lower() != 'doctor':
            messages.error(request, 'Brak dostępu')
            return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.request.user
        context['title'] = 'Profil lekarza'
        return context


class DoctorProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'doctors_login/profile_edit.html'
    model = User
    form_class = DoctorProfileForm
    login_url = reverse_lazy('doctor:login')
    success_url = reverse_lazy('doctor:profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and str(request.user.role).lower() != 'doctor':
            messages.error(request, 'Brak dostępu')
            return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edycja profilu lekarza'
        context['doctor'] = self.request.user
        return context

    def form_valid(self, form):
        logger.info(f'Doctor {self.request.user.username} updated profile')
        messages.success(self.request, 'Profil zaktualizowany pomyślnie!')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f'Doctor {self.request.user.username} profile update failed')
        messages.error(self.request, 'Proszę poprawić błędy w formularzu.')
        return super().form_invalid(form)


class DoctorVisitsView(LoginRequiredMixin, TemplateView):
    template_name = 'doctors_login/office.html'
    login_url = reverse_lazy('doctor:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and str(request.user.role).lower() != 'doctor':
            messages.error(request, 'Brak dostępu')
            return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        today = timezone.localdate()
        doctor = self.request.user

        all_appointments = (
            Appointment.objects
            .filter(slot__doctor=doctor)
            .select_related('patient', 'slot')
            .order_by('slot__start_datetime')
        )

        status = self.request.GET.get('status', 'all')
        if status == 'upcoming':
            visits = all_appointments.filter(slot__start_datetime__gte=now)
        elif status == 'done':
            visits = all_appointments.filter(slot__start_datetime__lt=now)
        elif status == 'cancelled':
            visits = all_appointments.none()
        else:
            visits = all_appointments

        visits_today = all_appointments.filter(
            slot__start_datetime__date=today
        )

        context['doctor'] = doctor
        context['today'] = today
        context['status'] = status
        context['visits'] = visits
        context['visits_today'] = visits_today
        context['now'] = now

        return context


class DoctorAppointmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'doctors_login/appointment_detail.html'
    login_url = reverse_lazy('doctor:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and str(request.user.role).lower() != 'doctor':
            messages.error(request, 'Brak dostępu')
            return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get_appointment(self):
        return get_object_or_404(
            Appointment,
            pk=self.kwargs.get('pk'),
            slot__doctor=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        appointment = self.get_appointment()

        past_appointments = (
            Appointment.objects
            .filter(
                patient=appointment.patient,
                slot__doctor=self.request.user,
                slot__start_datetime__lt=appointment.slot.start_datetime
            )
            .select_related('slot')
            .order_by('-slot__start_datetime')[:10]
        )

        context['doctor'] = self.request.user
        context['appointment'] = appointment
        context['past_appointments'] = past_appointments
        context['form'] = AppointmentDoctorForm(instance=appointment)

        return context

    def post(self, request, *args, **kwargs):
        appointment = self.get_appointment()
        form = AppointmentDoctorForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            messages.success(request, "Notatka zapisana.")
            return redirect('doctor:appointment_detail', pk=appointment.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)