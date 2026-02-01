from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import PatientRegistrationForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patients_login:login')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patients_registration/register_patient.html', {'form': form})

