from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientRegistrationForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Witaj {user.first_name}! Twoje konto zostało utworzone.')
            return redirect('visit:home_page')
        else:
            messages.error(request, 'Popraw błędy w formularzu rejestracyjnym.')

    else:
        form = PatientRegistrationForm()

    return render(request, 'patients_registration/register_patient.html', {'form': form})

