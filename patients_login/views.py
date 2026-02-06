from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView, UpdateView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .forms import PatientProfileForm
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)

User = get_user_model()


class PatientLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'patients_login/login.html'
    success_url = reverse_lazy('visit:home_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('visit:home_page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"User login: username={user.username}, email={user.email}, id={user.id}")
        if user.role == 'patient':
            login(self.request, user)
            logger.info(f'Patient login successful: {user.username} ({user.pk})')
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                'To konto nie jest kontem pacjenta.'
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f'Failed login attempt: {self.request.POST.get("username")}')
        messages.error(
            self.request,
            'Nieprawidłowy login lub hasło.'
        )
        return super().form_invalid(form)


class PatientLogoutView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        logger.info(f'Patient {user.username} logout')
        messages.info(request, 'Zostałeś wylogowany.')
        return redirect('patient:login')


class PatientProfileView(LoginRequiredMixin, UpdateView):
    form_class = PatientProfileForm
    template_name = 'patients_login/patient_profile.html'
    success_url = reverse_lazy('patient:profile')
    login_url = reverse_lazy('patient:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'patient':
            messages.error(request, 'Brak dostępu')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil zaktualizowany pomyślnie')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.request.user
        return context


